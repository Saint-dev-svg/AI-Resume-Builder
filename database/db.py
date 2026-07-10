import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "resume.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            education TEXT,
            skills TEXT,
            experience TEXT,
            summary TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    
def save_resume(full_name, email, phone, education, skills, experience, summary):
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO resumes (
            full_name,
            email,
            phone,
            education,
            skills, 
            experience, 
            summary
        )
        
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,(
        full_name,
        email,
        phone,
        education,
        skills,
        experience,
        summary
    ))
    
    conn.commit()
    conn.close()
    
def get_all_resumes():
    conn = sqlite3.connect(DB_PATH)
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