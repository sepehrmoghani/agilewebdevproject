// Fetch transaction data from the API
fetch('/dashboard/api/transactions')
    .then(response => response.json())
    .then(data => {
        // DOM elements
        const currentBalanceEl = document.getElementById('currentBalance');
        const totalIncomeEl = document.getElementById('totalIncome');
        const totalExpensesEl = document.getElementById('totalExpenses');
        const netSavingsEl = document.getElementById('netSavings');

        // Data containers
        let labels = [];
        let amounts = [];
        let balances = [];
        let categories = {};
        let transactionTypes = { 'Income': 0, 'Expense': 0, 'Transfer': 0 };

        // Calculated values
        let totalIncome = 0;
        let totalExpenses = 0;
        let netSavings = 0;
        let currentBalance = 0;

        // Process each transaction
        data.forEach(tx => {
            // Chart data
            labels.push(tx.date);
            amounts.push(tx.amount);
            balances.push(tx.balance);

            // Categorized expenses for bar chart
            if (categories[tx.category]) {
                categories[tx.category] += tx.amount;
            } else {
                categories[tx.category] = tx.amount;
            }

            // Transaction type pie chart data
            if (tx.transaction_type) {
                transactionTypes[tx.transaction_type] += tx.amount;
            }

            // Summarize income and expenses
            if (tx.transaction_type === 'Income') {
                totalIncome += tx.amount;
            } else if (tx.transaction_type === 'Expense') {
                totalExpenses += tx.amount;
            }
        });

        // Compute summaries
        netSavings = totalIncome - totalExpenses;
        currentBalance = balances.length ? balances[balances.length - 1] : 0;

        // Update overview cards
        currentBalanceEl.textContent = `$${currentBalance.toFixed(2)}`;
        totalIncomeEl.textContent = `$${totalIncome.toFixed(2)}`;
        totalExpensesEl.textContent = `$${totalExpenses.toFixed(2)}`;
        netSavingsEl.textContent = `$${netSavings.toFixed(2)}`;

        // --- Chart 1: Transaction Amounts Over Time (Line) ---
        const lineCtx = document.getElementById('transactionLineChart').getContext('2d');
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

        // --- Chart 2: Total Amount Spent by Category (Bar) ---
        const barCtx = document.getElementById('transactionBarChart').getContext('2d');
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

        // --- Chart 3: Distribution of Transaction Types (Pie) ---
        const pieCtx = document.getElementById('transactionPieChart').getContext('2d');
        new Chart(pieCtx, {
            type: 'pie',
            data: {
                labels: Object.keys(transactionTypes),
                datasets: [{
                    label: 'Transaction Types Distribution',
                    data: Object.values(transactionTypes),
                    backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Distribution of Transaction Types',
                        font: { size: 18 },
                        color: '#fff'
                    }
                }
            }
        });

        // --- Chart 4: Savings Trend Over Time (Line) ---
        const savingsCtx = document.getElementById('savingsTrendChart').getContext('2d');
        new Chart(savingsCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Balance Over Time',
                    data: balances,
                    borderColor: '#9966FF',
                    backgroundColor: 'rgba(153, 102, 255, 0.3)',
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Savings Trend Over Time',
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
    })
    .catch(error => console.error('Error fetching transactions:', error));
