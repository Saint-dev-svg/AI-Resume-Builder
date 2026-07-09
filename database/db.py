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