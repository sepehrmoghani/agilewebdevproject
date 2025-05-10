$(document).ready(function() {
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
});
