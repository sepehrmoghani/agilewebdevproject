$(document).ready(function() {
    // Default period
    let currentPeriod = 'monthly';
    
    // Initialize the dashboard
    loadDashboardData(currentPeriod);
    
    // Period selector buttons
    $('.btn-group .btn').on('click', function() {
        // Change active button
        $('.btn-group .btn').removeClass('active');
        $(this).addClass('active');
        
        // Get selected period
        currentPeriod = $(this).data('period');
        
        // Reload dashboard data
        loadDashboardData(currentPeriod);
    });
    
    // Function to load all dashboard data
    function loadDashboardData(period) {
        loadSpendingByCategory(period);
        loadDailySpending();
        loadBudgetStatus();
    }
    
    // Load spending by category chart
    function loadSpendingByCategory(period) {
        $.ajax({
            url: `/get_spending_data?period=${period}`,
            type: 'GET',
            success: function(data) {
                renderCategoryChart(data);
                updateSummaryCards(data);
            },
            error: function() {
                console.error('Failed to load category spending data');
            }
        });
    }
    
    // Render the category spending chart
    function renderCategoryChart(data) {
        const ctx = document.getElementById('category-chart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (window.categoryChart) {
            window.categoryChart.destroy();
        }
        
        window.categoryChart = new Chart(ctx, {
            type: 'pie',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#e9ecef'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                return `${label}: ${formatCurrency(value)}`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Load daily spending chart
    function loadDailySpending() {
        $.ajax({
            url: '/get_daily_spending',
            type: 'GET',
            success: function(data) {
                renderDailyChart(data);
            },
            error: function() {
                console.error('Failed to load daily spending data');
            }
        });
    }
    
    // Render the daily spending chart
    function renderDailyChart(data) {
        const ctx = document.getElementById('daily-chart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (window.dailyChart) {
            window.dailyChart.destroy();
        }
        
        // Format dates for display
        const formattedLabels = data.labels.map(dateStr => {
            const date = new Date(dateStr);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });
        
        window.dailyChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: formattedLabels,
                datasets: data.datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value;
                            },
                            color: '#e9ecef'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#e9ecef'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.dataset.label || '';
                                const value = context.raw || 0;
                                return `${label}: ${formatCurrency(value)}`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Update summary cards with calculated values
    function updateSummaryCards(data) {
        // Calculate total income, expenses and savings
        let totalExpenses = 0;
        
        if (data.datasets && data.datasets.length > 0) {
            data.datasets[0].data.forEach(amount => {
                totalExpenses += amount;
            });
        }
        
        // Get all transactions for income calculation
        $.ajax({
            url: '/get_transactions_data',
            type: 'GET',
            success: function(transactions) {
                // Calculate income for current period
                let totalIncome = 0;
                let startDate = getStartDateForPeriod(currentPeriod);
                
                transactions.forEach(transaction => {
                    const transDate = new Date(transaction.date);
                    if (transDate >= startDate && transaction.transaction_type === 'income') {
                        totalIncome += transaction.amount;
                    }
                });
                
                // Calculate net savings
                const netSavings = totalIncome - totalExpenses;
                
                // Update the UI
                $('#total-income').text(formatCurrency(totalIncome));
                $('#total-expenses').text(formatCurrency(totalExpenses));
                $('#net-savings').text(formatCurrency(netSavings));
                
                // Add color indicators
                if (netSavings >= 0) {
                    $('#net-savings').removeClass('text-danger').addClass('text-success');
                } else {
                    $('#net-savings').removeClass('text-success').addClass('text-danger');
                }
            },
            error: function() {
                console.error('Failed to load transaction data');
            }
        });
    }
    
    // Get start date based on period
    function getStartDateForPeriod(period) {
        const today = new Date();
        let startDate;
        
        if (period === 'daily') {
            startDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());
        } else if (period === 'weekly') {
            startDate = new Date(today);
            startDate.setDate(today.getDate() - today.getDay()); // Start of current week (Sunday)
        } else if (period === 'monthly') {
            startDate = new Date(today.getFullYear(), today.getMonth(), 1); // Start of current month
        } else {
            startDate = new Date(today.getFullYear(), today.getMonth(), 1); // Default to monthly
        }
        
        return startDate;
    }
    
    // Load budget status
    function loadBudgetStatus() {
        $.ajax({
            url: '/get_budget_status',
            type: 'GET',
            success: function(data) {
                renderBudgetStatus(data);
            },
            error: function() {
                console.error('Failed to load budget status data');
                $('#budget-loading').hide();
                $('#budget-list').removeClass('d-none').html(
                    `<div class="alert alert-danger">Failed to load budget data. Please try again.</div>`
                );
            }
        });
    }
    
    // Render budget status
    function renderBudgetStatus(budgets) {
        $('#budget-loading').hide();
        
        if (budgets.length === 0) {
            $('#budget-list').removeClass('d-none').html(
                `<div class="text-center py-4">
                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-muted mb-2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    <h5>No Budgets Created</h5>
                    <p class="text-muted">Create budgets to track your spending against limits</p>
                    <a href="/budget" class="btn btn-primary btn-sm">Create Budget</a>
                </div>`
            );
            return;
        }
        
        let budgetHTML = '';
        
        budgets.forEach(budget => {
            let statusClass = '';
            if (budget.percent_spent > 90) {
                statusClass = 'bg-danger';
            } else if (budget.percent_spent > 70) {
                statusClass = 'bg-warning';
            } else {
                statusClass = 'bg-success';
            }
            
            budgetHTML += `
                <div class="mb-3">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                        <span>${budget.category}</span>
                        <span class="small text-muted">${budget.period.charAt(0).toUpperCase() + budget.period.slice(1)}</span>
                    </div>
                    <div class="progress" style="height: 10px;">
                        <div class="progress-bar ${statusClass}" role="progressbar" 
                             style="width: ${budget.percent_spent}%" 
                             aria-valuenow="${budget.percent_spent}" 
                             aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                    <div class="d-flex justify-content-between align-items-center mt-1">
                        <small>Spent: ${formatCurrency(budget.spent)}</small>
                        <small>Budget: ${formatCurrency(budget.amount)}</small>
                    </div>
                </div>
            `;
        });
        
        $('#budget-list').removeClass('d-none').html(budgetHTML);
    }
    
    // Format currency
    function formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }
});
