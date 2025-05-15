// Progress Bar
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".progress-bar-container").forEach((container) => {
    const current = parseFloat(container.dataset.current);
    const target = parseFloat(container.dataset.target);
    let percent = target > 0 ? (current / target) * 100 : 0;
    percent = Math.min(percent, 100); // cap at 100%

    const bar = container.querySelector(".progress-bar");
    bar.style.width = percent.toFixed(1) + "%";
    bar.style.height = "20px"; // <-- Set your desired height here

    // Add class if 100%
    if (percent >= 100) {
      bar.classList.add("completed");
    }

    container.nextElementSibling.textContent = percent.toFixed(1) + "%";
  });
});

// Time Left
document.addEventListener("DOMContentLoaded", function () {
  const rows = document.querySelectorAll("table tbody tr");

  rows.forEach((row) => {
    const deadlineCell = row.querySelector("[data-deadline]");
    const timeLeftCell = row.querySelector(".col_time_left");
    const deadlineStr = deadlineCell.getAttribute("data-deadline");

    const deadlineDate = new Date(deadlineStr);
    const now = new Date();

    const timeDiffMs = deadlineDate - now;

    if (isNaN(timeDiffMs)) {
      timeLeftCell.textContent = "-";
      return;
    }

    if (timeDiffMs < 0) {
      timeLeftCell.textContent = "Over due";
      return;
    }

    const totalSeconds = Math.floor(timeDiffMs / 1000);
    const days = Math.floor(totalSeconds / (24 * 3600));
    const hours = Math.floor((totalSeconds % (24 * 3600)) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    let display = "";

    if (totalSeconds > 86400) {
      if (days > 1) {
        display = `${days} days, `;
      } else {
        display = `${days} day, `;
      }
      if (hours > 1) {
        display += `${hours} hours`;
      } else {
        display += `${hours} hour`;
      }
    } else if (totalSeconds > 3600) {
      if (hours > 1) {
        display = `${hours} hours, `;
      } else {
        display = `${hours} hour, `;
      }
      if (minutes > 1) {
        display += `${minutes} minutes`;
      } else {
        display += `${minutes} minute`;
      }
    } else if (totalSeconds > 60) {
      if (minutes > 1) {
        display = `${minutes} minutes, `;
      } else {
        display = `${minutes} minute, `;
      }
      if (seconds > 1) {
        display += `${seconds} seconds`;
      } else {
        display += `${seconds} second`;
      }
    } else {
      if (seconds > 1) {
        display = `${seconds} seconds`;
      } else {
        display = `${seconds} second`;
      }
    }

    timeLeftCell.textContent = display;
  });
});

// Widget #4 Alternating Completed and Upcoming Goals
document.addEventListener("DOMContentLoaded", function () {
  const completed = document.querySelector(".goal-completed");
  const upcoming = document.querySelector(".goal-upcoming");

  if (completed && upcoming) {
    // Initially show completed, hide upcoming
    completed.classList.remove("hidden");
    upcoming.classList.add("hidden");

    let showingCompleted = true;

    setInterval(() => {
      // Hide both first (silence period)
      completed.classList.add("hidden");
      upcoming.classList.add("hidden");

      // After 250ms, show the other one
      setTimeout(() => {
        if (showingCompleted) {
          upcoming.classList.remove("hidden");
        } else {
          completed.classList.remove("hidden");
        }
        showingCompleted = !showingCompleted;
      }, 1000); // silence duration in ms
    }, 5000); // full interval duration
  }
});

// Checkbox
document.getElementById("showHiddenGoalsCheckbox")
  .addEventListener("change", function () {
    const showHidden = this.checked ? "true" : "false";
    const url = new URL(window.location.href);
    url.searchParams.set("show_hidden", showHidden);
    window.location.href = url.toString();
  });
