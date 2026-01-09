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

    for canonical, variants in SKILL_MAP.items():
        for variant in variants:
            pattern = r"\b" + re.escape(variant) + r"\b"
            match = re.search(pattern, text)

            if match:
                # Look at nearby context (±50 chars)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]

                if any(hint in context for hint in PREFERRED_HINTS):
                    preferred.add(canonical)
                else:
                    required.add(canonical)

                break

    preferred = preferred - required
    return sorted(required), sorted(preferred)

def extract_min_yoe(text: str) -> float | None:
    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*(?:\+?\s*)?(?:years?|yrs?)",
        text
    )

    if not matches:
        return None

    # Conservative: take the minimum required YOE
    return float(min(matches))

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

def extract_keywords(text: str) -> list[str]:
    found = set()
    for kw in KEYWORDS:
        if kw in text:
            found.add(kw)
    return sorted(found)

def parse_jd(jd_text: str):
    text = normalize_text(jd_text)

    required_skills, preferred_skills = extract_skills(text)
    min_yoe = extract_min_yoe(text)
    keywords = extract_keywords(text)

    return {
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "min_yoe": min_yoe,
        "keywords": keywords
    }

