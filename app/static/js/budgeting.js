document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".budget-bar-container").forEach((container) => {
    const current = parseFloat(container.dataset.current);
    const limit = parseFloat(container.dataset.limit);
    const previous = parseFloat(container.dataset.previous);

    const fill = container.querySelector(".budget-bar-fill");
    const previousBar = container.querySelector(".budget-bar-previous");
    const zeroMarker = container.querySelector(".marker-zero");
    const limitMarker = container.querySelector(".marker-limit");

    const rawCurrentPct = limit > 0 ? (current / limit) * 100 : 0;
    const rawPrevPct = limit > 0 ? (previous / limit) * 100 : 0;

    const rightPeak = Math.max(rawCurrentPct, rawPrevPct, 100);
    const buffer = rightPeak > 100 ? 10 : 5;
    const dynamicMax = rightPeak + buffer;

    const currentPct = Math.min(rawCurrentPct, dynamicMax);
    const prevPct = Math.min(rawPrevPct, dynamicMax);
    const limitPct = 100 / dynamicMax * 100;

    fill.style.transition = "none";
    previousBar.style.transition = "none";

    fill.style.left = "0%";
    fill.style.width = "0%";
    previousBar.style.left = "0%";
    previousBar.style.width = "0%";

    fill.offsetHeight;
    previousBar.offsetHeight;

    setTimeout(() => {
      fill.style.transition = "";
      previousBar.style.transition = "";

      fill.style.width = (currentPct / dynamicMax * 100) + "%";
      previousBar.style.width = (prevPct / dynamicMax * 100) + "%";
    }, 10);

    const currentColor = "rgba(76, 175, 80, 0.7)";
    const previousColor = "rgba(33, 150, 243, 0.7)";
    const overLimitColor = "rgba(255, 99, 132, 0.7)";

    fill.style.backgroundColor = rawCurrentPct > 100 ? overLimitColor : currentColor;
    previousBar.style.backgroundColor = previousColor;

    if (Math.abs(currentPct) > Math.abs(prevPct)) {
      fill.style.zIndex = "1";
      previousBar.style.zIndex = "2";
    } else {
      fill.style.zIndex = "2";
      previousBar.style.zIndex = "1";
    }

    zeroMarker.style.left = "0%";
    zeroMarker.style.backgroundColor = "black";

    const limitLeft = 100 / dynamicMax * 100;
    limitMarker.style.left = limitLeft + "%";
    limitMarker.style.backgroundColor = "rgba(255, 0, 0)";
    limitMarker.style.width = "6px";
    limitMarker.style.borderRadius = "3px";
  });

  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((el) => {
    new bootstrap.Tooltip(el);
  });
});
