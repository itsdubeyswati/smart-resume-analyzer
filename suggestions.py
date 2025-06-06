def get_improvement_suggestions(analysis_result, selected_role):
    suggestions = []

    if analysis_result['match_percentage'] < 50:
        suggestions.append("🚀 Significant opportunity for growth. Focus on building foundational skills for this role.")
    else:
        suggestions.append("👍 Good match! Keep enhancing your skills with advanced topics.")

    # Suggest to learn missing skills
    for skill in analysis_result['missing_skills']:
        suggestions.append(f"🎯 Priority: {skill} - Consider learning this skill to improve your profile.")

    suggestions.append("📝 Resume Enhancement: Use action verbs and quantify achievements.")
    suggestions.append("🔍 Optimize your resume with keywords matching the job description.")

    return suggestions
