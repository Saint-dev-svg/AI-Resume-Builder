from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from ai_helper import generate_summary
from config import Config
from pdf_generator import create_resume_pdf
from database.db import (init_db, save_resume, get_all_resumes, 
    get_resume_by_id, 
    delete_resume, update_resume, 
    search_resumes, sort_resumes,
    get_dashboard_stats,
    filter_resumes, save_user,
    get_user_by_email
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
        
        save_resume(
            full_name,
            email,
            phone,
            education,
            skills,
            experience,
            summary
        )
        
        global latest_resume

        latest_resume = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "summary": summary,
            "education": education,
            "skills": skills,
            "experience": experience,
        }

        return render_template(
            "result.html",
            title = "Resume Submitted",
            full_name = full_name,
            email = email,
            phone = phone,
            education = education,
            skills_list = skills_list,
            experience = experience,
            summary = summary
        )
        
        
    return render_template("resume.html", title = "Resume")

@app.route("/cover-letter")
def cover_letter():
    return render_template("cover_letter.html", title = "Cover Letter")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = get_user_by_email(email)

        if user and check_password_hash(user[3], password):
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

    search_query = request.args.get("search", "")
    sort_by = request.args.get("sort", "newest")
    filter_type = request.args.get("filter_type", "")
    filter_value = request.args.get("filter_value", "")

    if search_query:
        resumes = search_resumes(search_query)
        
    elif filter_type and filter_value:
        resumes = filter_resumes(filter_type, filter_value)
    
    else:
        resumes = sort_resumes(sort_by)
        
    stats = get_dashboard_stats()

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
        
        return redirect(url_for("dashboard"))
    
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
        
        existing_user = get_user_by_email(email)
        
        if existing_user:
            return "An account with this email already exists."

        hashed_password = generate_password_hash(password)

        save_user(
            full_name,
            email,
            hashed_password
        )

        return redirect(url_for("dashboard"))

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)