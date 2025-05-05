/* change numbers that dont need dp */
function formatSmartDecimal(value) {
    const fixed = parseFloat(value).toFixed(2);
    return fixed.endsWith(".00") ? parseInt(fixed) : fixed;
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".col_limit, .col_current, .col_target").forEach((cell) => {
        const rawValue = parseFloat(cell.textContent); 
        if (!isNaN(rawValue)) {
            cell.textContent = formatSmartDecimal(rawValue);
        }
    });
});