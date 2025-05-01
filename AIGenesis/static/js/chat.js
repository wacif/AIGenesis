// Chat functionality for AIGenesis
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userMessageInput = document.getElementById('user-message');
    const chatMessagesContainer = document.getElementById('chat-messages');
    const agentSelect = document.getElementById('agent-select');
    
    // Function to add a message to the chat window
    function addMessageToChat(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        
        // Add class based on sender (user, agent, system)
        messageDiv.classList.add(sender);
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.textContent = content;
        
        messageDiv.appendChild(messageContent);
        chatMessagesContainer.appendChild(messageDiv);
        
        // Scroll to the bottom
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    }
    
    // Function to send a message to the server and get a response
    async function sendMessageToServer(message, agent) {
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    agent: agent
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Add agent's response to the chat
                addMessageToChat(data.response, 'agent');
            } else {
                // Display error message
                addMessageToChat(`Error: ${data.error}`, 'system');
            }
        } catch (error) {
            addMessageToChat(`Network error: ${error.message}`, 'system');
        }
    }
    
    // Handle form submission
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const message = userMessageInput.value.trim();
        const selectedAgent = agentSelect.value;
        
        if (message) {
            // Add user message to chat
            addMessageToChat(message, 'user');
            
            // Clear input
            userMessageInput.value = '';
            
            // Get response from the selected agent
            sendMessageToServer(message, selectedAgent);
        }
    });
    
    // Focus on input when page loads
    userMessageInput.focus();
});