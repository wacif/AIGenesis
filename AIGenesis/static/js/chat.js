// Enhanced Chat functionality for EcoSync Logistics
document.addEventListener('DOMContentLoaded', () => {
    // Main elements
    const chatForm = document.getElementById('chat-form');
    const userMessageInput = document.getElementById('user-message');
    const chatMessagesContainer = document.getElementById('chat-messages');
    const agentSelect = document.getElementById('agent-select');
    const clearChatButton = document.getElementById('clear-chat');
    const submitLogisticsButton = document.getElementById('submit-logistics');
    
    // Logistics form fields
    const fromLocationInput = document.getElementById('from-location');
    const toLocationInput = document.getElementById('to-location');
    const goodsTypeSelect = document.getElementById('goods-type');
    const deliveryDateInput = document.getElementById('delivery-date');
    
    // Set default date to today
    const today = new Date().toISOString().split('T')[0];
    deliveryDateInput.value = today;
    
    // Auto-resize textarea as user types
    userMessageInput.addEventListener('input', () => {
        userMessageInput.style.height = 'auto';
        userMessageInput.style.height = (userMessageInput.scrollHeight) + 'px';
    });

    // Allow Shift+Enter for new line, Enter to submit
    userMessageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
    
    // Format markdown-like syntax in messages
    function formatMessageContent(text) {
        // Handle code blocks with ```
        text = text.replace(/```([^`]+)```/g, '<pre><code>$1</code></pre>');
        
        // Handle inline code with `
        text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // Handle bold text with **
        text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        
        // Handle italic text with *
        text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');
        
        // Handle URLs
        text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
        
        // Handle newlines
        text = text.replace(/\n/g, '<br>');
        
        return text;
    }
    
    // Function to add a message to the chat window with enhanced formatting
    function addMessageToChat(content, sender, agentName = null) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender);
        
        let formattedContent = formatMessageContent(content);
        
        // Create message structure
        let messageHTML = '';
        
        if (sender === 'agent' && agentName) {
            messageHTML += `<div class="message-sender">${agentName}</div>`;
        }
        
        messageHTML += `<div class="message-content">${formattedContent}</div>`;
        
        // Add timestamp
        const now = new Date();
        const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        messageHTML += `<div class="message-time">${timeStr}</div>`;
        
        messageDiv.innerHTML = messageHTML;
        chatMessagesContainer.appendChild(messageDiv);
        
        // Scroll to the bottom
        scrollToBottom();
    }
    
    // Function to create a typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'agent', 'typing');
        
        typingDiv.innerHTML = `
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        
        chatMessagesContainer.appendChild(typingDiv);
        scrollToBottom();
        return typingDiv;
    }
    
    // Function to remove the typing indicator
    function removeTypingIndicator() {
        const typingIndicator = chatMessagesContainer.querySelector('.typing');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Function to scroll chat to bottom
    function scrollToBottom() {
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    }
    
    // Function to get agent name from selector
    function getSelectedAgentName() {
        return agentSelect.options[agentSelect.selectedIndex].text;
    }
    
    // Function to send a message to the server and get a response
    async function sendMessageToServer(message, agent) {
        try {
            // Show typing indicator
            const typingIndicator = showTypingIndicator();
            
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
            
            // Remove typing indicator
            removeTypingIndicator();
            
            const data = await response.json();
            
            if (response.ok) {
                // Add agent's response to the chat
                addMessageToChat(data.response, 'agent', getSelectedAgentName());
            } else {
                // Display error message
                addMessageToChat(`Error: ${data.error}`, 'system');
            }
        } catch (error) {
            removeTypingIndicator();
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
            
            // Clear input and reset height
            userMessageInput.value = '';
            userMessageInput.style.height = 'auto';
            
            // Get response from the selected agent
            sendMessageToServer(message, selectedAgent);
        }
    });
    
    // Handle logistics form submission
    submitLogisticsButton.addEventListener('click', () => {
        const from = fromLocationInput.value.trim();
        const to = toLocationInput.value.trim();
        const goods = goodsTypeSelect.value;
        const date = deliveryDateInput.value;
        
        if (!from || !to) {
            addMessageToChat("Please specify both 'From' and 'To' locations to get logistics information.", 'system');
            return;
        }
        
        // Create a structured message from the form data
        let formattedMessage = '';
        
        // Check what kind of agent is selected to format the message appropriately
        const selectedAgent = getSelectedAgentName();
        
        if (selectedAgent.includes('Logistics')) {
            if (goods) {
                formattedMessage = `I need to transport ${goods} from ${from} to ${to} by ${date}. What's the best route?`;
            } else {
                formattedMessage = `What's the best route from ${from} to ${to} for delivery on ${date}?`;
            }
        } else if (selectedAgent.includes('Forecasting')) {
            if (goods) {
                formattedMessage = `What's the demand forecast for ${goods} in ${to} based on current weather conditions?`;
            } else {
                formattedMessage = `What's the current weather in ${to} and how might it affect deliveries from ${from}?`;
            }
        } else {
            // Generic format for other agents
            formattedMessage = `From ${from} to ${to}, delivery of ${goods || 'goods'} scheduled for ${date}. Please provide logistics information.`;
        }
        
        // Add the formatted message to the chat as if the user typed it
        addMessageToChat(formattedMessage, 'user');
        
        // Send the message to the server
        sendMessageToServer(formattedMessage, agentSelect.value);
        
        // Optional: Clear form fields after submission
        // fromLocationInput.value = '';
        // toLocationInput.value = '';
        // goodsTypeSelect.selectedIndex = 0;
        // deliveryDateInput.value = today;
    });
    
    // Handle agent selector change
    agentSelect.addEventListener('change', () => {
        const selectedAgentName = getSelectedAgentName();
        
        // Show appropriate instructions based on the selected agent
        let welcomeMessage = '';
        
        if (selectedAgentName.includes('Logistics')) {
            welcomeMessage = `Switched to ${selectedAgentName}. You can now ask about routes, traffic conditions, and delivery options.`;
        } else if (selectedAgentName.includes('Forecasting')) {
            welcomeMessage = `Switched to ${selectedAgentName}. You can now ask about weather forecasts and product demand predictions.`;
        } else {
            welcomeMessage = `Switched to ${selectedAgentName}. How can I help you today?`;
        }
        
        addMessageToChat(welcomeMessage, 'system');
    });
    
    // Handle clear chat button
    clearChatButton.addEventListener('click', () => {
        // Keep only the first welcome message
        while (chatMessagesContainer.childElementCount > 1) {
            chatMessagesContainer.removeChild(chatMessagesContainer.lastChild);
        }
        
        // Add a system message about clearing the chat
        addMessageToChat('Chat history has been cleared.', 'system');
    });
    
    // Focus on input when page loads
    userMessageInput.focus();
});