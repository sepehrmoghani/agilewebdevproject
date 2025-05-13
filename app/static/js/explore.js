document.addEventListener("DOMContentLoaded", function () {

    function getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    const likeButtons = document.querySelectorAll('.like-btn');
    const saveButtons = document.querySelectorAll('.save-btn');


    function toggleIconAndCount(button) {
        const icon = button.querySelector('svg');
        const countSpan = button.querySelector('span');

        let count = parseInt(countSpan.textContent) || 0;

        if (icon.getAttribute('data-prefix') === 'fas') {
            icon.setAttribute('data-prefix', 'far');
            count = Math.max(0, count - 1);
        } else {
            icon.setAttribute('data-prefix', 'fas');
            count += 1;
        }

        countSpan.textContent = count;
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
                toggleIconAndCount(button); 
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
                toggleIconAndCount(button); 
                sendAjax(`/budgeting_and_goals/goal/${goalId}/save`, data => {
                    console.log('Save toggled:', data.saved);
                });
            }
        });
    });
});
