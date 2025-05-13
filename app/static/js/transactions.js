$(document).ready(function() {

    console.log('Transactions page loaded');
    // Initialize DataTables
    const transactionsTable = $('#transactions-table').DataTable({
        order: [[0, 'desc']], // Sort by date descending
        responsive: true,
        language: {
            search: 'Search transactions:',
            lengthMenu: 'Show _MENU_ entries',
            info: 'Showing _START_ to _END_ of _TOTAL_ transactions',
            paginate: {
                first: 'First',
                last: 'Last',
                next: '›',
                previous: '‹'
            }
        },
        columnDefs: [
            { targets: 0, type: 'date' }, // Date column
            { targets: 4, className: 'text-end' }, // Amount column
            { targets: 5, className: 'text-end' }  // Balance column
        ]
    });
0
    // Show filename in custom file input
    $('input[type=file]').on('change', function() {
        const fileName = $(this).val().split('\\').pop();
        $(this).next('.custom-file-label').html(fileName);
    });

    // Transaction type toggle
    $('#transaction_type').change(function() {
        const type = $(this).val();
        if (type === 'expense') {
            $('.amount-label').text('Expense Amount');
        } else if (type === 'income') {
            $('.amount-label').text('Income Amount');
        } else {
            $('.amount-label').text('Transfer Amount');
        }
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
    $('input[name="amount"], #edit-amount').on('input', function() {
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
    
    // Handle clicking the edit button for a transaction
    $('.edit-transaction').on('click', function() {
        const transactionId = $(this).data('transaction-id');
        
        // Clear previous messages
        $('#edit-transaction-error').addClass('d-none').text('');
        $('#edit-transaction-success').addClass('d-none').text('');
        
        // Fetch transaction data
        $.ajax({
            url: `/transaction/${transactionId}`,
            method: 'GET',
            success: function(data) {
                // Populate form with transaction data
                $('#edit-transaction-id').val(data.id);
                $('#edit-date').val(data.date);
                $('#edit-description').val(data.description);
                $('#edit-amount').val(data.amount);
                $('#edit-category').val(data.category);
                $('#edit-transaction-type').val(data.transaction_type);
            },
            error: function(xhr) {
                let errorMessage = 'Failed to fetch transaction data';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }
                $('#edit-transaction-error').removeClass('d-none').text(errorMessage);
            }
        });
    });
    
    // Handle saving edited transaction
    $('#save-transaction').on('click', function() {
        // Validate form
        const form = document.getElementById('edit-transaction-form');
        if (!form.checkValidity()) {
            $(form).addClass('was-validated');
            return;
        }
        
        // Get transaction ID and form data
        const transactionId = $('#edit-transaction-id').val();
        const formData = new FormData();
        
        formData.append('date', $('#edit-date').val());
        formData.append('description', $('#edit-description').val());
        formData.append('amount', $('#edit-amount').val());
        formData.append('category', $('#edit-category').val());
        formData.append('transaction_type', $('#edit-transaction-type').val());
        
        // Clear previous messages
        $('#edit-transaction-error').addClass('d-none').text('');
        $('#edit-transaction-success').addClass('d-none').text('');
        
        // Send updated data to server
        $.ajax({
            url: `/transaction/${transactionId}`,
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Show success message
                $('#edit-transaction-success').removeClass('d-none').text(response.message);
                
                // After 1 second, reload the page to reflect the updated transaction
                setTimeout(function() {
                    window.location.reload();
                }, 1000);
            },
            error: function(xhr) {
                let errorMessage = 'Failed to update transaction';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }
                $('#edit-transaction-error').removeClass('d-none').text(errorMessage);
            }
        });
    });
    
    // Reset validation when modal is hidden
    $('#editTransactionModal').on('hidden.bs.modal', function() {
        const form = document.getElementById('edit-transaction-form');
        $(form).removeClass('was-validated');
    });
});
