$(document).ready(function() {
    var chatForm = $('#chat-form');
    var chatInput = $('#chat-input');
    var chatMessages = $('#chat-messages');

    chatForm.submit(function(event) {
        event.preventDefault();
        var message = chatInput.val();

        $.ajax({
            url: "{{ url_for('chat') }}",
            type: 'POST',
            data: { message: message },
            success: function(response) {
                console.log('Message sent successfully to server:', response.message);
                // Update chat box in HTML
                var newMessage = $('<p>').text(response.message);
                chatMessages.append(newMessage);
                chatInput.val(''); // Clear input field after sending message
                chatMessages.scrollTop(chatMessages[0].scrollHeight); // Scroll to the bottom
            },
            error: function(error) {
                console.error('Error sending message:', error);
            }
        });
    });
});