def match_resume_to_jd(resume: dict, jd: dict) -> dict:
    resume_skills = set(resume["skills"])
    resume_yoe = resume["total_yoe"]
    resume_education = set(resume.get("education", []))
    resume_qualifications = set(resume.get("qualifications", []))

    required_skills = set(jd["required_skills"])
    preferred_skills = set(jd["preferred_skills"])
    min_yoe = jd["min_yoe"] or 0
    keywords = set(jd["keywords"])
    jd_education = set(jd.get("education", []))
    jd_qualifications = set(jd.get("qualifications", []))

    # --- Skill Match ---
    matched_required = resume_skills & required_skills
    matched_preferred = resume_skills & preferred_skills

    req_score = len(matched_required) / max(len(required_skills), 1)
    
    # If no preferred skills in JD, give full points for preferred skill match
    if len(preferred_skills) == 0:
        pref_score = 1.0  # 100% if no preferred skills to match
    else:
        pref_score = len(matched_preferred) / len(preferred_skills)

    skill_score = (0.7 * req_score + 0.3 * pref_score) * 100

    # --- Experience Match ---
    if min_yoe == 0 or resume_yoe >= min_yoe:
        experience_score = 100
        experience_gap = 0
    else:
        experience_score = (resume_yoe / min_yoe) * 100
        experience_gap = round(min_yoe - resume_yoe, 1)

    # --- Keyword Match ---
    keyword_score = (len(keywords) / max(len(keywords), 1)) * 100

    # --- Education Match ---
    matched_education = resume_education & jd_education
    if len(jd_education) == 0:
        education_score = 100  # No education requirement = full points
    else:
        education_score = (len(matched_education) / len(jd_education)) * 100
    
    # --- Qualifications Match ---
    matched_qualifications = resume_qualifications & jd_qualifications
    
    # Also check if resume education matches JD qualifications (e.g., "bachelor" in both)
    education_as_qualifications = resume_education & jd_qualifications
    matched_qualifications = matched_qualifications | education_as_qualifications
    
    if len(jd_qualifications) == 0:
        qualifications_score = 100  # No specific qualifications = full points
    else:
        qualifications_score = (len(matched_qualifications) / len(jd_qualifications)) * 100

    # --- Overall ---
    # Weights: 50% skills, 20% experience, 15% keywords, 10% education, 5% qualifications
    overall_match = round(
        0.50 * skill_score +
        0.20 * experience_score +
        0.15 * keyword_score +
        0.10 * education_score +
        0.05 * qualifications_score
    )

    return {
        "overall_match": overall_match,
        "skill_score": round(skill_score),
        "experience_score": round(experience_score),
        "keyword_score": round(keyword_score),
        "education_score": round(education_score),
        "qualifications_score": round(qualifications_score),
        "matched_required": list(matched_required),
        "missing_required": list(required_skills - resume_skills),
        "missing_preferred": list(preferred_skills - resume_skills),
        "matched_education": list(matched_education),
        "missing_education": list(jd_education - resume_education),
        "matched_qualifications": list(matched_qualifications),
        "missing_qualifications": list(jd_qualifications - matched_qualifications),
        "experience_gap": experience_gap,
        "explanation": "Strong skill match with minor experience gap"
        if experience_gap > 0 else "Strong overall alignment"
    }
