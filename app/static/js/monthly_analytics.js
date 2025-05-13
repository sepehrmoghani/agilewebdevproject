fetch('/dashboard/api/transactions')
    .then(response => response.json())
    .then(data => {
        const monthlyTotals = {};

        data.forEach(tx => {
            const month = tx.date.slice(0, 7); // YYYY-MM
            if (!monthlyTotals[month]) monthlyTotals[month] = 0;
            monthlyTotals[month] += tx.amount;
        });

        const labels = Object.keys(monthlyTotals);
        const values = Object.values(monthlyTotals);

        const ctx = document.getElementById('monthlyBalanceChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Monthly Transaction Total',
                    data: values,
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
                        text: 'Monthly Balance Trends',
                        font: { size: 20 },
                        color: '#333'
                    },
                    tooltip: {
                        backgroundColor: '#333',
                        titleFont: { size: 16, weight: 'bold' },
                        bodyFont: { size: 14 }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(0,0,0,0.1)' },
                        ticks: { color: '#333', font: { size: 14 } }
                    },
                    y: {
                        grid: { color: 'rgba(0,0,0,0.1)' },
                        ticks: { color: '#333', font: { size: 14 } },
                        beginAtZero: true
                    }
                },
                interaction: {
                    mode: 'nearest',
                    intersect: false
                }
            }
        });
    });
