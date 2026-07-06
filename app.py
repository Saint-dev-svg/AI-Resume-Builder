from flask import Flask, render_template, request

app = Flask(__name__)

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

        return render_template(
            "result.html",
            title="Resume Submitted",
            full_name=full_name,
            email=email,
            phone=phone,
            education=education,
            skills=skills,
            experience=experience
        )
        
    return render_template("resume.html", title = "Resume")

@app.route("/cover-letter")
def cover_letter():
    return render_template("cover_letter.html", title = "Cover Letter")

@app.route("/login")
def login():
    return render_template("login.html", title = "Login")

if __name__ == "__main__":
    app.run(debug=True)