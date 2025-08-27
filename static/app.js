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

function toggleAnswer() {
    const answerDisplay = document.getElementById('answer-display');
    const flipBtn = document.querySelector('.flip-btn');
    const inputForm = document.querySelector('.input-form');
    const hintBox = document.querySelector('.hint-box');
    
    // Call backend to mark flip was used
    fetch('/flip_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    
    // Show the answer and disable the flip button
    answerDisplay.style.display = 'block';
    flipBtn.textContent = '✅ Answer Revealed';
    flipBtn.classList.add('btn-secondary');
    flipBtn.classList.remove('btn-info');
    flipBtn.disabled = true;
    flipBtn.style.cursor = 'not-allowed';
    
    // Hide the input form and hint box using CSS classes
    if (inputForm) inputForm.classList.add('hidden');
    if (hintBox) hintBox.style.display = 'none';
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

