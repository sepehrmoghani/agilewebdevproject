document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".budget-bar-container").forEach((container) => {
    const current = parseFloat(container.dataset.current);
    const limit = parseFloat(container.dataset.limit);
    const previous = parseFloat(container.dataset.previous);

    if (!(current >= 0 && previous >= 0)) return; // Only handle both-positive values

    const fill = container.querySelector(".budget-bar-fill");
    const previousBar = container.querySelector(".budget-bar-previous");
    const zeroMarker = container.querySelector(".marker-zero");
    const limitMarker = container.querySelector(".marker-limit");

    let overflowBar = container.querySelector(".budget-bar-overfill");
    if (!overflowBar) {
      overflowBar = document.createElement("div");
      overflowBar.className = "budget-bar-overfill";
      overflowBar.style.position = "absolute";
      overflowBar.style.height = "100%";
      overflowBar.style.top = "0";
      overflowBar.style.backgroundColor = "rgba(255, 99, 132, 0.7)";
      overflowBar.style.transition = "none";
      container.appendChild(overflowBar);
    }

    const fullScale = 105; // Extend bar container to 105%

    const rawCurrentPct = limit > 0 ? (current / limit) * 100 : 0;
    const rawPreviousPct = limit > 0 ? (previous / limit) * 100 : 0;
    const overflowPct = rawCurrentPct > 100 ? Math.min(rawCurrentPct - 100, 5) : 0;

    const currentPct = Math.min(rawCurrentPct, 100);
    const previousPct = Math.min(rawPreviousPct, 100);

    // Normalize widths to 105% range
    const scaledCurrentPct = (currentPct / fullScale) * 100;
    const scaledPreviousPct = (previousPct / fullScale) * 100;
    const scaledOverflowPct = (overflowPct / fullScale) * 100;

    // Reset transitions and positions
    fill.style.transition = "none";
    previousBar.style.transition = "none";
    overflowBar.style.transition = "none";

    fill.style.left = "0%";
    fill.style.width = "0%";
    previousBar.style.left = "0%";
    previousBar.style.width = "0%";
    overflowBar.style.left = "100%";
    overflowBar.style.width = "0%";

    // Force reflow
    fill.offsetHeight;
    previousBar.offsetHeight;
    overflowBar.offsetHeight;

    // Animate bars
    setTimeout(() => {
      fill.style.transition = "";
      previousBar.style.transition = "";
      overflowBar.style.transition = "";

      fill.style.width = scaledCurrentPct + "%";
      previousBar.style.width = scaledPreviousPct + "%";
      overflowBar.style.width = scaledOverflowPct + "%";
      overflowBar.style.left = ((100 / fullScale) * 100) + "%"; // Place right after 100%
    }, 10);

    // Bar colors
    const currentColor = "rgba(76, 175, 80, 0.7)";
    const previousColor = "rgba(33, 150, 243, 0.7)";

    fill.style.backgroundColor = currentColor;
    previousBar.style.backgroundColor = previousColor;
    overflowBar.style.backgroundColor = "rgba(255, 99, 132, 0.7)";

    // Z-index logic
    fill.style.zIndex = current > previous ? "1" : "2";
    previousBar.style.zIndex = current > previous ? "2" : "1";
    overflowBar.style.zIndex = "3";

    // Zero marker (far left)
    zeroMarker.style.left = "0%";
    zeroMarker.style.backgroundColor = "black";

    // Limit marker (now at ~95.2% to match 100% in new scale)
    const limitPos = (100 / fullScale) * 100;
    limitMarker.style.left = limitPos + "%";
    limitMarker.style.backgroundColor = "rgba(255, 0, 0)";
    limitMarker.style.width = "6px";
    limitMarker.style.borderRadius = "3px";
  });

  // Bootstrap tooltips
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((el) => {
    new bootstrap.Tooltip(el);
  });
});
