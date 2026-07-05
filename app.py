from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", title = "Home")

@app.route("/resume")
def resume():
    return render_template("resume.html", title = "Resume")

@app.route("/cover-letter")
def cover_letter():
    return render_template("cover_letter.html", title = "Cover Letter")

@app.route("/login")
def login():
    return render_template("login.html", title = "Login")

if __name__ == "__main__":
    app.run(debug=True)