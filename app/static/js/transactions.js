$(document).ready(function () {
    console.log("transactions.js loaded and DOM is ready");

    // Handle select all checkbox
    $("#select-all").change(function() {
        $(".transaction-checkbox").prop('checked', $(this).prop('checked'));
        updateDeleteButton();
    });

    // Handle individual checkboxes
    $(document).on('change', '.transaction-checkbox', function() {
        updateDeleteButton();
    });

    // Update delete button visibility
    function updateDeleteButton() {
        const checkedCount = $('.transaction-checkbox:checked').length;
        $('#delete-selected').toggle(checkedCount > 0);
    }

    // Handle bulk delete
    $("#delete-selected").click(function() {
        if (confirm('Are you sure you want to delete the selected transactions?')) {
            const selectedIds = $('.transaction-checkbox:checked').map(function() {
                return $(this).data('transaction-id');
            }).get();

            $.ajax({
                url: '/transactions/delete_multiple',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ transaction_ids: selectedIds }),
                headers: {
                    'X-CSRFToken': csrf_token
                },
                success: function(response) {
                    $("#select-all").prop('checked', false);
                    $(".transaction-checkbox").prop('checked', false);
                    updateDeleteButton();
                    location.reload();
                },
                error: function(error) {
                    console.error('Error deleting transactions:', error);
                    alert('Error deleting transactions');
                }
            });
        }
    });

    // Handle edit button click
    $(".edit-transaction").click(function () {
        const transactionId = $(this).data("transaction-id");
        $("#editTransactionId").val(transactionId);
        const row = $(this).closest("tr");

        const date = row.find("td:eq(1)").text().trim();
        const description = row.find("td:eq(2)").text().trim();
        const category = row.find("td:eq(3)").text().replace("Uncategorized", "").trim();
        const type = row.find("td:eq(4) span").text().trim().toLowerCase();
        const amount = row.find("td:eq(5)").text().trim().replace("$", "").trim();

        // Convert date from dd/mm/yyyy to yyyy-mm-dd for input field
        const [day, month, year] = date.split('/');
        const formattedDate = `${year}-${month}-${day}`;
        
        $("#editDate").val(formattedDate);
        $("#editDescription").val(description);
        $("#editCategory").val(category);
        $("#editType").val(type);
        $("#editAmount").val(amount);
    });

    // Handle save changes button click
    $("#saveEditTransaction").click(function () {
        const transactionId = $("#editTransactionId").val();
        const formData = {
            date: $("#editDate").val(),
            description: $("#editDescription").val(),
            amount: $("#editAmount").val(),
            category: $("#editCategory").val(),
            transaction_type: $("#editType").val(),
            csrf_token: csrf_token
        };

        $.ajax({
            url: `/transactions/edit/${transactionId}`,
            method: "POST",
            data: formData,
            success: function (response) {
                $("#editTransactionModal").modal("hide");
                location.reload();
            },
            error: function (error) {
                console.error("Error updating transaction:", error);
                alert("Error updating transaction");
            },
        });
    });

    // Initialize DataTables
    if ($('#transactions-table tbody tr').length && $('#transactions-table tbody td[colspan]').length === 0) {
        $('#transactions-table').DataTable({
            order: [[0, 'desc']],
            responsive: true,
            language: {
                search: "Search transactions:",
                lengthMenu: "Show _MENU_ entries",
                info: "Showing _START_ to _END_ of _TOTAL_ transactions",
                paginate: {
                    first: "First",
                    last: "Last",
                    next: "›",
                    previous: "‹",
                },
            },
            columnDefs: [
                { targets: 0, orderable: false },
                { targets: 1, type: "date" },
                { targets: 5, className: "text-end" },
                { targets: 6, className: "text-end" },
            ],
        });
        console.log("DataTable initialized");
    } else {
        console.log('Skipping DataTable initialization: table is empty');
    }


    // Show filename in custom file input
    $("input[type=file]").on("change", function () {
        const fileName = $(this).val().split("\\").pop();
        console.log("File selected:", fileName);
        $(this).next(".custom-file-label").html(fileName);
    });

    // Transaction type toggle
    $("#transaction_type").change(function () {
        const type = $(this).val();
        console.log("Transaction type selected:", type);
        if (type === "expense") {
            $(".amount-label").text("Expense Amount");
        } else if (type === "income") {
            $(".amount-label").text("Income Amount");
        } else {
            $(".amount-label").text("Transfer Amount");
        }
    });

    // Form validation
    $(".needs-validation").submit(function (event) {
        console.log("Form validation triggered");
        if (this.checkValidity() === false) {
            console.warn("Form is invalid");
            event.preventDefault();
            event.stopPropagation();
        }
        $(this).addClass("was-validated");
    });

    // Amount input formatting
    $('input[name="amount"]').on("input", function () {
        let value = $(this)
            .val()
            .replace(/[^\d.]/g, "");
        const decimalCount = (value.match(/\./g) || []).length;

        if (decimalCount > 1) {
            const firstDecimalIndex = value.indexOf(".");
            value =
                value.slice(0, firstDecimalIndex + 1) +
                value.slice(firstDecimalIndex + 1).replace(/\./g, "");
        }

        if (value.includes(".")) {
            const parts = value.split(".");
            if (parts[1].length > 2) {
                parts[1] = parts[1].slice(0, 2);
                value = parts.join(".");
            }
        }

        console.log("Formatted amount input:", value);
        $(this).val(value);
    });

    // Handle delete button click
    $(".delete-transaction").click(function () {
        const transactionId = $(this).data("transaction-id");
        console.log("Delete button clicked for transaction:", transactionId);

        if (confirm("Are you sure you want to delete this transaction?")) {
            $.ajax({
                url: `/transactions/delete/${transactionId}`,
                method: "DELETE",
                headers: {
                    "X-CSRFToken": csrf_token,
                },
                success: function (response) {
                    console.log("Delete success:", response);
                    if (response.success) {
                        location.reload();
                    }
                },
                error: function (error) {
                    console.error("Error deleting transaction:", error);
                    alert("Error deleting transaction");
                },
            });
        }
    });
});
