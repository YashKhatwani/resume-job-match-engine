def match_resume_to_jd(resume: dict, jd: dict) -> dict:
    resume_skills = set(resume["skills"])
    resume_yoe = resume["total_yoe"]

    required_skills = set(jd["required_skills"])
    preferred_skills = set(jd["preferred_skills"])
    min_yoe = jd["min_yoe"] or 0
    keywords = set(jd["keywords"])

    # --- Skill Match ---
    matched_required = resume_skills & required_skills
    matched_preferred = resume_skills & preferred_skills

    req_score = len(matched_required) / max(len(required_skills), 1)
    pref_score = len(matched_preferred) / max(len(preferred_skills), 1)

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

    # --- Overall ---
    overall_match = round(
        0.6 * skill_score +
        0.25 * experience_score +
        0.15 * keyword_score
    )

    return {
        "overall_match": overall_match,
        "skill_score": round(skill_score),
        "experience_score": round(experience_score),
        "keyword_score": round(keyword_score),
        "matched_required": list(matched_required),
        "missing_required": list(required_skills - resume_skills),
        "missing_preferred": list(preferred_skills - resume_skills),
        "experience_gap": experience_gap,
        "explanation": "Strong skill match with minor experience gap"
        if experience_gap > 0 else "Strong overall alignment"
    }
