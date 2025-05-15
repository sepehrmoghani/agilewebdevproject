fetch('/dashboard/api/transactions')
    .then(response => response.json())
    .then(data => {
        const categoryTotals = {};

        data.forEach(tx => {
            if (!categoryTotals[tx.category]) categoryTotals[tx.category] = 0;
            categoryTotals[tx.category] += tx.amount;
        });

        // Sort categories alphabetically
        const sortedCategories = Object.entries(categoryTotals).sort((a, b) => a[0].localeCompare(b[0]));
        const labels = sortedCategories.map(e => e[0]);
        const values = sortedCategories.map(e => e[1]);
        const colors = labels.map((_, i) => `hsl(${i * 40 % 360}, 70%, 60%)`);

        const ctx = document.getElementById('categoryChart').getContext('2d');
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
                responsive: true,
                aspectRatio: 1,
                plugins: {
                    title: {
                        display: true,
                        text: 'Spending Breakdown by Category',
                        font: { size: 20 },
                        color: '#eee'
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
                            color: '#eee'
                        }
                    }
                }
            }
        });
    });
