$(document).ready(function() {
    // Handle edit button click
    $('.edit-transaction').click(function() {
        const transactionId = $(this).data('transaction-id');
        $('#editTransactionId').val(transactionId);
        
        // Get the current row data
        const row = $(this).closest('tr');
        $('#editDate').val(row.find('td:eq(0)').text().trim());
        $('#editDescription').val(row.find('td:eq(1)').text().trim());
        $('#editCategory').val(row.find('td:eq(2)').text().replace('Uncategorized', '').trim());
        const type = row.find('td:eq(3) span').text().trim().toLowerCase();
        $('#editType').val(type);
        $('#editAmount').val(row.find('td:eq(4)').text().trim().replace('$', '').trim());
    });

    // Handle save changes button click
    $('#saveEditTransaction').click(function() {
        const transactionId = $('#editTransactionId').val();
        const formData = {
            date: $('#editDate').val(),
            description: $('#editDescription').val(),
            amount: $('#editAmount').val(),
            category: $('#editCategory').val(),
            transaction_type: $('#editType').val()
        };

        // Send AJAX request to update transaction
        $.ajax({
            url: `/transactions/edit/${transactionId}`,
            method: 'POST',
            data: formData,
            success: function(response) {
                $('#editTransactionModal').modal('hide');
                location.reload(); // Reload to show updated data
            },
            error: function(error) {
                alert('Error updating transaction');
            }
        });
    });
    // Initialize DataTables
    $('#transactions-table').DataTable({
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
    $('input[name="amount"]').on('input', function() {
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

    // Handle delete button click
    $('.delete-transaction').click(function() {
        const transactionId = $(this).data('transaction-id');
        if (confirm('Are you sure you want to delete this transaction?')) {
            $.ajax({
                url: `/transactions/delete/${transactionId}`,
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrf_token
                },
                success: function(response) {
                    if (response.success) {
                        location.reload();
                    }
                },
                error: function(error) {
                    alert('Error deleting transaction');
                }
            });
        }
    });
});
