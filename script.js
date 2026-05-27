const checkboxes = document.querySelectorAll(".taskCheck");
const progressBar = document.getElementById("progressBar");

// 🔊 Sound (with control)
const doneSound = new Audio("https://www.soundjay.com/buttons/sounds/button-3.mp3");
doneSound.volume = 0.4;

// 🔥 State
let state = JSON.parse(localStorage.getItem("planner_state")) || {
    tasks: [],
    streak: 0,
    lastCompleted: null
};

// 🔥 INIT
window.onload = () => {
    checkboxes.forEach((cb, index) => {
        if (state.tasks[index]) {
            cb.checked = true;
            markCompleted(cb);
        }
    });
    updateProgress();
    updateStreak();
};

// 🔥 EVENTS
checkboxes.forEach((cb, index) => {
    cb.addEventListener("change", () => {
        state.tasks[index] = cb.checked;
        saveState();

        if (cb.checked) {
            playSound();
            markCompleted(cb);
            updateStreakLogic();
        } else {
            unmarkCompleted(cb);
        }

        updateProgress();
    });
});

// 🔥 SAVE STATE
function saveState() {
    localStorage.setItem("planner_state", JSON.stringify(state));
}

// 🔊 Play sound safely
function playSound() {
    doneSound.currentTime = 0;
    doneSound.play().catch(() => {});
}

// 🔥 PROGRESS UPDATE (Animated Counter)
function updateProgress() {
    let total = checkboxes.length;
    let completed = state.tasks.filter(Boolean).length;

    let percent = total === 0 ? 0 : Math.round((completed / total) * 100);

    animateProgress(percent);
    showMotivation(percent, total - completed);
}

// 🔥 Smooth Progress Animation + Counter
function animateProgress(target) {
    let current = parseInt(progressBar.style.width) || 0;

    let interval = setInterval(() => {
        if (current >= target) {
            clearInterval(interval);
        } else {
            current++;
            progressBar.style.width = current + "%";
            progressBar.innerText = current + "%";
        }
    }, 10);
}

// 🔥 Completed style
function markCompleted(cb) {
    let box = cb.closest(".box");
    box.style.opacity = "0.5";
    box.style.textDecoration = "line-through";
    box.style.transform = "scale(0.98)";
}

// 🔥 Unmark
function unmarkCompleted(cb) {
    let box = cb.closest(".box");
    box.style.opacity = "1";
    box.style.textDecoration = "none";
    box.style.transform = "scale(1)";
}

// 🔥 Motivation Engine (Dynamic)
function showMotivation(percent, remaining) {
    let msg = "";

    if (percent === 100) {
        msg = "🔥 LEGEND MODE UNLOCKED!";
    } else if (percent > 80) {
        msg = "💪 Almost done, finish strong!";
    } else if (percent > 50) {
        msg = "⚡ You're doing great!";
    } else if (percent > 20) {
        msg = "🚀 Keep pushing!";
    } else {
        msg = "😴 Wake up! Start now!";
    }

    let el = document.getElementById("motivation");

    if (!el) {
        el = document.createElement("div");
        el.id = "motivation";
        el.style.marginTop = "20px";
        el.style.fontSize = "22px";
        el.style.fontWeight = "bold";
        el.style.textAlign = "center";
        document.body.appendChild(el);
    }

    el.innerText = `${msg} (${remaining} tasks left)`;
}

// 🔥 STREAK SYSTEM (DAILY CONSISTENCY)
function updateStreakLogic() {
    let today = new Date().toDateString();

    if (state.lastCompleted !== today) {
        state.streak++;
        state.lastCompleted = today;
        saveState();
    }
}

// 🔥 SHOW STREAK
function updateStreak() {
    let el = document.getElementById("streak");

    if (!el) {
        el = document.createElement("div");
        el.id = "streak";
        el.style.marginTop = "10px";
        el.style.textAlign = "center";
        el.style.fontSize = "18px";
        document.body.appendChild(el);
    }

    el.innerText = `🔥 Streak: ${state.streak} days`;
}
