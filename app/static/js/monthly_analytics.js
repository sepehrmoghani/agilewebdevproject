fetch('/dashboard/api/transactions')
    .then(response => response.json())
    .then(data => {
        const monthlyTotals = {};
        const weeklyTotals = {};

        data.forEach(tx => {
            const dateObj = new Date(tx.date);
            const year = dateObj.getFullYear();

            const monthKey = tx.date.slice(0, 7);
            if (!monthlyTotals[monthKey]) monthlyTotals[monthKey] = 0;
            monthlyTotals[monthKey] += tx.amount;

            const weekNumber = getWeekNumber(dateObj);
            const weekKey = `${year}-W${weekNumber}`;
            if (!weeklyTotals[weekKey]) weeklyTotals[weekKey] = 0;
            weeklyTotals[weekKey] += tx.amount;
        });

        // Render Monthly Chart
        renderChart('monthlyBalanceChart', 'Monthly Transaction Total', monthlyTotals);

        // Render Weekly Chart
        renderChart('weeklyBalanceChart', 'Weekly Transaction Total', weeklyTotals);
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

function renderChart(canvasId, label, dataObj) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.keys(dataObj),
            datasets: [{
                label: label,
                data: Object.values(dataObj),
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
