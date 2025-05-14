document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".budget-bar-container").forEach((container) => {
    const current = parseFloat(container.dataset.current);
    const limit = parseFloat(container.dataset.limit);
    const previous = parseFloat(container.dataset.previous);

    const fill = container.querySelector(".budget-bar-fill");
    const previousBar = container.querySelector(".budget-bar-previous");
    const zeroMarker = container.querySelector(".marker-zero");
    const limitMarker = container.querySelector(".marker-limit");

    const maxPct = 105;
    const totalRange = maxPct * 2;

    let currentPct = limit > 0 ? (current / limit) * 100 : 0;
    currentPct = Math.max(Math.min(currentPct, maxPct), -maxPct);

    let prevPct = limit > 0 ? (previous / limit) * 100 : 0;
    prevPct = Math.max(Math.min(prevPct, maxPct), -maxPct);

    // Compute positions for previous bar
    const prevStart = ((prevPct < 0 ? prevPct : 0) + maxPct) / totalRange * 100;
    const prevWidth = Math.abs(prevPct) / totalRange * 100;

    previousBar.style.left = prevStart + "%";
    previousBar.style.width = prevWidth + "%";
    previousBar.style.backgroundColor = "#2196F3";

    // Compute positions for current bar
    const currStart = ((currentPct < 0 ? currentPct : 0) + maxPct) / totalRange * 100;
    const currWidth = Math.abs(currentPct) / totalRange * 100;

    fill.style.left = currStart + "%";
    fill.style.width = currWidth + "%";

    // Determine overlap
    const currEnd = currStart + currWidth;
    const prevEnd = prevStart + prevWidth;
    const isOverlap = !(currEnd <= prevStart || prevEnd <= currStart);

    // Determine fill colors
    const overlapColor = "orange";
    const currentColor = "#4caf50"; // green
    const previousColor = "#33adff";

    // Set default colors
    fill.style.backgroundColor = currentColor;
    previousBar.style.backgroundColor = previousColor;

    // Check for overlap
    if (isOverlap) {
    if (currWidth > prevWidth) {
        fill.style.backgroundColor = currentColor;       // current stays green
        previousBar.style.backgroundColor = overlapColor; // previous turns orange
    } else {
        fill.style.backgroundColor = overlapColor;       // current turns orange
        previousBar.style.backgroundColor = previousColor; // previous stays blue
    }
    }


    // Zero marker (0%)
    zeroMarker.style.left = "50%";
    zeroMarker.style.backgroundColor = "black";

    // Limit marker (100%)
    const limitLeft = ((100 + maxPct) / totalRange) * 100;
    limitMarker.style.left = limitLeft + "%";
    limitMarker.style.backgroundColor = "red";
    limitMarker.style.width = "10px";
  });

  // Initialize tooltips
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((el) => {
    new bootstrap.Tooltip(el);
  });
});
