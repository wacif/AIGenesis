// Enhanced Chat functionality for EcoSync Logistics
document.addEventListener('DOMContentLoaded', () => {
    // Main elements
    const chatForm = document.getElementById('chat-form');
    const userMessageInput = document.getElementById('user-message');
    const chatMessagesContainer = document.getElementById('chat-messages');
    const agentSelect = document.getElementById('agent-select');
    const clearChatButton = document.getElementById('clear-chat');
    const submitLogisticsButton = document.getElementById('submit-logistics');
    const clearFormButton = document.getElementById('clear-form');
    const logisticsForm = document.getElementById('logistics-form');
    const toggleFormButton = document.getElementById('toggle-form-button');
    const historyPanel = document.getElementById('history-panel');
    const toggleHistoryButton = document.getElementById('toggle-history');
    const refreshButton = document.getElementById('refresh-button');
    const exportButton = document.getElementById('export-button');
    
    // Logistics form fields
    const fromLocationInput = document.getElementById('from-location');
    const toLocationInput = document.getElementById('to-location');
    const goodsTypeSelect = document.getElementById('goods-type');
    const deliveryDateInput = document.getElementById('delivery-date');
    
    // Form labels that will change based on agent
    const fromLabel = document.querySelector('label[for="from-location"]');
    const toLabel = document.querySelector('label[for="to-location"]');
    const goodsTypeLabel = document.querySelector('label[for="goods-type"]');
    
    // Chat history storage
    let chatHistory = [];
    
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
        
        // Handle bullet points
        text = text.replace(/^[*•-] (.+)$/gm, '<li>$1</li>');
        text = text.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
        
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
        
        // Store in chat history
        chatHistory.push({
            role: sender === 'user' ? 'user' : 'assistant',
            content: content,
            agentName: agentName,
            timestamp: now.toISOString()
        });
        
        // Update history panel if visible
        if (historyPanel.classList.contains('visible')) {
            updateHistoryPanel();
        }
        
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
    
    // Function to update history panel
    function updateHistoryPanel() {
        // Clear current history panel
        historyPanel.innerHTML = '';
        
        // Add header
        const header = document.createElement('div');
        header.classList.add('history-header');
        header.innerHTML = '<h3><i class="fas fa-history"></i> Chat History</h3>';
        historyPanel.appendChild(header);
        
        // Group messages by day
        const messagesByDay = {};
        
        chatHistory.forEach(msg => {
            const date = new Date(msg.timestamp);
            const dateKey = date.toLocaleDateString();
            
            if (!messagesByDay[dateKey]) {
                messagesByDay[dateKey] = [];
            }
            
            messagesByDay[dateKey].push(msg);
        });
        
        // Create sections for each day
        for (const [day, messages] of Object.entries(messagesByDay)) {
            const daySection = document.createElement('div');
            daySection.classList.add('history-day');
            
            const dayHeader = document.createElement('div');
            dayHeader.classList.add('history-day-header');
            dayHeader.textContent = day;
            daySection.appendChild(dayHeader);
            
            // Add message summaries
            messages.forEach(msg => {
                const msgItem = document.createElement('div');
                msgItem.classList.add('history-message');
                msgItem.classList.add(msg.role === 'user' ? 'user' : 'agent');
                
                // Truncate long messages
                let content = msg.content;
                if (content.length > 30) {
                    content = content.substring(0, 30) + '...';
                }
                
                const time = new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                
                msgItem.innerHTML = `
                    <div class="history-message-time">${time}</div>
                    <div class="history-message-content">${content}</div>
                `;
                
                daySection.appendChild(msgItem);
            });
            
            historyPanel.appendChild(daySection);
        }
    }
    
    // Function to update form labels and placeholders based on selected agent
    function updateFormForAgent(agentName) {
        const logisticsFormTitle = document.querySelector('.logistics-form-title');
        
        if (agentName.includes('Weather') || agentName.includes('Forecasting')) {
            // Update for Weather/Forecasting agent
            fromLabel.innerHTML = '<i class="fas fa-box-open"></i> Product:';
            fromLocationInput.placeholder = 'Product name (e.g., Umbrellas)';
            
            toLabel.innerHTML = '<i class="fas fa-city"></i> Location:';
            toLocationInput.placeholder = 'City name (e.g., Lahore)';
            
            goodsTypeLabel.innerHTML = '<i class="fas fa-search"></i> Query Type:';
            
            // Clear and rebuild options for goods type select
            goodsTypeSelect.innerHTML = '';
            const forecastOptions = [
                {value: '', text: 'Select query type...'},
                {value: 'Weather', text: 'Current Weather'},
                {value: 'Demand', text: 'Product Demand'},
                {value: 'Supply', text: 'Supply Chain Impact'}
            ];
            
            forecastOptions.forEach(option => {
                const optElement = document.createElement('option');
                optElement.value = option.value;
                optElement.textContent = option.text;
                goodsTypeSelect.appendChild(optElement);
            });
            
            logisticsFormTitle.innerHTML = '<i class="fas fa-cloud-sun"></i> Weather & Demand Query';
            submitLogisticsButton.innerHTML = '<i class="fas fa-search"></i> Get Weather & Demand Info';
            
        } else if (agentName.includes('Routing') || agentName.includes('Traffic')) {
            // Update for Routing/Traffic agent
            fromLabel.innerHTML = '<i class="fas fa-map-marker-alt"></i> From:';
            fromLocationInput.placeholder = 'Origin city (e.g., Lahore)';
            
            toLabel.innerHTML = '<i class="fas fa-map-pin"></i> To:';
            toLocationInput.placeholder = 'Destination city (e.g., Karachi)';
            
            goodsTypeLabel.innerHTML = '<i class="fas fa-truck"></i> Transport Type:';
            
            // Clear and rebuild options for goods type select
            goodsTypeSelect.innerHTML = '';
            const routingOptions = [
                {value: '', text: 'Select transport type...'},
                {value: 'Car', text: 'Car/Personal Vehicle'},
                {value: 'Truck', text: 'Commercial Truck'},
                {value: 'Cargo', text: 'Cargo Delivery'},
                {value: 'Emergency', text: 'Emergency Vehicle'}
            ];
            
            routingOptions.forEach(option => {
                const optElement = document.createElement('option');
                optElement.value = option.value;
                optElement.textContent = option.text;
                goodsTypeSelect.appendChild(optElement);
            });
            
            logisticsFormTitle.innerHTML = '<i class="fas fa-route"></i> Route Planning Query';
            submitLogisticsButton.innerHTML = '<i class="fas fa-map-marked-alt"></i> Get Route & Traffic Info';
            
        } else {
            // Default form (Triage or other agents)
            fromLabel.innerHTML = '<i class="fas fa-map-marker-alt"></i> From:';
            fromLocationInput.placeholder = 'Origin city (e.g., Lahore)';
            
            toLabel.innerHTML = '<i class="fas fa-map-pin"></i> To:';
            toLocationInput.placeholder = 'Destination city (e.g., Karachi)';
            
            goodsTypeLabel.innerHTML = '<i class="fas fa-box"></i> Kind of Goods:';
            
            // Clear and rebuild options for goods type select
            goodsTypeSelect.innerHTML = '';
            const defaultOptions = [
                {value: '', text: 'Select goods type...'},
                {value: 'Clothing', text: 'Clothing'},
                {value: 'Electronics', text: 'Electronics'},
                {value: 'Food', text: 'Food'},
                {value: 'Furniture', text: 'Furniture'},
                {value: 'Medicine', text: 'Medicine'},
                {value: 'Weather Equipment', text: 'Weather Equipment'},
                {value: 'Other', text: 'Other'}
            ];
            
            defaultOptions.forEach(option => {
                const optElement = document.createElement('option');
                optElement.value = option.value;
                optElement.textContent = option.text;
                goodsTypeSelect.appendChild(optElement);
            });
            
            logisticsFormTitle.innerHTML = '<i class="fas fa-truck"></i> Logistics Request Form';
            submitLogisticsButton.innerHTML = '<i class="fas fa-search"></i> Get Logistics Information';
        }
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
    
    // Function to export chat history to a text file
    function exportChatHistory() {
        // Create a formatted string of the chat history
        let exportText = "EcoSync Logistics - Chat Export\n";
        exportText += "==============================\n\n";
        exportText += `Date: ${new Date().toLocaleDateString()}\n\n`;
        
        chatHistory.forEach(msg => {
            const time = new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            const role = msg.role === 'user' ? 'You' : (msg.agentName || 'Agent');
            exportText += `[${time}] ${role}:\n${msg.content}\n\n`;
        });
        
        // Create a blob and download it
        const blob = new Blob([exportText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ecosync-chat-export-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    // Function to toggle the form visibility
    function toggleFormVisibility() {
        logisticsForm.classList.toggle('collapsed');
        toggleFormButton.classList.toggle('active');
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
            addMessageToChat("Please fill in both required fields to get information.", 'system');
            return;
        }
        
        // Create a structured message from the form data
        let formattedMessage = '';
        
        // Check what kind of agent is selected to format the message appropriately
        const selectedAgentName = getSelectedAgentName();
        
        if (selectedAgentName.includes('Weather') || selectedAgentName.includes('Forecasting')) {
            if (goods === 'Weather') {
                formattedMessage = `What's the current weather in ${to}?`;
            } else if (goods === 'Demand') {
                formattedMessage = `What's the demand forecast for ${from} in ${to} based on current weather conditions?`;
            } else if (goods === 'Supply') {
                formattedMessage = `How will the current weather affect the supply chain for ${from} in ${to}?`;
            } else {
                formattedMessage = `What's the weather in ${to} and how might it affect ${from} products?`;
            }
        } else if (selectedAgentName.includes('Routing') || selectedAgentName.includes('Traffic')) {
            if (goods) {
                formattedMessage = `I need to travel from ${from} to ${to} by ${goods} on ${date}. What's the best route and current traffic conditions?`;
            } else {
                formattedMessage = `What's the best route from ${from} to ${to} for travel on ${date}? Any traffic issues I should know about?`;
            }
        } else {
            // Generic format for other agents including the triage agent
            if (goods) {
                formattedMessage = `I need to transport ${goods} from ${from} to ${to} by ${date}. What's the best route and are there any weather concerns?`;
            } else {
                formattedMessage = `What's the logistics information for a trip from ${from} to ${to} on ${date}?`;
            }
        }
        
        // Add the formatted message to the chat as if the user typed it
        addMessageToChat(formattedMessage, 'user');
        
        // Send the message to the server
        sendMessageToServer(formattedMessage, agentSelect.value);
    });
    
    // Handle agent selector change
    agentSelect.addEventListener('change', () => {
        const selectedAgentName = getSelectedAgentName();
        
        // Update form for the selected agent
        updateFormForAgent(selectedAgentName);
        
        // Show appropriate instructions based on the selected agent
        let welcomeMessage = '';
        
        if (selectedAgentName.includes('Weather') || selectedAgentName.includes('Forecasting')) {
            welcomeMessage = `Switched to ${selectedAgentName}. You can now ask directly about weather conditions and product demand forecasts.`;
        } else if (selectedAgentName.includes('Routing') || selectedAgentName.includes('Traffic')) {
            welcomeMessage = `Switched to ${selectedAgentName}. You can now ask directly about routes, traffic conditions, and travel disruptions.`;
        } else if (selectedAgentName.includes('EcoSync Logistics')) {
            welcomeMessage = `Switched to ${selectedAgentName}. This is our main agent that will route your questions to the appropriate specialized agent based on your query.`;
        } else {
            welcomeMessage = `Switched to ${selectedAgentName}. How can I help you today?`;
        }
        
        addMessageToChat(welcomeMessage, 'system');
        
        // Reset form fields
        fromLocationInput.value = '';
        toLocationInput.value = '';
        goodsTypeSelect.selectedIndex = 0;
        deliveryDateInput.value = today;
    });
    
    // Handle clear chat button
    clearChatButton.addEventListener('click', () => {
        // Keep only the first welcome message
        while (chatMessagesContainer.childElementCount > 1) {
            chatMessagesContainer.removeChild(chatMessagesContainer.lastChild);
        }
        
        // Clear chat history array (except welcome message)
        chatHistory = chatHistory.slice(0, 1);
        
        // Add a system message about clearing the chat
        addMessageToChat('Chat history has been cleared.', 'system');
    });
    
    // Handle clear form button
    clearFormButton.addEventListener('click', () => {
        fromLocationInput.value = '';
        toLocationInput.value = '';
        goodsTypeSelect.selectedIndex = 0;
        deliveryDateInput.value = today;
    });
    
    // Handle toggle history button
    toggleHistoryButton.addEventListener('click', () => {
        historyPanel.classList.toggle('visible');
        toggleHistoryButton.classList.toggle('active');
        updateHistoryPanel();
    });
    
    // Handle toggle form button
    toggleFormButton.addEventListener('click', toggleFormVisibility);
    
    // Handle refresh button
    refreshButton.addEventListener('click', () => {
        const refreshMessage = "Refreshing data...";
        addMessageToChat(refreshMessage, 'system');
        
        // Simulate refresh action
        setTimeout(() => {
            addMessageToChat("All data has been refreshed with the latest information.", 'system');
        }, 1000);
    });
    
    // Handle export button
    exportButton.addEventListener('click', exportChatHistory);
    
    // Initialize form based on the default selected agent
    updateFormForAgent(getSelectedAgentName());
    
    // Focus on input when page loads
    userMessageInput.focus();
});