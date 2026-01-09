import pdfplumber
import re
from .skill_dictionary import SKILL_MAP

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.lower()

def extract_skills(text: str) -> list[str]:
    found_skills = set()

    for canonical, variants in SKILL_MAP.items():
        for variant in variants:
            pattern = r"\b" + re.escape(variant) + r"\b"
            if re.search(pattern, text):
                found_skills.add(canonical)
                break

    return sorted(found_skills)

def extract_years_of_experience(text: str) -> float:
    yoe_patterns = [
        r'(\d+)\+?\s+years? of experience',
        r'(\d+)\+?\s+yrs? experience',
        r'(\d+)\+?\s+years? experience',
        r'(\d+)\+?\s+yrs? of experience'
    ]

    total_yoe = 0
    for pattern in yoe_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                total_yoe += float(match)
            except ValueError:
                continue

    return total_yoe

def parse_resume(file):
    text = extract_text_from_pdf(file)

    return {
        "skills": extract_skills(text),
        "total_yoe": extract_total_yoe(text),
        "roles": extract_roles(text),
    }

def extract_roles(text: str) -> list[str]:
    role_patterns = [
        r'(?i)(software engineer|developer|programmer|analyst|administrator|consultant|manager|architect|specialist|technician|intern|backend|frontend|full[- ]stack|devops|data scientist|data engineer|qa engineer|tester|product manager|project manager|business analyst)'
    ]

    found_roles = set()
    for pattern in role_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            found_roles.add(match.lower())

    return sorted(found_roles)
