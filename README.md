# AI Resume Builder

An AI-powered web application built with Flask that helps users create professional resumes and AI-generated cover letters. Users can create, edit, manage, and download resumes and cover letters as PDF documents through a clean and responsive web interface.

## ✨ Features

- 🔐 User registration and login
- 📄 AI-generated professional resume summaries
- 📝 AI-generated cover letters
- 💾 Save resumes to a database
- ✏️ Edit existing resumes
- 🗑️ Delete resumes
- 📥 Download resumes as PDF
- 📥 Download cover letters as PDF
- 🔍 Search resumes
- ↕️ Sort and filter resumes
- 📱 Responsive modern user interface
- 🎨 Clean and intuitive dashboard

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- SQLite

### Frontend
- HTML5
- CSS3
- JavaScript
- Font Awesome

### AI & PDF Generation
- OpenAI API
- ReportLab

### Development Tools
- Git
- GitHub
- Visual Studio Code

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Saint-dev-svg/AI-Resume-Builder.git
```

### 2. Navigate into the project

```bash
cd AI-Resume-Builder
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Create a `.env` file

Add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

### 7. Run the application

```bash
python app.py
```

The application will start locally at:

```text
http://127.0.0.1:5000
```

## 📁 Project Structure

```text
AI-Resume-Builder/
│
├── app.py
├── ai_helper.py
├── db.py
├── pdf_generator.py
├── requirements.txt
├── README.md
├── Procfile
├── .gitignore
│
├── database/
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── resume.html
    ├── edit_resume.html
    ├── view_resume.html
    ├── cover_letter.html
    └── view_cover_letter.html
```

## 🚀 Future Improvements

- Multiple resume templates
- Dark mode
- DOCX export
- AI-powered resume analysis
- Resume scoring and suggestions
- Interview preparation assistant
- Email sharing of resumes and cover letters

## 👨‍💻 Author

**Dennis Kibet Kemboi**

- Software Engineering Student
- Multimedia University of Kenya
- Passionate about Software Engineering, Artificial Intelligence, and Backend Development.

## 📸 Screenshots

### Home Page

![Home Page](screenshots/home.png)

---

### Dashboard

![Dashboard](screenshots/dashboard.png)

---

### Resume Preview

![Resume Preview](screenshots/resume-preview.png)

---

### Cover Letter

![Cover Letter](screenshots/cover-letter.png)

## 🌐 Live Demo

The application is available at:

> **Coming Soon...**

(Will be updated after deployment.)