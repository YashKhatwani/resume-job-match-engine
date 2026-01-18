from app.schemas.ai import AISuggestionRequest

def build_groq_prompt(data: AISuggestionRequest) -> str:
    experience_context = ""
    if data.experience_gap >= 1:
        experience_context = f"- Experience gap: {data.experience_gap} years (FOCUS on this)\n"
    
    return f"""You are an expert resume coach for software engineers. Provide concise, actionable suggestions to improve resume match.

CONTEXT:
- Missing required skills: {', '.join(data.missing_required) if data.missing_required else 'None'}
- Missing preferred skills: {', '.join(data.missing_preferred) if data.missing_preferred else 'None'}
{experience_context}- Key job keywords not covered: {', '.join(data.jd_keywords) if data.jd_keywords else 'None'}

INSTRUCTIONS:
1. Provide 3-4 specific, actionable suggestions ONLY
2. Each suggestion must be something the candidate can ADD, HIGHLIGHT, or REPHRASE on their resume
3. Do NOT invent skills, tools, or experience
4. Do NOT suggest certifications or generic advice
5. Do NOT mention minor experience gaps (less than 1 year)
6. Focus on bridging gaps between their resume and the job requirements
7. Format each suggestion as: [ACTION]: [Specific change to make]
   Examples: "ADD: Experience with [specific tool]" or "HIGHLIGHT: [Skill] used in [context]"
8. Be direct and concise - max 1 line per suggestion

OUTPUT: Only the bulleted suggestions, nothing else."""
