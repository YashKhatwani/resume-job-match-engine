from .skill_dictionary import SKILL_MAP
import re

PREFERRED_HINTS = [
    "nice to have",
    "good to have",
    "preferred",
    "bonus",
    "optional"

]

def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())

def extract_skills(text: str):
    required = set()
    preferred = set()
    
    print(f"  📊 SKILL_MAP has {len(SKILL_MAP)} skills to search for")

    for canonical, variants in SKILL_MAP.items():
        for variant in variants:
            # For skills with special characters like C++, handle differently
            if any(char in variant for char in ['+', '#', '.']):
                # Don't use word boundaries for special characters
                pattern = re.escape(variant)
            else:
                # Use word boundaries for normal alphanumeric skills
                pattern = r"\b" + re.escape(variant) + r"\b"
            
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                print(f"    ✓ Found skill: '{canonical}' (variant: '{variant}')")
                # Look at nearby context (±50 chars)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]

                if any(hint in context for hint in PREFERRED_HINTS):
                    preferred.add(canonical)
                    print(f"      → Marked as PREFERRED")
                else:
                    required.add(canonical)
                    print(f"      → Marked as REQUIRED")

                break

    preferred = preferred - required
    print(f"  Final: {len(required)} required, {len(preferred)} preferred\n")
    return sorted(required), sorted(preferred)

def extract_min_yoe(text: str) -> float | None:
    # First try to match numeric patterns
    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*(?:\+?\s*)?(?:years?|yrs?)",
        text,
        re.IGNORECASE
    )
    
    # If no numeric matches, try word numbers (one, two, three, etc.)
    if not matches:
        word_numbers = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
        }
        for word, num in word_numbers.items():
            if re.search(rf"\b{word}\s*(?:year|yr)", text, re.IGNORECASE):
                matches.append(str(num))

    print(f"  📅 YOE matches found: {matches}")
    
    if not matches:
        print(f"    → No YOE found\n")
        return None

    # Conservative: take the minimum required YOE
    min_yoe = float(min(matches))
    print(f"    → Min YOE: {min_yoe}\n")
    return min_yoe

KEYWORDS = [
    "design",
    "scalable",
    "scalability",
    "ownership",
    "architecture",
    "microservices",
    "lead",
    "mentoring"
]

QUALIFICATIONS = [
    "bachelor",
    "master",
    "mba",
    "phd",
    "ai",
    "artificial intelligence",
    "machine learning",
    "generative ai",
    "agile",
    "scrum",
    "devops",
    "cloud"
]

def extract_keywords(text: str) -> list[str]:
    found = set()
    print(f"  🔑 Checking {len(KEYWORDS)} keywords")
    for kw in KEYWORDS:
        if kw in text:
            found.add(kw)
            print(f"    ✓ Found keyword: '{kw}'")
    if not found:
        print(f"    → No keywords found")
    print()
    return sorted(found)

def extract_education_requirements(text: str) -> list[str]:
    """Extract education level requirements (Bachelor's, Master's, etc.)"""
    found = set()
    print(f"  🎓 Checking education requirements")
    
    education_levels = {
        "master": ["master's", "master degree", "m.s.", "m.a.", "m.eng"],
        "bachelor": ["bachelor's", "bachelor degree", "b.s.", "b.a.", "b.eng"],
        "phd": ["phd", "doctorate", "doctoral"]
    }
    
    for level, variants in education_levels.items():
        for variant in variants:
            if variant in text:
                found.add(level)
                print(f"    ✓ Found: {level}")
                break
    
    if not found:
        print(f"    → No specific degree required")
    print()
    return sorted(found)

def extract_qualifications(text: str) -> list[str]:
    """Extract important qualifications like AI knowledge, Agile, etc."""
    found = set()
    print(f"  📋 Checking {len(QUALIFICATIONS)} qualifications")
    for qual in QUALIFICATIONS:
        if qual in text:
            found.add(qual)
            print(f"    ✓ Found: {qual}")
    
    if not found:
        print(f"    → No special qualifications found")
    print()
    return sorted(found)

def extract_job_title(text: str) -> str:
    """Extract job title from the beginning of the JD"""
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if len(line) > 0 and len(line) < 100:  # Job titles are usually short
            # Skip common header words
            if not any(skip in line.lower() for skip in ["job description", "position", "about us", "company", "we are"]):
                print(f"  💼 Extracted job title: '{line}'")
                return line
    print(f"  💼 No job title found")
    return "Not specified"

def extract_company(text: str) -> str:
    """Extract company name - usually appears early or in About Us section"""
    lines = text.split("\n")
    for i, line in enumerate(lines[:10]):  # Check first 10 lines
        line_lower = line.lower().strip()
        if "company" in line_lower or "about" in line_lower:
            # Check next line for company name
            if i + 1 < len(lines):
                company = lines[i + 1].strip()
                if company and len(company) < 100:
                    print(f"  🏢 Extracted company: '{company}'")
                    return company
    print(f"  🏢 No company found")
    return "Not specified"

def parse_jd(jd_text: str):
    text = normalize_text(jd_text)
    original_text = jd_text  # Keep original for better title/company extraction

    required_skills, preferred_skills = extract_skills(text)
    min_yoe = extract_min_yoe(text)
    keywords = extract_keywords(text)
    education = extract_education_requirements(text)
    qualifications = extract_qualifications(text)
    title = extract_job_title(original_text)
    company = extract_company(original_text)

    return {
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "min_yoe": min_yoe,
        "keywords": keywords,
        "education": education,
        "qualifications": qualifications,
        "title": title,
        "company": company
    }

