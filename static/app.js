// FlashCard App JavaScript

function getHint() {
    fetch('/get_hint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(() => {
        location.reload();
    });
}

// Auto-focus input field
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('user_input');
    if (input) {
        input.focus();
    }
});

// Handle Enter key submission
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && e.target.id === 'user_input') {
        e.target.form.submit();
    }
});
