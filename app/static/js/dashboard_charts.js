fetch('/dashboard/api/transactions')
    .then(response => response.json())
    .then(data => {
        const totalIncomeEl = document.getElementById('totalIncome');
        const totalExpensesEl = document.getElementById('totalExpenses');
        const netSavingsEl = document.getElementById('netSavings');

        let categories = {};
        let totalIncome = 0, totalExpenses = 0, netSavings = 0;

        const sortedData = data.slice().sort((a, b) => new Date(a.date) - new Date(b.date));
        let labels = [];
        let amounts = [];
        let transactionTypes = { 'Income': 0, 'Expense': 0, 'Transfer': 0 };

        // Process each transaction
        data.forEach(tx => {
            labels.push(tx.date);
            amounts.push(tx.amount);

            categories[tx.category] = (categories[tx.category] || 0) + tx.amount;

            if (tx.transaction_type === 'Income') {
                totalIncome += tx.amount;
            } else if (tx.transaction_type === 'Expense') {
                totalExpenses += tx.amount;
            }
        });

        netSavings = totalIncome - totalExpenses;
        totalIncomeEl.textContent = `$${totalIncome.toFixed(2)}`;
        totalExpensesEl.textContent = `$${totalExpenses.toFixed(2)}`;
        netSavingsEl.textContent = `$${netSavings.toFixed(2)}`;

        const lineCtx = document.getElementById('transactionLineChart')?.getContext('2d');
        if (lineCtx) {
            new Chart(lineCtx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Transaction Amount',
                        data: amounts,
                        borderColor: '#4bc0c0',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        fill: true,
                        tension: 0.3,
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Transaction Amounts Over Time',
                            font: { size: 18 },
                            color: '#eee'
                        },
                        legend: {
                            labels: { color: '#ccc', font: { size: 14 } }
                        }
                    },
                    scales: {
                        x: { ticks: { color: '#ccc' }, grid: { color: '#444' } },
                        y: { ticks: { color: '#ccc' }, grid: { color: '#444' } }
                    }
                }
            });
        }

        const barCtx = document.getElementById('transactionBarChart')?.getContext('2d');
        if (barCtx) {
            new Chart(barCtx, {
                type: 'bar',
                data: {
                    labels: Object.keys(categories),
                    datasets: [{
                        label: 'Total Spent by Category',
                        data: Object.values(categories),
                        backgroundColor: 'rgba(255, 159, 64, 0.6)',
                        borderColor: '#ff9f40',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Total Amount Spent by Category',
                            font: { size: 18 },
                            color: '#eee'
                        },
                        legend: {
                            labels: { color: '#ccc', font: { size: 14 } }
                        }
                    },
                    scales: {
                        x: { ticks: { color: '#ccc' }, grid: { color: '#444' } },
                        y: { ticks: { color: '#ccc' }, grid: { color: '#444' } }
                    }
                }
            });
        }
    })
    .catch(error => console.error('Error fetching transactions:', error));
