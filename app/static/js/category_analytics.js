
fetch("/dashboard/api/transactions")
    .then((response) => response.json())
    .then((data) => {
        const categoryTotals = {};

        data.forEach((tx) => {
            if (!categoryTotals[tx.category]) categoryTotals[tx.category] = 0;
            categoryTotals[tx.category] += Math.abs(tx.amount);
        });

        const sortedCategories = Object.entries(categoryTotals)
            .sort((a, b) => b[1] - a[1]);
        
        const labels = sortedCategories.map((e) => e[0]);
        const values = sortedCategories.map((e) => e[1]);
        const colors = labels.map((_, i) => `hsl(${(i * 40) % 360}, 70%, 60%)`);

        const ctx = document.getElementById("categoryChart").getContext("2d");
        new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors,
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 2,
                    hoverOffset: 15
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#eee',
                            font: {
                                size: 14
                            },
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: {
                            size: 16
                        },
                        bodyFont: {
                            size: 14
                        },
                        callbacks: {
                            label: function(context) {
                                const value = context.raw;
                                return `$${value.toFixed(2)}`;
                            }
                        }
                    }
                }
            }
        });
    });
