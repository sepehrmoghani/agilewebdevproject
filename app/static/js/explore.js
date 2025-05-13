document.addEventListener("DOMContentLoaded", function () {

    function getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    const likeButtons = document.querySelectorAll('.like-btn');
    const saveButtons = document.querySelectorAll('.save-btn');

    function toggleIcon(icon) {
        if (icon.getAttribute('data-prefix') === 'fas') {
            icon.setAttribute('data-prefix', 'far');
        } else {
            icon.setAttribute('data-prefix', 'fas');
        }
    }

    function sendAjax(url, callback) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(), 
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ toggle: true }) 
        })
        .then(response => response.json())
        .then(data => {
            if (callback) callback(data);
        })
        .catch(error => console.error('AJAX error:', error));
    }

    likeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const icon = button.querySelector('svg');
            const goalId = button.dataset.goalId;

            if (icon) {
                toggleIcon(icon);
                sendAjax(`/budgeting_and_goals/goal/${goalId}/like`, data => {
                    console.log('Like toggled:', data.liked);
                });
            }
        });
    });

    saveButtons.forEach(button => {
        button.addEventListener('click', function () {
            const icon = button.querySelector('svg');
            const goalId = button.dataset.goalId;
            
            if (icon) {
                toggleIcon(icon);
                sendAjax(`/budgeting_and_goals/goal/${goalId}/save`, data => {
                    console.log('Save toggled:', data.saved);
                });
            }
        });
    });
});
