document.addEventListener('DOMContentLoaded', () => {
    // Input Auto-resize
    const msgInput = document.getElementById('message-input');
    if (msgInput) {
        msgInput.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        msgInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }

    // Scroll chat to bottom on load
    scrollToBottom(false);
    setupFeatureInteractions();
});

// ... (existing code) ...

function addMessage(text, sender) {
    const container = document.getElementById('chat-messages');
    const isUser = sender === 'user';

    const div = document.createElement('div');
    div.className = `flex w-full mb-6 ${isUser ? 'justify-end' : 'justify-start'} animate-fade-in`;

    const userBubble = `bg-white text-gray-800 rounded-2xl rounded-tr-sm shadow-sm border border-gray-200`;
    const aiBubble = `bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-2xl rounded-tl-sm shadow-md border border-blue-500/20`;

    const content = `
        <div class="max-w-[75%] ${isUser ? userBubble : aiBubble} p-4 relative group">
            <p class="text-sm leading-relaxed">${text}</p>
            <span class="text-[10px] absolute -bottom-5 ${isUser ? 'right-0 text-gray-400' : 'left-0 text-gray-400'} opacity-0 group-hover:opacity-100 transition-opacity">
                ${getCurrentTime()}
            </span>
        </div>
    `;

    div.innerHTML = content;
    container.appendChild(div);
    scrollToBottom(true);
}

function showTypingIndicator() {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.id = 'typing-indicator';
    div.className = 'flex w-full mb-6 justify-start animate-fade-in';
    div.innerHTML = `
        <div class="bg-white border border-gray-100 p-3 rounded-2xl rounded-tl-sm shadow-sm flex items-center space-x-1">
            <div class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce"></div>
            <div class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            <div class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
        </div>
    `;
    container.appendChild(div);
    scrollToBottom(true);
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
}

async function sendMessage() {
    const input = document.getElementById('message-input');
    const text = input.value.trim();
    if (!text) return;

    // Clear input
    input.value = '';
    input.style.height = 'auto';

    // Add User Message
    addMessage(text, 'user');

    // Show Typing
    showTypingIndicator();

    try {
        const model = document.getElementById('model-selector')?.value || 'gemma-it';

        let apiUrl = '/api/chat'; // Default for Flask/FastAPI
        // Django's URL might be different if not configured the same, but we made it /api/chat

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Django specific, harmless elsewhere usually
            },
            body: JSON.stringify({
                text,
                model,
                session_id: 1,
                coords: [19.0760, 72.8777]
            })
        });

        const data = await response.json();
        removeTypingIndicator();

        if (data.reply) {
            addMessage(data.reply, 'ai');
        } else {
            addMessage("Error: No reply received.", "ai");
        }
    } catch (err) {
        removeTypingIndicator();
        console.error(err);
        addMessage("Sorry, I couldn't reach the server. Is it running?", "ai");
    }
}

// Helper for Django CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



function getCurrentTime() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Interactive Features
function setupFeatureInteractions() {
    // 1. New Chat Button
    const buttons = document.querySelectorAll('button');
    buttons.forEach(btn => {
        if (btn.textContent.includes('New Chat')) {
            btn.addEventListener('click', () => {
                document.getElementById('chat-messages').innerHTML = `
                    <div class="flex w-full mb-6 justify-start animate-fade-in">
                        <div class="max-w-[75%] bg-gradient-to-br from-blue-600 to-blue-700 text-white p-4 rounded-2xl rounded-tl-sm shadow-md relative group">
                            <p class="text-sm leading-relaxed">Session reset. How can I help you now?</p>
                            <span class="text-[10px] absolute -bottom-5 left-0 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity">Just now</span>
                        </div>
                    </div>
                `;
            });
        }

        // 2. Voice & Video Call Simulation
        const title = btn.getAttribute('title');
        if (title === 'Voice Call') {
            btn.addEventListener('click', () => {
                alert("Requesting microphone permission...\n(This is a simulation)");
                addMessage("📞 Starting secure voice call...", "ai");
                setTimeout(() => addMessage("Call ended. Duration: 0:00", "ai"), 3000);
            });
        }
        if (title === 'Video Call') {
            btn.addEventListener('click', () => {
                alert("Requesting camera permission... \n(This is a simulation)");
                addMessage("📹 Starting secure video call...", "ai");
                setTimeout(() => addMessage("Call ended. Duration: 0:00", "ai"), 3000);
            });
        }
    });

    // 3. Attachments (Paperclip/Image inside input area)
    const icons = document.querySelectorAll('.fa-paperclip, .fa-image');
    icons.forEach(icon => {
        icon.parentElement.addEventListener('click', () => {
            // Create hidden file input
            const input = document.createElement('input');
            input.type = 'file';
            input.onchange = e => {
                const file = e.target.files[0];
                if (file) {
                    addMessage(`📎 Uploaded: ${file.name}`, 'user');
                    setTimeout(() => addMessage("I've received your file. Analyzing...", "ai"), 1000);
                }
            };
            input.click();
        });
    });

    // 4. Microphone
    const micIcon = document.querySelector('.fa-microphone');
    if (micIcon) {
        micIcon.parentElement.addEventListener('click', () => {
            micIcon.classList.toggle('text-red-500');
            micIcon.classList.toggle('text-red-700');
            micIcon.parentElement.classList.toggle('animate-pulse');

            if (micIcon.parentElement.classList.contains('animate-pulse')) {
                // Recording started
            } else {
                // Recording stopped
                addMessage("🎤 Voice message (0:05)", "user");
                setTimeout(() => addMessage("I heard you. Processing...", "ai"), 1000);
            }
        });
    }

    // 5. History Items
    const historyItems = document.querySelectorAll('#left-sidebar .group');
    historyItems.forEach(item => {
        item.addEventListener('click', () => {
            const title = item.querySelector('span.font-medium').textContent;
            // Simulate loading a chat
            document.getElementById('chat-messages').innerHTML = ''; // Clear
            addMessage(`(Loaded session: ${title})`, 'ai');
            addMessage("Here is where we left off...", "ai");
        });
    });
}

// State for Sidebars
let leftSidebarOpen = true;
let rightSidebarOpen = true;

function startNewChat() {
    if (confirm("Start a fresh new chat session?")) {
        window.location.href = "/";
    }
}

function shareSession(sessionId, event) {
    if (event) event.stopPropagation();
    // In real app: Generate share link or open modal
    alert(`Sharing session ${sessionId}... Link copied to clipboard!`);
}

function downloadSession(sessionId, event) {
    if (event) event.stopPropagation();
    // In real app: Trigger PDF/Text download
    alert(`Downloading session ${sessionId} as PDF...`);
}

function deleteSession(sessionId, event) {
    if (event) event.stopPropagation();
    if (confirm(`Are you sure you want to delete session ${sessionId}?`)) {
        // In real app: API call to delete
        alert(`Session ${sessionId} deleted.`);
        location.reload();
    }
}


function toggleLeftSidebar() {
    const sidebar = document.getElementById('left-sidebar');
    const toggleBtn = document.getElementById('left-toggle-btn');
    const icon = toggleBtn.querySelector('i');
    const headerLogo = document.getElementById('header-logo');

    if (leftSidebarOpen) {
        sidebar.style.marginLeft = '-18rem'; // Hide
        // Icon points RIGHT to show it can be opened
        icon.style.transform = 'rotate(180deg)';
        // Show Header Logo
        if (headerLogo) {
            headerLogo.classList.remove('hidden');
        }
    } else {
        sidebar.style.marginLeft = '0'; // Show
        // Icon points LEFT to show it can be closed
        icon.style.transform = 'rotate(0deg)';
        // Hide Header Logo
        if (headerLogo) headerLogo.classList.add('hidden');
    }
    leftSidebarOpen = !leftSidebarOpen;
}

function toggleRightSidebar() {
    const sidebar = document.getElementById('right-sidebar');
    const toggleBtn = document.getElementById('right-toggle-btn');
    const icon = toggleBtn.querySelector('i');

    if (rightSidebarOpen) {
        sidebar.style.marginRight = '-20rem'; // Hide
        // Icon points LEFT to show it can be opened
        icon.style.transform = 'rotate(180deg)';
    } else {
        sidebar.style.marginRight = '0'; // Show
        // Icon points RIGHT to show it can be closed
        icon.style.transform = 'rotate(0deg)';
    }
    rightSidebarOpen = !rightSidebarOpen;
}
