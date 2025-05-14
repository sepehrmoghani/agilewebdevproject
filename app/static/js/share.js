
function copyShareUrl() {
    var copyText = document.getElementById("shareUrl");
    copyText.select();
    document.execCommand("copy");
    alert("URL copied to clipboard!");
}

document.addEventListener('DOMContentLoaded', function() {
    const shareToggle = document.getElementById('shareToggle');
    if (shareToggle) {
        shareToggle.addEventListener('change', function(e) {
            fetch('/share/toggle_share', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                },
                body: JSON.stringify({
                    is_public: e.target.checked
                })
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    e.target.checked = !e.target.checked;
                }
            });
        });
    }
});
