// ========== Progress Bar ==========
document.addEventListener("DOMContentLoaded", function () {
      // Edit Goal Modal Handling
    const editGoalModal = document.getElementById('editGoalModal');
    if (editGoalModal) {
        document.querySelectorAll('.edit-goal-btn').forEach(button => {
            button.addEventListener('click', function() {
                const goalId = this.dataset.goalId;
                const form = document.getElementById('editGoalForm');
                const csrf = document.querySelector('input[name="csrf_token"]').value;
                
                form.action = `/budgeting_and_goals/goals/edit/${goalId}`;
                
                // Ensure CSRF token exists in form
                let csrfInput = document.getElementById('edit_csrf_token');
                if (!csrfInput) {
                    csrfInput = document.createElement('input');
                    csrfInput.type = 'hidden';
                    csrfInput.id = 'edit_csrf_token';
                    csrfInput.name = 'csrf_token';
                    form.appendChild(csrfInput);
                }
                csrfInput.value = csrf;
                
                document.getElementById('edit_title').value = this.dataset.title;
                document.getElementById('edit_target_amount').value = this.dataset.targetAmount;
                document.getElementById('edit_current_amount').value = this.dataset.currentAmount;
                document.getElementById('edit_start_date').value = this.dataset.startDate;
                document.getElementById('edit_deadline').value = this.dataset.deadline;
                document.getElementById('edit_description').value = this.dataset.description;

                const modal = new bootstrap.Modal(editGoalModal);
                modal.show();
            });
        });

        document.getElementById('saveGoalBtn').addEventListener('click', function() {
            document.getElementById('editGoalForm').submit();
        });

        document.getElementById('deleteGoalBtn').addEventListener('click', function() {
            if (confirm('Are you sure you want to delete this goal?')) {
                const form = document.getElementById('editGoalForm');
                form.action = form.action.replace('/edit/', '/delete/');
                form.submit();
            }
        });
    }
  document.querySelectorAll(".progress-bar-container").forEach((container) => {
    const current = parseFloat(container.dataset.current);
    const target = parseFloat(container.dataset.target);
    let percent = target > 0 ? (current / target) * 100 : 0;
    percent = Math.min(percent, 100); // cap at 100%

    const bar = container.querySelector(".progress-bar");
    bar.style.width = percent.toFixed(1) + "%";
    bar.style.height = "20px";

    if (percent >= 100) {
      bar.classList.add("completed");
    }

    container.nextElementSibling.textContent = percent.toFixed(1) + "%";
  });

  // ========== Salary Plan Calculator ==========
  function calculateSalaryPlan() {
    const targetAmount = parseFloat(document.getElementById('target_amount')?.value) || 0;
    const currentAmount = parseFloat(document.getElementById('current_amount')?.value) || 0;
    const salaryAmount = parseFloat(document.getElementById('salary_amount')?.value) || 0;
    const salaryFrequency = document.getElementById('salary_frequency')?.value;
    const startDate = new Date(document.getElementById('start_date')?.value);
    const endDate = new Date(document.getElementById('deadline')?.value);
    const outputElement = document.getElementById('salary_plan_output');
    const salaryPercentageInput = document.getElementById('salary_percentage');

    if (
      targetAmount > 0 &&
      salaryAmount > 0 &&
      !isNaN(startDate) &&
      !isNaN(endDate) &&
      startDate < endDate
    ) {
      const remainingAmount = targetAmount - currentAmount;
      const msPerPeriod = {
        weekly: 1000 * 60 * 60 * 24 * 7,
        fortnightly: 1000 * 60 * 60 * 24 * 14,
        monthly: 1000 * 60 * 60 * 24 * 30.44,
        annually: 1000 * 60 * 60 * 24 * 365.25
      };

      const timeDiff = endDate - startDate;
      const totalPayments = timeDiff / msPerPeriod[salaryFrequency];
      const requiredPerPayment = remainingAmount / totalPayments;
      const percentageToSave = Math.min((requiredPerPayment / salaryAmount) * 100, 100);

      if (salaryPercentageInput) {
        salaryPercentageInput.value = percentageToSave.toFixed(2);
      }

      if (outputElement) {
        if (percentageToSave > 100) {
          outputElement.textContent = `⚠️ This goal is not achievable with your current salary and timeline. Try increasing the duration or lowering the target.`;
        } else {
          outputElement.textContent = `💡 If you save ${percentageToSave.toFixed(2)}% of your salary each ${salaryFrequency}, you'll reach your goal of $${targetAmount.toLocaleString()} by ${endDate.toLocaleDateString()}.`;
        }
      }
    } else {
      if (salaryPercentageInput) salaryPercentageInput.value = '';
      if (outputElement) outputElement.textContent = '';
    }
  }

  ['target_amount', 'current_amount', 'salary_amount', 'salary_frequency', 'start_date', 'deadline'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('input', calculateSalaryPlan);
      el.addEventListener('change', calculateSalaryPlan);
    }
  });

  // Run once on load
  calculateSalaryPlan();

  // ========== Time Left Calculator ==========
  document.querySelectorAll("table tbody tr").forEach((row) => {
    const deadlineCell = row.querySelector("[data-deadline]");
    const timeLeftCell = row.querySelector(".col_time_left");
    const deadlineStr = deadlineCell?.getAttribute("data-deadline");

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
      display = `${days} day${days > 1 ? 's' : ''}, ${hours} hour${hours > 1 ? 's' : ''}`;
    } else if (totalSeconds > 3600) {
      display = `${hours} hour${hours > 1 ? 's' : ''}, ${minutes} minute${minutes > 1 ? 's' : ''}`;
    } else if (totalSeconds > 60) {
      display = `${minutes} minute${minutes > 1 ? 's' : ''}, ${seconds} second${seconds > 1 ? 's' : ''}`;
    } else {
      display = `${seconds} second${seconds > 1 ? 's' : ''}`;
    }

    timeLeftCell.textContent = display;
  });

  // ========== Goal Status Toggle ==========
  const completed = document.querySelector(".goal-completed");
  const upcoming = document.querySelector(".goal-upcoming");

  if (completed && upcoming) {
    completed.classList.remove("hidden");
    upcoming.classList.add("hidden");

    let showingCompleted = true;

    setInterval(() => {
      completed.classList.add("hidden");
      upcoming.classList.add("hidden");

      setTimeout(() => {
        if (showingCompleted) {
          upcoming.classList.remove("hidden");
        } else {
          completed.classList.remove("hidden");
        }
        showingCompleted = !showingCompleted;
      }, 1000);
    }, 5000);
  }

  // ========== Hidden Goals Toggle ==========
  const checkbox = document.getElementById("showHiddenGoalsCheckbox");
  if (checkbox) {
    checkbox.addEventListener("change", function () {
      const showHidden = this.checked ? "true" : "false";
      const url = new URL(window.location.href);
      url.searchParams.set("show_hidden", showHidden);
      window.location.href = url.toString();
    });
  }
});
