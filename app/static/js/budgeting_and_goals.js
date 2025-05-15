// change numbers that dont need dp 
function formatSmartDecimal(value) {
  const fixed = parseFloat(value).toFixed(2);
  return fixed.endsWith(".00") || fixed.endsWith(".0")
    ? parseInt(fixed)
    : fixed;
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".removeZero").forEach((cell) => {
    const rawValue = parseFloat(cell.textContent);
    if (!isNaN(rawValue)) {
      cell.textContent = formatSmartDecimal(rawValue);
    }
  });
});

// Initialize all tooltips
document.addEventListener("DOMContentLoaded", function () {
  var tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipElements.forEach(function (element) {
    new bootstrap.Tooltip(element);
  });
});

// Flash message function
function createFlashMessage({ message, type, icon, duration = 5000 }) {
  const alert = document.createElement("div");
  alert.className = `alert alert-${type} alert-dismissible fade show position-fixed m-3`;
  alert.style.zIndex = 1055;
  alert.style.right = "0";
  alert.style.bottom = "0";
  alert.innerHTML = `
    <div>
      <i class="fa fa-${icon} me-2"></i>
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <div class="flash-progress-bar mt-2" style="height: 3px; background-color: rgba(255, 255, 255, 0.5); overflow: hidden;">
      <div class="flash-progress-fill" style="height: 100%; width: 100%; background-color: currentColor; transition: width ${duration}ms linear;"></div>
    </div>
  `;

  document.body.appendChild(alert);

  // Start the progress bar animation
  setTimeout(() => {
    alert.querySelector(".flash-progress-fill").style.width = "0%";
  }, 10); // slight delay to trigger CSS transition

  setTimeout(() => {
    alert.classList.remove("show");
    alert.classList.add("hide");
  }, duration);
}

function showStandardSuccess(message = "Success! Your action was completed successfully.") {
  createFlashMessage({
    message: message,
    type: "success",
    icon: "check-circle",
  });
}

window.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);

  if (urlParams.get("success") === "goal_added") {
    showStandardSuccess("Goal added successfully!");
  }

  if (urlParams.get("success") === "goal_edited") {
    createFlashMessage({
      message: "Goal updated successfully!",
      type: "info",
      icon: "info-circle",
    });
  }

  if (urlParams.get("success") === "goal_deleted") {
    showStandardSuccess("Goal deleted successfully!");
  }

  if (urlParams.get("success") === "budget_added") {
    showStandardSuccess("Budget added successfully!");
  }

  if (urlParams.get("success") === "budget_edited") {
    createFlashMessage({
      message: "Budget updated successfully!",
      type: "info",
      icon: "info-circle",
    });
  }

    if (urlParams.get("error") === "goal_update_failed") {
    createFlashMessage({
      message: "An error occurred while updating goal completion status.",
      type: "danger",
      icon: "exclamation-triangle",
    });
  }

    if (urlParams.get("success") === "goal_completed") {
    createFlashMessage({
      message: "Goal marked as completed!",
      type: "warning", 
      icon: "check-circle",
    });
  }

  if (urlParams.get("info") === "goal_already_completed") {
    createFlashMessage({
      message: "Goal is already completed.",
      type: "info",
      icon: "check-circle",
    });
  }


  if (urlParams.get("success") === "goal_hidden") {
    createFlashMessage({
      message: "Goal is now hidden.",
      type: "danger", 
      icon: "eye-slash",
    });
  }

  if (urlParams.get("success") === "goal_unhidden") {
    createFlashMessage({
      message: "Goal is now visible.",
      type: "success", 
      icon: "eye",
    });
  }

  if (urlParams.get("success") === "budget_deleted") {
    showStandardSuccess("Budget deleted successfully!");
  }

  if (urlParams.get("error") === "form_invalid") {
    createFlashMessage({
      message: "There was a problem with your submission.",
      type: "danger",
      icon: "exclamation-triangle",
    });
  }

  if (urlParams.get("error") === "not_authorized_budget") {
    createFlashMessage({
      message: "You are not authorized to delete this budget.",
      type: "danger",
      icon: "exclamation-triangle",
    });
  }

  if (urlParams.get("error") === "not_authorized_goal") {
    createFlashMessage({
      message: "You are not authorized to delete this goal.",
      type: "danger",
      icon: "exclamation-triangle",
    });
  }
});

