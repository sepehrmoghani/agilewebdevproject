fetch('/dashboard/api/transactions')
    .then(response => response.json())
    .then(data => {
        const categoryTotals = {};

        data.forEach(tx => {
            if (!categoryTotals[tx.category]) categoryTotals[tx.category] = 0;
            categoryTotals[tx.category] += tx.amount;
        });

        const labels = Object.keys(categoryTotals);
        const values = Object.values(categoryTotals);
        const colors = labels.map((_, i) => `hsl(${i * 40 % 360}, 70%, 60%)`);

        const ctx = document.getElementById('categoryPieChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Spending Breakdown by Category',
                    data: values,
                    backgroundColor: colors,
                    hoverOffset: 4,
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,  // This is crucial for resizing the chart
                plugins: {
                    title: {
                        display: true,
                        text: 'Spending Breakdown by Category',
                        font: { size: 20 },
                        color: '#333'
                    },
                    tooltip: {
                        backgroundColor: '#333',
                        titleFont: { size: 16, weight: 'bold' },
                        bodyFont: { size: 14 }
                    },
                    legend: {
                        position: 'top',
                        labels: {
                            font: { size: 14, weight: 'bold' },
                            color: '#333'
                        }
                    }
                }
            }
        });
    });
