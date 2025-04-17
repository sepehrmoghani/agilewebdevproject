/* Progress Bar */
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".progress-bar-container").forEach((container) => {
    const current = parseFloat(container.dataset.current);
    const target = parseFloat(container.dataset.target);
    let percent = target > 0 ? (current / target) * 100 : 0;
    percent = Math.min(percent, 100); // cap at 100%

    const bar = container.querySelector(".progress-bar");
    bar.style.width = percent.toFixed(1) + "%";
    bar.style.height = "20px"; // <-- Set your desired height here

    container.nextElementSibling.textContent = percent.toFixed(1) + "%";
  });
});

/* Time Left */
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
      timeLeftCell.textContent = "Past due";
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
