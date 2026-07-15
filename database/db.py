import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "resume.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            education TEXT,
            skills TEXT,
            experience TEXT,
            summary TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cover_letters(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        resume_id INTEGER NOT NULL,

        company_name TEXT NOT NULL,
        job_title TEXT NOT NULL,
        hiring_manager TEXT,

        content TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(resume_id) REFERENCES resumes(id)
    )
""")
    
    conn.commit()
    conn.close()
    
def save_resume(
    user_id, full_name, 
    email, phone, 
    education, skills, 
    experience, summary

):
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO resumes (
            user_id,
            full_name,
            email,
            phone,
            education,
            skills, 
            experience, 
            summary
        )
        
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,(
        user_id,
        full_name,
        email,
        phone,
        education,
        skills,
        experience,
        summary
    ))
    
    resume_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return resume_id
    
def get_all_resumes():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, full_name, email
        FROM resumes
        ORDER BY id DESC
    """)
    
    resumes = cursor.fetchall()
    conn.close()
    
    return resumes

def get_resume_by_id(resume_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT *
        FROM resumes
        WHERE id = ? 
    """, (resume_id,))
    
    resume = cursor.fetchone()
    
    conn.close()
    
    return resume

def delete_resume(resume_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM resumes
        WHERE id = ? 
    """, (resume_id,))
    
    conn.commit()
    conn.close()
    
def update_resume(
    resume_id,
    full_name,
    email,
    phone,
    education,
    skills,
    experience,
    summary
):
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE resumes
        SET
            full_name = ?,
            email = ?,
            phone = ?,
            education = ?,
            skills = ?,
            experience = ?,
            summary = ?
        WHERE id = ?
    """, (
        full_name,
        email,
        phone,
        education,
        skills,
        experience,
        summary,
        resume_id
    ))
    
    conn.commit()
    conn.close()
    
def search_resumes(user_id, search_query):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    search = f"%{search_query}%"

    cursor.execute("""
        SELECT id, full_name, email
        FROM resumes
        WHERE user_id = ?
        AND (
            full_name LIKE ?
            OR email LIKE ?
        )
        ORDER BY id DESC
    """, (
        user_id,
        search,
        search
    ))

    resumes = cursor.fetchall()

    conn.close()

    return resumes

def sort_resumes(user_id, sort_by):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if sort_by == "oldest":
        query = """
            SELECT id, full_name, email
            FROM resumes
            WHERE user_id = ?
            ORDER BY id ASC
        """

    elif sort_by == "name_asc":
        query = """
            SELECT id, full_name, email
            FROM resumes
            WHERE user_id = ?
            ORDER BY full_name ASC
        """

    elif sort_by == "name_desc":
        query = """
            SELECT id, full_name, email
            FROM resumes
            WHERE user_id = ?
            ORDER BY full_name DESC
        """

    else:
        query = """
            SELECT id, full_name, email
            FROM resumes
            WHERE user_id = ?
            ORDER BY id DESC
        """

    cursor.execute(query, (user_id,))

    resumes = cursor.fetchall()

    conn.close()

    return resumes

def get_dashboard_stats(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM resumes
        WHERE user_id = ?
    """, (user_id,))
    
    total_resumes = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_resumes": total_resumes
    }
    
def filter_resumes(user_id, filter_type, filter_value):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    filter_text = f"%{filter_value}%"

    if filter_type == "education":
        cursor.execute("""
            SELECT id, full_name, email
            FROM resumes
            WHERE user_id = ?
            AND education LIKE ?
            ORDER BY id DESC
        """, (user_id, filter_text))

    elif filter_type == "skills":
        cursor.execute("""
            SELECT id, full_name, email
            FROM resumes
            WHERE user_id = ?
            AND skills LIKE ?
            ORDER BY id DESC
        """, (user_id, filter_text))

    else:
        cursor.execute("""
            SELECT id, full_name, email
            FROM resumes
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,))

    resumes = cursor.fetchall()

    conn.close()

    return resumes

def save_user(full_name, email, password):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users(
            full_name,
            email,
            password
        )

        VALUES (?, ?, ?)
    """, (
        full_name,
        email,
        password
    ))

    conn.commit()
    conn.close()
    
def get_user_by_email(email):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    conn.close()

    return user

def get_user_resumes(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, full_name, email
        FROM resumes
        WHERE user_id = ?
        ORDER BY DESC
    """, (user_id,))
    
    resumes = cursor.fetchall()
    
    conn.close()
    
    return resumes

def save_cover_letter(
    user_id,
    resume_id,
    company_name,
    job_title,
    hiring_manager,
    content
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cover_letters(
            user_id,
            resume_id,
            company_name,
            job_title,
            hiring_manager,
            content
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        resume_id,
        company_name,
        job_title,
        hiring_manager,
        content
    ))

    letter_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return letter_id
    
def get_cover_letter_by_id(letter_id):
    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM cover_letters
        WHERE id = ?
    """, (letter_id,))

    letter = cursor.fetchone()

    conn.close()

    return letter

def get_all_cover_letters(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM cover_letters
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    letters = cursor.fetchall()

    conn.close()

    return letters