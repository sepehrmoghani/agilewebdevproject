fetch('/dashboard/api/transactions')
    .then(response => response.json())
    .then(data => {
        const monthlyTotals = {};
        const weeklyTotals = {};

        data.forEach(tx => {
            const dateObj = new Date(tx.date);
            const year = dateObj.getFullYear();

            // Monthly key (e.g. Jan 2024)
            const monthKey = dateObj.toLocaleString('en-US', { month: 'short', year: 'numeric' });
            if (!monthlyTotals[monthKey]) monthlyTotals[monthKey] = 0;
            monthlyTotals[monthKey] += tx.amount;

            // Weekly key (e.g. Jan 1, 2024)
            const weekNumber = getWeekNumber(dateObj);
            const weekKey = getWeekLabel(dateObj);
            if (!weeklyTotals[weekKey]) weeklyTotals[weekKey] = 0;
            weeklyTotals[weekKey] += tx.amount;
        });

        // Sort keys chronologically
        const sortedMonthly = Object.entries(monthlyTotals).sort((a, b) => new Date(a[0]) - new Date(b[0]));
        const sortedWeekly = Object.entries(weeklyTotals).sort((a, b) => new Date(a[0]) - new Date(b[0]));

        // Render Monthly Chart
        renderChart('monthlyBalanceChart', 'Monthly Transaction Total',
            sortedMonthly.map(e => e[0]), sortedMonthly.map(e => e[1]));

        // Render Weekly Chart
        renderChart('weeklyBalanceChart', 'Weekly Transaction Total',
            sortedWeekly.map(e => e[0]), sortedWeekly.map(e => e[1]));
    })
    .catch(err => console.error('Error loading analytics data:', err));

// Utility to get ISO week number
function getWeekNumber(d) {
    d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

// Format week label as "Jan 1, 2024"
function getWeekLabel(d) {
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function renderChart(canvasId, label, labels, dataValues) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: dataValues,
                borderColor: '#00bcd4',
                backgroundColor: 'rgba(0, 188, 212, 0.2)',
                borderWidth: 2,
                pointBackgroundColor: '#00bcd4',
                pointBorderColor: '#fff',
                pointBorderWidth: 3,
                pointRadius: 5,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: label,
                    font: { size: 20 },
                    color: '#eee'
                },
                tooltip: {
                    backgroundColor: '#333',
                    titleFont: { size: 16, weight: 'bold' },
                    bodyFont: { size: 14 }
                },
                legend: {
                    labels: {
                        font: { size: 14 },
                        color: '#ccc'
                    }
                }
            },
            scales: {
                x: {
                    ticks: { color: '#ccc', font: { size: 14 } },
                    grid: { color: '#444' }
                },
                y: {
                    beginAtZero: true,
                    ticks: { color: '#ccc', font: { size: 14 } },
                    grid: { color: '#444' }
                }
            }
        }
    });
}
