
fetch('/dashboard/api/transactions')
    .then(response => response.json())
    .then(data => {
        window.transactionsData = data; // Store data globally
        updateCharts();
    })
    .catch(error => console.error('Error fetching transactions:', error));

function updateCharts() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    
    let filteredData = window.transactionsData;
    if (startDate && endDate) {
        filteredData = window.transactionsData.filter(tx => {
            const txDate = new Date(tx.date);
            return txDate >= new Date(startDate) && txDate <= new Date(endDate);
        });
    }

    const totalIncomeEl = document.getElementById('totalIncome');
    const totalExpensesEl = document.getElementById('totalExpenses');
    const netSavingsEl = document.getElementById('netSavings');

    let expenseCategories = {};
    let incomeCategories = {};
    let totalIncome = 0, totalExpenses = 0;

    // Sort by date (oldest to newest)
    const sortedData = filteredData.slice().sort((a, b) => new Date(a.date) - new Date(b.date));
    
    let labels = [];
    let amounts = [];

    const formatDate = (dateStr) => {
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return new Date(dateStr).toLocaleDateString('en-US', options);
    };

    // Process each transaction
    sortedData.forEach(tx => {
        labels.push(formatDate(tx.date));
        
        if (tx.transaction_type.toLowerCase() === 'income') {
            incomeCategories[tx.category] = (incomeCategories[tx.category] || 0) + tx.amount;
            totalIncome += tx.amount;
            amounts.push(tx.amount);
        } else if (tx.transaction_type.toLowerCase() === 'expense') {
            expenseCategories[tx.category] = (expenseCategories[tx.category] || 0) + Math.abs(tx.amount);
            totalExpenses += Math.abs(tx.amount);
            amounts.push(-tx.amount);
        }
    });

    const netSavings = totalIncome - totalExpenses;
    totalIncomeEl.textContent = `$${totalIncome.toFixed(2)}`;
    totalExpensesEl.textContent = `$${totalExpenses.toFixed(2)}`;
    netSavingsEl.textContent = `$${netSavings.toFixed(2)}`;

    // Line Chart
    const lineCtx = document.getElementById('transactionLineChart')?.getContext('2d');
    if (lineCtx) {
        if (window.lineChart) window.lineChart.destroy();
        window.lineChart = new Chart(lineCtx, {
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

    // Expense Chart
    const expenseCtx = document.getElementById('expenseBarChart')?.getContext('2d');
    if (expenseCtx) {
        if (window.expenseChart) window.expenseChart.destroy();
        window.expenseChart = new Chart(expenseCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(expenseCategories),
                datasets: [{
                    label: 'Total Expenses by Category',
                    data: Object.values(expenseCategories),
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: '#ff6384',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Total Expenses by Category',
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

    // Income Chart
    const incomeCtx = document.getElementById('incomeBarChart')?.getContext('2d');
    if (incomeCtx) {
        if (window.incomeChart) window.incomeChart.destroy();
        window.incomeChart = new Chart(incomeCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(incomeCategories),
                datasets: [{
                    label: 'Total Income by Category',
                    data: Object.values(incomeCategories),
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: '#4bc0c0',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Total Income by Category',
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
}
