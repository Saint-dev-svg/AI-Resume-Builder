from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ai_helper import generate_summary, generate_cover_letter
from config import Config
from pdf_generator import create_resume_pdf
from cover_letter_pdf import create_cover_letter_pdf
from database.db import (init_db, save_resume, get_all_resumes, 
    get_resume_by_id, 
    delete_resume, update_resume, 
    search_resumes, sort_resumes,
    get_dashboard_stats,
    filter_resumes, save_user,
    get_user_by_email, 
    
    save_cover_letter, get_all_cover_letters, get_cover_letter_by_id
)


app = Flask(__name__)
app.config.from_object(Config)

init_db()

latest_resume = {}

@app.route("/")
def home():
    return render_template("index.html", title = "Home")

@app.route("/resume", methods=["GET", "POST"])
def resume():
    
    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        education = request.form["education"]
        skills = request.form["skills"]
        experience = request.form["experience"]
        
        if not full_name.strip():
            return "Error: Full name can not be empty!"
        
        if "@" not in email:
            return "Error: Please enter a valid email address!"
        
        if len(phone) < 10:
            return "Error: Phone number is too short!"
        
        skills_list = [skill.strip() for skill in skills.split(",")]
        
        summary = generate_summary(
            full_name,
            education,
            skills,
            experience
            
        )
        
        user_id = session["user_id"]
        
        resume_id = save_resume(
            user_id,
            full_name,
            email,
            phone,
            education,
            skills,
            experience,
            summary
        )
        
        flash("Resume created successfully!", "success")
        
        return redirect(url_for("view_resume", resume_id=resume_id))
        
    return render_template("resume.html", title = "Resume")

@app.route("/cover-letter/<int:resume_id>", methods=["GET", "POST"])
def cover_letter(resume_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    resume = get_resume_by_id(resume_id)

    if not resume:
        return "Resume not found."

    if request.method == "POST":

        company_name = request.form["company_name"]
        job_title = request.form["job_title"]
        hiring_manager = request.form["hiring_manager"]

        content = generate_cover_letter(
            resume["full_name"],
            resume["education"],
            resume["skills"],
            resume["experience"],
            company_name,
            job_title,
            hiring_manager
        )

        letter_id = save_cover_letter(
            session["user_id"],
            resume_id,
            company_name,
            job_title,
            hiring_manager,
            content
        )

        return redirect(
            url_for(
                "view_cover_letter",
                letter_id = letter_id
            )
        )

    return render_template(
        "cover_letter.html",
        resume=resume
    )
    
@app.route("/view-cover-letter/<int:letter_id>")
def view_cover_letter(letter_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    letter = get_cover_letter_by_id(letter_id)

    if not letter:
        return "Cover letter not found."

    return render_template(
        "view_cover_letter.html",
        letter=letter
    )
    
@app.route("/download-cover-letter/<int:letter_id>")
def download_cover_letter(letter_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    letter = get_cover_letter_by_id(letter_id)

    if not letter:
        return "Cover letter not found."

    pdf = create_cover_letter_pdf(letter["content"])

    return send_file(
        pdf,
        as_attachment=True,
        download_name="cover_letter.pdf",
        mimetype="application/pdf"
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = get_user_by_email(email)

        if user and check_password_hash(user[3], password):
            session["user_id"] = user["id"]
            session["full_name"] = user["full_name"]
            return redirect(url_for("dashboard"))

        return "Invalid email or password."

    return render_template("login.html")

@app.route("/download")
def download_resume():
    pdf = create_resume_pdf(latest_resume)
        
    return send_file(
        pdf,
        as_attachment=True,
        download_name="resume.pdf",
        mimetype="application/pdf"
    )

@app.route("/dashboard")
def dashboard():
    
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    print(user_id)
    print(type(user_id))

    search_query = request.args.get("search", "")
    sort_by = request.args.get("sort", "newest")
    filter_type = request.args.get("filter_type", "")
    filter_value = request.args.get("filter_value", "")

    if search_query:
        resumes = search_resumes(user_id, search_query)
        
    elif filter_type and filter_value:
        resumes = filter_resumes(user_id, filter_type, filter_value)
    
    else:
        resumes = sort_resumes(user_id, sort_by)
        
    stats = get_dashboard_stats(user_id)

    return render_template(
        "dashboard.html",
        resumes=resumes,
        search_query=search_query,
        sort_by=sort_by,
        filter_type=filter_type,
        filter_value=filter_value,
        stats=stats
    )

@app.route("/resume/<int:resume_id>")
def view_resume(resume_id):
    
    resume = get_resume_by_id(resume_id)
    
    return render_template(
        "view_resume.html",
        resume = resume
    )
    
@app.route("/download-resume/<int:resume_id>")
def download_resume_pdf(resume_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    resume = get_resume_by_id(resume_id)

    if not resume:
        return "Resume not found."

    pdf = create_resume_pdf(resume)

    return send_file(
        pdf,
        as_attachment=True,
        download_name=f"{resume['full_name']}_Resume.pdf",
        mimetype="application/pdf"
    )
    
@app.route("/delete/<int:resume_id>")
def delete_resume_route(resume_id):
    
    delete_resume(resume_id)
    
    return redirect(url_for("dashboard"))

@app.route("/edit/<int:resume_id>", methods = ["GET", "POST"])
def edit_resume(resume_id):
    if request.method == "POST":
                
        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        education = request.form["education"]
        skills = request.form["skills"]
        experience = request.form["experience"]
        summary = request.form["summary"]
        
        update_resume(
            resume_id,
            full_name,
            email,
            phone,
            education,
            skills,
            experience,
            summary
        )
        
        return redirect(url_for("view_resume", resume_id=resume_id))
    
    resume = get_resume_by_id(resume_id)
    
    return render_template(
        "edit_resume.html",
        resume = resume
    )
    
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))
        
        existing_user = get_user_by_email(email)
        
        if existing_user:
            flash("An account with this email already exists.", "error")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        save_user(
            full_name,
            email,
            hashed_password
        )
        
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)