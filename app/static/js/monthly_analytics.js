fetch('/dashboard/api/transactions')
    .then(response => response.json())
    .then(data => {
        const monthlyTotals = {};
        const weeklyTotals = {};

        data.forEach(tx => {
            const dateObj = new Date(tx.date);
            const year = dateObj.getFullYear();

            const monthKey = tx.date.slice(0, 7);
            monthlyTotals[monthKey] = (monthlyTotals[monthKey] || 0) + tx.amount;

            const weekNumber = getWeekNumber(dateObj);
            const weekKey = `${year}-W${weekNumber}`;
            weeklyTotals[weekKey] = (weeklyTotals[weekKey] || 0) + tx.amount;
        });

        renderChart('monthlyBalanceChart', 'Monthly Transaction Total', monthlyTotals, formatMonthLabel);
        renderChart('weeklyBalanceChart', 'Weekly Transaction Total', weeklyTotals, formatWeekLabel);
    })
    .catch(err => console.error('Error loading analytics data:', err));

function getWeekNumber(d) {
    d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    const weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
    return String(weekNo).padStart(2, '0');
}

function formatMonthLabel(key) {
    const [year, month] = key.split('-');
    return new Date(`${year}-${month}-01`).toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
}

function formatWeekLabel(key) {
    return key.replace('-W', ' Week ');
}

function renderChart(canvasId, label, dataObj, labelFormatter) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const sortedKeys = Object.keys(dataObj).sort();

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: sortedKeys.map(labelFormatter),
            datasets: [{
                label: label,
                data: sortedKeys.map(k => dataObj[k]),
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
