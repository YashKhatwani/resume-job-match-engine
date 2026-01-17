import pdfplumber
import re
import datetime
import calendar
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
            # For skills with special characters like C++, handle differently
            if any(char in variant for char in ['+', '#', '.']):
                # Don't use word boundaries for special characters
                pattern = re.escape(variant)
            else:
                # Use word boundaries for normal alphanumeric skills
                pattern = r"\b" + re.escape(variant) + r"\b"
            
            if re.search(pattern, text, re.IGNORECASE):
                found_skills.add(canonical)
                break

    return sorted(found_skills)

# This is not giving proper year of experience need to debug
def extract_years_of_experience(text: str) -> float:
    """
    Extract years of experience by parsing date ranges.
    Handles formats like:
      - "Jan 2018 - Mar 2021"
      - "2016 - 2019"
      - "2023 - Present"
      - "June 2017 to Present"
    """
    import datetime
    import calendar

    text = text or ""
    text_lower = text.lower()
    
    print(f"\n📝 DEBUG: Input text to parse:\n{text[:500]}\n")  # ← Debug print
    
    month_map = {
        "jan": 1, "january": 1,
        "feb": 2, "february": 2,
        "mar": 3, "march": 3,
        "apr": 4, "april": 4,
        "may": 5,
        "jun": 6, "june": 6,
        "jul": 7, "july": 7,
        "aug": 8, "august": 8,
        "sep": 9, "sept": 9, "september": 9,
        "oct": 10, "october": 10,
        "nov": 11, "november": 11,
        "dec": 12, "december": 12,
    }

    def parse_date_token(token: str):
        token = token.strip().lower()
        if re.search(r'\bpresent\b|\bcurrent\b|\bnow\b', token):
            return datetime.date.today()

        # month name + year (e.g., "Jan 2018")
        for name, mnum in month_map.items():
            m = re.search(rf"\b{name}\b\s*(\d{{4}})", token, flags=re.I)
            if m:
                year = int(m.group(1))
                return datetime.date(year, mnum, 1)

        # year-only (e.g., "2018")
        m = re.search(r"\b(19|20)\d{2}\b", token)
        if m:
            year = int(m.group(0))
            return datetime.date(year, 1, 1)

        return None

    intervals = []

    # Pattern 1: Month Year - Month Year (e.g., "Jan 2018 - Mar 2021")
    month_names = r'(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)'
    pattern_month_range = re.compile(
        rf"(?P<start>{month_names}\s+\d{{4}})\s*(?:[-–—]|to)\s*(?P<end>{month_names}\s+\d{{4}}|present|current|now)",
        flags=re.I
    )

    print("🔍 Pattern 1 (Month Year - Month Year):")
    matched_positions = set()  # Track which positions Pattern 1 matched
    
    for m in pattern_month_range.finditer(text):
        s_tok = m.group('start')
        e_tok = m.group('end')
        s_date = parse_date_token(s_tok)
        e_date = parse_date_token(e_tok)
        
        print(f"  Found: '{s_tok}' to '{e_tok}' -> {s_date} to {e_date}")
        
        if s_date and e_date and s_date <= e_date:
            if e_date.day == 1 and not re.search(r'present|current|now', e_tok, flags=re.I):
                last_day = calendar.monthrange(e_date.year, e_date.month)[1]
                e_date = datetime.date(e_date.year, e_date.month, last_day)
            intervals.append((s_date, e_date))
            matched_positions.add((m.start(), m.end()))  # Track match position
            print(f"    ✓ Added to intervals")

    # Pattern 2: Year - Year or Year - Present (e.g., "2018 - 2021" or "2023 - Present")
    # Only match if NOT already matched by Pattern 1
    pattern_year_range = re.compile(
        r"\b(?P<start>19|20)(?P<start_year>\d{2})\b\s*(?:[-–—]|to)\s*(?P<end>present|current|now|(?:19|20)\d{2})\b",
        flags=re.I
    )
    
    print("\n🔍 Pattern 2 (Year - Year):")
    for m in pattern_year_range.finditer(text):
        # Skip if this match overlaps with Pattern 1
        overlap = any(m.start() < end and m.end() > start for start, end in matched_positions)
        if overlap:
            print(f"  Skipped (already matched by Pattern 1): '{m.group(0)}'")
            continue
        
        s_year = int(m.group('start') + m.group('start_year'))
        e_token = m.group('end').lower()
        
        s_date = datetime.date(s_year, 1, 1)
        
        if re.search(r'\bpresent\b|\bcurrent\b|\bnow\b', e_token):
            e_date = datetime.date.today()
        else:
            e_year = int(e_token)
            e_date = datetime.date(e_year, 12, 31)
        
        print(f"  Found: '{s_year}' to '{e_token}' -> {s_date} to {e_date}")
        
        if s_date <= e_date:
            intervals.append((s_date, e_date))
            print(f"    ✓ Added to intervals")

    print(f"\n📊 All intervals before merging: {intervals}\n")

    # Merge overlapping intervals
    if intervals:
        intervals = sorted(intervals, key=lambda x: x[0])
        merged = []
        
        for start, end in intervals:
            if not merged:
                merged.append([start, end])
            else:
                last_start, last_end = merged[-1]
                # If intervals overlap or are adjacent, merge them
                if start <= last_end + datetime.timedelta(days=90):  # 90 days grace period for job transitions
                    merged[-1][1] = max(last_end, end)
                else:
                    merged.append([start, end])

        total_days = 0
        for s, e in merged:
            if e >= s:
                total_days += (e - s).days + 1

        total_years = round(total_days / 365.25, 1)
        
        print(f"\n✓ Date ranges found:")
        for s, e in merged:
            days = (e - s).days + 1
            years = round(days / 365.25, 1)
            print(f"  {s} to {e} ({years} years)")
        print(f"  Total YOE: {total_years} years\n")
        
        return total_years

    # Fallback: Search for numeric YOE patterns
    yoe_patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*years? of experience",
        r"(\d+(?:\.\d+)?)\s*\+?\s*yrs? of experience",
        r"(\d+(?:\.\d+)?)\s*\+?\s*years? experience",
        r"(\d+(?:\.\d+)?)\s*\+?\s*yrs? experience",
    ]

    total_yoe = 0.0
    for pattern in yoe_patterns:
        matches = re.findall(pattern, text, flags=re.I)
        for match in matches:
            try:
                total_yoe += float(match)
            except Exception:
                continue

    if total_yoe > 0:
        print(f"✓ YOE from keyword patterns: {total_yoe} years\n")
        return total_yoe

    return 0.0

def extract_work_experience_section(text: str) -> str:
    """Extract only the work experience section from resume text."""
    section_pattern = r"(?i)(work\s+experience|professional\s+experience|experience|employment\s+history|career\s+history)"
    end_pattern = r"(?i)(education|skills|certifications|projects|awards|languages|technical\s+skills|summary|objective)"
    
    section_match = re.search(section_pattern, text)
    if not section_match:
        return ""
    
    start_pos = section_match.start()
    remaining_text = text[start_pos + len(section_match.group(0)):]
    end_match = re.search(end_pattern, remaining_text)
    
    if end_match:
        end_pos = start_pos + len(section_match.group(0)) + end_match.start()
        return text[start_pos:end_pos]
    
    return remaining_text

def parse_resume(file):
    text = extract_text_from_pdf(file)
    experience_section = extract_work_experience_section(text)  # ← Extract first

    # print("Extracted Work Experience Section:\n", experience_section)

    return {
        "raw_text": text,
        "skills": extract_skills(text),
        "total_yoe": extract_years_of_experience(experience_section),
        "roles": extract_roles(text),
        "education": extract_education(text),
        "qualifications": extract_qualifications(text),
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

def extract_education(text: str) -> list[str]:
    """Extract education level from resume (Bachelor's, Master's, PhD, etc.)"""
    found = set()
    
    education_levels = {
        "bachelor": [
            "bachelor's", "bachelor degree", "b.s.", "b.a.", "b.eng", 
            "bs computer science", "bachelor of", "b. tech", "btech",
            "bachelor"
        ],
        "master": [
            "master's", "master degree", "m.s.", "m.a.", "m.eng", 
            "ms computer science", "master of", "m. tech", "mtech",
            "master"
        ],
        "phd": [
            "phd", "doctorate", "doctoral degree", "ph.d.", "doctor of"
        ]
    }
    
    text_lower = text.lower()
    
    for level, variants in education_levels.items():
        for variant in variants:
            if variant in text_lower:
                found.add(level)
                break
    
    return sorted(found)

def extract_qualifications(text: str) -> list[str]:
    """Extract qualifications like AI knowledge, Agile, SCRUM, etc. from resume"""
    qualifications = [
        "agile",
        "scrum",
        "ai",
        "artificial intelligence",
        "machine learning",
        "generative ai",
        "devops",
        "cloud",
        "aws",
        "gcp",
        "azure"
    ]
    
    found = set()
    for qual in qualifications:
        if qual in text.lower():
            found.add(qual)
    
    return sorted(found)
