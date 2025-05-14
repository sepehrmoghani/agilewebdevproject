// Fetch transaction data from the API
fetch('/dashboard/api/transactions')
    .then(response => response.json())
    .then(data => {
        // DOM elements
        const totalIncomeEl = document.getElementById('totalIncome');
        const totalExpensesEl = document.getElementById('totalExpenses');
        const netSavingsEl = document.getElementById('netSavings');

        // Containers
        let categories = {};
        let totalIncome = 0, totalExpenses = 0;

        // Sort transactions by date
        const sortedData = data.slice().sort((a, b) => new Date(a.date) - new Date(b.date));

        // Line chart data
        let labels = [];
        let amounts = [];

        sortedData.forEach(tx => {
            const dateObj = new Date(tx.date);
            const formattedDate = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
            labels.push(formattedDate);
            amounts.push(tx.amount);

            // Categorized totals
            categories[tx.category] = (categories[tx.category] || 0) + tx.amount;

            // Totals
            if (tx.transaction_type === 'Income') {
                totalIncome += tx.amount;
            } else if (tx.transaction_type === 'Expense') {
                totalExpenses += tx.amount;
            }
        });

        const netSavings = totalIncome - totalExpenses;

        // Update cards
        totalIncomeEl.textContent = `$${totalIncome.toFixed(2)}`;
        totalExpensesEl.textContent = `$${totalExpenses.toFixed(2)}`;
        netSavingsEl.textContent = `$${netSavings.toFixed(2)}`;

        // Chart 1: Transaction Amounts Over Time (Line)
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
                            color: '#fff'
                        }
                    },
                    scales: {
                        x: { ticks: { color: '#ccc' }, grid: { color: '#444' } },
                        y: { ticks: { color: '#ccc' }, grid: { color: '#444' } }
                    }
                }
            });
        }

        // Chart 2: Total Amount Spent by Category (Bar)
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
                            color: '#fff'
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
