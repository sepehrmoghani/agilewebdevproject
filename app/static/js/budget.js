$(document).ready(function() {
    // Handle update goal button clicks
    $('.update-goal').on('click', function() {
        const goalId = $(this).data('goal-id');
        const goalName = $(this).data('goal-name');
        const goalCurrent = $(this).data('goal-current');
        const goalTarget = $(this).data('goal-target');
        
        $('#goal-id').val(goalId);
        $('#goal-name').val(goalName);
        $('#goal-current').val(goalCurrent);
        $('#goal-target').val(goalTarget);
    });
    
    // Handle saving goal updates
    $('#save-goal-update').on('click', function() {
        const goalId = $('#goal-id').val();
        const currentAmount = $('#goal-current').val();
        
        // Validate input
        if (!currentAmount || isNaN(currentAmount) || parseFloat(currentAmount) < 0) {
            alert('Please enter a valid amount');
            return;
        }
        
        // Send AJAX request to update goal
        $.ajax({
            url: `/update_goal/${goalId}`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                current_amount: currentAmount
            }),
            success: function(response) {
                if (response.success) {
                    // Close the modal
                    $('#updateGoalModal').modal('hide');
                    
                    // Reload the page to show updated data
                    location.reload();
                } else {
                    alert('Failed to update goal. Please try again.');
                }
            },
            error: function() {
                alert('An error occurred. Please try again.');
            }
        });
    });
    
    // Form validation
    $('.needs-validation').submit(function(event) {
        if (this.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
        }
        $(this).addClass('was-validated');
    });
    
    // Amount input formatting
    $('input[name="amount"], input[name="target_amount"], input[name="current_amount"]').on('input', function() {
        let value = $(this).val().replace(/[^\d.]/g, '');
        
        // Allow only one decimal point
        const decimalCount = (value.match(/\./g) || []).length;
        if (decimalCount > 1) {
            const firstDecimalIndex = value.indexOf('.');
            value = value.slice(0, firstDecimalIndex + 1) + value.slice(firstDecimalIndex + 1).replace(/\./g, '');
        }
        
        // Limit to 2 decimal places
        if (value.includes('.')) {
            const parts = value.split('.');
            if (parts[1].length > 2) {
                parts[1] = parts[1].slice(0, 2);
                value = parts.join('.');
            }
        }
        
        $(this).val(value);
    });
    
    // Date validation for target date
    $('#target_date').on('change', function() {
        const targetDate = new Date($(this).val());
        const today = new Date();
        
        if (targetDate <= today) {
            alert('Target date must be in the future');
            $(this).val('');
        }
    });
});
