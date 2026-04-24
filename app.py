from flask import Flask, render_template, request
import random
from datetime import datetime

app = Flask(__name__)

# ⏰ Time formatter
def format_time(hour):
    h = int(hour)
    m = int((hour - h) * 60)

    am_pm = "AM" if h < 12 else "PM"
    h = h % 12 or 12

    return f"{h}:{m:02d} {am_pm}"


# 🧠 Smart Strategy Engine
def get_strategy(subject):
    methods = [
        "📘 Concept → Practice → Revise",
        "🧠 Active Recall + Self Testing",
        "📖 Learn → Solve Questions",
        "✍️ Notes + Quick Revision",
        "🔁 Spaced Repetition Focus"
    ]

    return {
        "method": random.choice(methods),
        "tips": [
            "Focus on 1 concept at a time",
            "Avoid multitasking",
            "Revise within 24 hrs",
            "Solve questions after theory"
        ]
    }


# ⚡ AI Tips Engine
def get_ai_tip():
    tips = [
        "🔥 Study hardest subject first (morning focus)",
        "⚡ Pomodoro: 50 min study + 10 min break",
        "🧠 Revise before sleep",
        "📵 Keep phone away",
        "🎯 Set small daily targets"
    ]
    return random.choice(tips)


# 🧠 Difficulty detection (basic AI feel)
def get_difficulty(subject):
    hard_keywords = ["dsa", "math", "algorithm", "physics", "coding"]
    if any(k in subject.lower() for k in hard_keywords):
        return 1.5  # more time
    return 1


# 🚀 MAIN PLAN GENERATOR (SMART)
def generate_plan(subjects, hours, start_time=8):

    subject_list = [s.strip() for s in subjects.split(",") if s.strip()]

    if not subject_list or hours <= 0:
        return [], 0

    # 🎯 Assign weights (priority + difficulty)
    weights = []
    for i, sub in enumerate(subject_list):
        base = len(subject_list) - i  # priority
        difficulty = get_difficulty(sub)
        weights.append(base * difficulty)

    total_weight = sum(weights)

    break_time = 0.25
    total_break = break_time * (len(subject_list) - 1)

    effective_hours = hours - total_break
    if effective_hours <= 0:
        return [], 0

    plan = []
    current_time = start_time

    for i, sub in enumerate(subject_list):

        time_alloc = (weights[i] / total_weight) * effective_hours

        start = current_time
        end = current_time + time_alloc

        strategy = get_strategy(sub)

        # 🎯 Productivity score per subject
        productivity = random.randint(70, 95)

        plan.append({
            "subject": sub,
            "start": format_time(start),
            "end": format_time(end),
            "hours": round(time_alloc, 2),
            "method": strategy["method"],
            "tips": strategy["tips"],
            "ai_tip": get_ai_tip(),
            "productivity": f"{productivity}%"
        })

        # Add break except last
        if i != len(subject_list) - 1:
            current_time = end + break_time
        else:
            current_time = end

    # 🏆 Overall productivity score
    overall_score = random.randint(75, 92)

    return plan, overall_score


# 🌐 ROUTES
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        subjects = request.form.get("subjects", "")
        hours = float(request.form.get("hours", 0))

        plan, score = generate_plan(subjects, hours)

        return render_template(
            "result.html",
            plan=plan,
            total=hours,
            score=score,
            today=datetime.now().strftime("%d %B %Y")
        )

    return render_template("index.html")


if __name__ == "__main__":
    if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

