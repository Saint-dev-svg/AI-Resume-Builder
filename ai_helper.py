def infer_role(skills):
    skills = skills.lower()

    if "flask" in skills or "django" in skills:
        return "backend software developer"

    elif "react" in skills or "javascript" in skills:
        return "frontend software developer"

    elif "tensorflow" in skills or "machine learning" in skills:
        return "AI engineer"

    elif "java" in skills:
        return "software developer"

    else:
        return "software engineering student"
    

def build_opening(full_name, education, skills):
    
    role = infer_role(skills)
    return (
        f"{full_name} is a motivated {role} "
        f"with a background in {education}. "
    )


def build_skills(skills):
    skills_list = [skill.strip() for skill in skills.split(",")]

    if len(skills_list) == 1:
        return (
            f"Demonstrates expertise in {skills_list[0]}, "
        )

    elif len(skills_list) == 2:
        return (
            f"Possesses strong technical skills in {skills_list[0]} and {skills_list[1]}, "
        )

    else:
        first_two = ", ".join(skills_list[:2])
        remaining = len(skills_list) - 2

        return (
            f"Possesses strong technical skills in {first_two} "
            f"and {remaining} additional technologies, "
        )

def build_experience(experience):
    experience = experience.strip()

    if len(experience) < 50:
        return (
            f"Has gained practical experience in {experience}. "
        )

    elif len(experience) < 150:
        return (
            f"Has built valuable hands-on experience through {experience}. "
        )

    else:
        return (
            f"Brings extensive practical experience, including {experience}. "
        )

def build_closing(skills):
    skills = skills.lower()

    if "python" in skills:
        return (
            "Passionate about developing scalable backend applications and continuously expanding Python expertise."
        )

    elif "react" in skills or "javascript" in skills:
        return (
            "Enjoys creating responsive, user-friendly web interfaces and delivering exceptional user experiences."
        )

    elif "machine learning" in skills or "tensorflow" in skills:
        return (
            "Passionate about applying artificial intelligence and data-driven solutions to solve real-world challenges."
        )

    else:
        return (
            "Committed to continuous learning, teamwork, and building high-quality software solutions."
        )

def generate_summary(full_name, education, skills, experience):
    return (
        build_opening(full_name, education, skills)
        + build_skills(skills)
        + build_experience(experience)
        + build_closing(skills)
    )