def generate_plan(subjects, hours, start_time=8):
    # Clean input
    subject_list = [s.strip() for s in subjects.split(",") if s.strip()]
    
    if not subject_list or hours <= 0:
        return []

    total_subjects = len(subject_list)

    # Keep 15 min break between subjects
    break_time = 0.25  # hours
    total_break_time = break_time * (total_subjects - 1)

    # Effective study time (excluding breaks)
    effective_hours = hours - total_break_time
    if effective_hours <= 0:
        return []

    time_per_subject = effective_hours / total_subjects

    # Smart study methods rotation
    methods = [
        "📚 Pomodoro (50-10) + quick revision",
        "🧠 Active Recall + Self Testing",
        "📖 Concept + Practice Questions",
        "✍️ Notes Making + Revision",
        "🔁 Spaced Repetition Focus"
    ]

    # Smart tips rotation
    tips = [
        "🔥 No phone | Deep focus | Airplane mode",
        "⚡ Focus on weak areas first",
        "🧘 Stay hydrated + proper posture",
        "🎯 Solve questions after concepts",
        "🚫 Avoid multitasking"
    ]

    plan = []
    current_time = start_time

    for i, sub in enumerate(subject_list):
        start = current_time
        end = current_time + time_per_subject

        plan.append({
            "subject": sub,
            "start": format_time(start),
            "end": format_time(end),
            "hours": round(time_per_subject, 2),
            "method": methods[i % len(methods)],
            "tip": tips[i % len(tips)]
        })

        # Add break except after last subject
        if i != total_subjects - 1:
            current_time = end + break_time
        else:
            current_time = end

    return plan

