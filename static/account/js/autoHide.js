// Auto-hide messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.message');
    messages.forEach(function(message, index) {
        setTimeout(function() {
            message.classList.add('fade-out');
            setTimeout(function() {
                message.style.display = 'none';
            }, 300);
        }, 5000 + (index * 500)); // Stagger the hiding
    });
});

// Function to manually close messages
function closeMessage(messageId) {
    const message = document.getElementById(messageId);
    if (message) {
        message.classList.add('fade-out');
        setTimeout(function() {
            message.style.display = 'none';
        }, 300);
    }
}