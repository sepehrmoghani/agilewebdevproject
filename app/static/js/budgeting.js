document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".budget-bar-container").forEach((container) => {
    const current = parseFloat(container.dataset.current);
    const limit = parseFloat(container.dataset.limit);
    const previous = parseFloat(container.dataset.previous);

    const fill = container.querySelector(".budget-bar-fill");
    const previousBar = container.querySelector(".budget-bar-previous");
    const zeroMarker = container.querySelector(".marker-zero");
    const limitMarker = container.querySelector(".marker-limit");

    // Compute raw % values relative to the limit
    let rawCurrentPct = limit > 0 ? (current / limit) * 100 : 0;
    let rawPrevPct = limit > 0 ? (previous / limit) * 100 : 0;

    // Determine the maximum absolute extent from center (symmetric)
    // Determine the dynamic max (largest absolute % value)
    const peakPct = Math.max(Math.abs(rawCurrentPct), Math.abs(rawPrevPct), 100);

    // Add a buffer of 5% to each side
    const buffer = 20;
    const dynamicMax = peakPct + buffer;
    const totalRange = dynamicMax * 2;

    // Scale and clamp for bar calculation
    let currentPct = Math.max(Math.min(rawCurrentPct, dynamicMax), -dynamicMax);
    let prevPct = Math.max(Math.min(rawPrevPct, dynamicMax), -dynamicMax);

    // Compute visual positions
    const currStart = ((currentPct < 0 ? currentPct : 0) + dynamicMax) / totalRange * 100;
    const currWidth = Math.abs(currentPct) / totalRange * 100;

    const prevStart = ((prevPct < 0 ? prevPct : 0) + dynamicMax) / totalRange * 100;
    const prevWidth = Math.abs(prevPct) / totalRange * 100;

    // Apply positions
    // Set initial styles without transition (start point)
    fill.style.transition = "none";
    previousBar.style.transition = "none";

    fill.style.left = "50%";
    fill.style.width = "0%";
    previousBar.style.left = "50%";
    previousBar.style.width = "0%";

    // Force reflow to apply the styles immediately
    fill.offsetHeight;
    previousBar.offsetHeight;

    // Animate to final position and size
    setTimeout(() => {
      fill.style.transition = "";  // restore CSS transition
      previousBar.style.transition = "";

      fill.style.left = currStart + "%";
      fill.style.width = currWidth + "%";

      previousBar.style.left = prevStart + "%";
      previousBar.style.width = prevWidth + "%";
    }, 10);



    // Bar color logic
    const currentColor = "rgba(76, 175, 80, 0.7)";
    const previousColor = "rgba(33, 150, 243, 0.7)";
    const overLimitColor = "rgba(255, 99, 132, 0.7)";

    fill.style.backgroundColor = currentPct > 100 ? overLimitColor : currentColor;
    previousBar.style.backgroundColor = previousColor;

    // Z-index based on prominence
    if (Math.abs(currentPct) > Math.abs(prevPct)) {
      fill.style.zIndex = "1";
      previousBar.style.zIndex = "2";
    } else {
      fill.style.zIndex = "2";
      previousBar.style.zIndex = "1";
    }

    // Keep zero marker always centered
    zeroMarker.style.left = "50%";
    zeroMarker.style.backgroundColor = "black";

    // Recompute limit marker (relative to new dynamic range)
    const limitLeft = ((100 + dynamicMax) / totalRange) * 100;
    limitMarker.style.left = limitLeft + "%";
    limitMarker.style.backgroundColor = "rgba(255, 0, 0)";
    limitMarker.style.width = "6px";
    limitMarker.style.borderRadius = "3px";
  });

  // Bootstrap tooltips
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((el) => {
    new bootstrap.Tooltip(el);
  });
});
