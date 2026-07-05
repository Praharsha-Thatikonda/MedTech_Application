let selectedImage = null;
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

// State for Sidebars
let leftSidebarOpen = true;
let rightSidebarOpen = true;

function startNewChat() {
    // In a real app, this would likely create a new session ID via API first
    // For now, reload to simulate or clear
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

function getSessionId() {
    return 1;
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
            // Small delay for fade-in (requires opacity transition classes in HTML)
            // But 'hidden' display:none overrides opacity. 
            // So we remove hidden first.
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

function sendMessage() {
    const input = document.getElementById('message-input');
    const text = input.value.trim();
    if (!text) return;

    // Optimistic UI Update (Add User Message Immediately)
    addMessage(text, 'user');
    input.value = '';
    input.style.height = 'auto';
    showTypingIndicator();

    // Call Backend API
    const payload = {
        text: text,
        session_id: getSessionId(),
        model: document.getElementById('model-selector').value,
        coords: [40.7128, -74.0060]
    };

    if (selectedImage) {
        payload.image_data = selectedImage;
    }

    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            hideTypingIndicator();
            selectedImage = null; // Clear image after send
            addMessage(data.reply, 'ai');
        })
        .catch(error => {
            console.error('Error:', error);
            hideTypingIndicator();
            addMessage("Sorry, I'm having trouble connecting to the server.", 'ai');
        });
}

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

// (Removed generateAIResponse as it is now server-side)

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

function hideTypingIndicator() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
}

function scrollToBottom(smooth = false) {
    const container = document.getElementById('chat-container');
    if (container) {
        if (smooth) {
            container.scrollTo({
                top: container.scrollHeight,
                behavior: 'smooth'
            });
        } else {
            container.scrollTop = container.scrollHeight;
        }
    }
}

function getCurrentTime() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Interactive Features (Keep these simulations for non-DB features like Calls/Uploads)
function setupFeatureInteractions() {
    // 1. New Chat Button
    const buttons = document.querySelectorAll('button');
    buttons.forEach(btn => {
        if (btn.textContent.includes('New Chat')) {
            btn.addEventListener('click', () => {
                location.reload(); // Reload to start new or reset
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
            btn.addEventListener('click', async () => {
                // Real Video Call Feature (Webcam Overlay)
                if (document.getElementById('video-overlay')) return; // Already open

                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });

                    const overlay = document.createElement('div');
                    overlay.id = 'video-overlay';
                    overlay.className = 'fixed inset-0 bg-black/80 z-[60] flex items-center justify-center animate-fade-in';
                    overlay.innerHTML = `
                        <div class="relative bg-gray-900 rounded-3xl overflow-hidden shadow-2xl w-[90%] max-w-4xl aspect-video border border-gray-800">
                            <video id="local-video" autoplay muted playsinline class="w-full h-full object-cover transform scale-x-[-1]"></video>
                            
                            <!-- Controls -->
                            <div class="absolute bottom-6 left-0 right-0 flex justify-center space-x-4">
                                <button onclick="stopVideoCall()" class="w-12 h-12 bg-red-600 hover:bg-red-700 text-white rounded-full flex items-center justify-center shadow-lg transition-transform hover:scale-110">
                                    <i class="fas fa-phone-slash"></i>
                                </button>
                                <button class="w-12 h-12 bg-gray-700 hover:bg-gray-600 text-white rounded-full flex items-center justify-center shadow-lg">
                                    <i class="fas fa-microphone-slash"></i>
                                </button>
                            </div>
                            
                            <!-- Status -->
                            <div class="absolute top-6 left-6 bg-black/50 backdrop-blur-md px-4 py-1.5 rounded-full flex items-center space-x-2">
                                <div class="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                                <span class="text-white text-xs font-mono">REC 00:00</span>
                            </div>
                        </div>
                    `;
                    document.body.appendChild(overlay);

                    const videoElement = document.getElementById('local-video');
                    videoElement.srcObject = stream;

                    // Global stop function
                    window.stopVideoCall = () => {
                        stream.getTracks().forEach(track => track.stop());
                        overlay.remove();
                        addMessage("Video call ended.", "ai");
                    };

                    addMessage("Starting video secure connection...", "ai");

                } catch (err) {
                    console.error(err);
                    alert("Could not access camera: " + err.message);
                }
            });
        }
    });

    // 3. Attachments
    const icons = document.querySelectorAll('.fa-paperclip, .fa-image');
    icons.forEach(icon => {
        icon.parentElement.addEventListener('click', () => {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = 'image/*'; // Accept images
            input.onchange = e => {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function (event) {
                        selectedImage = event.target.result; // Store Base64
                        addMessage(`📎 Image selected: ${file.name} (Ready to send)`, 'user');
                    };
                    reader.readAsDataURL(file);
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
                // Recording
            } else {
                addMessage("🎤 Voice message (0:05)", "user");
                setTimeout(() => addMessage("I heard you. Processing...", "ai"), 1000);
            }
        });
    }

    // 5. History Items (Clicking them simulates switch, but real implementation would need ID navigation)
    // We already load history via SSR loop, so clicking simulated switch:
    const historyItems = document.querySelectorAll('#left-sidebar .group');
    historyItems.forEach(item => {
        item.addEventListener('click', () => {
            // Ideally navigate to ?session_id=X
            // For now, simple visual check
            console.log("Switching session...");
        });
    });
}

// State for Sidebars (Already declared at top)

function startNewChat() {
    if (confirm("Start a fresh new chat session?")) {
        window.location.href = "/";
    }
}

function shareSession(sessionId, event) {
    if (event) event.stopPropagation();
    alert(`Sharing session ${sessionId}... Link copied to clipboard!`);
}

function downloadSession(sessionId, event) {
    if (event) event.stopPropagation();
    alert(`Downloading session ${sessionId} as PDF...`);
}

function deleteSession(sessionId, event) {
    if (event) event.stopPropagation();
    if (confirm(`Are you sure you want to delete session ${sessionId}?`)) {
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
