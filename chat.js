// document.addEventListener('DOMContentLoaded', () => {
//     const chatBox = document.getElementById('chat-box');
//     const chatInputForm = document.getElementById('chat-input');
//     const userInput = document.getElementById('userInput');

//     const API_URL = 'http://127.0.0.1:8000';
//     let interviewId = null;

//     // Get project_id from URL
//     const params = new URLSearchParams(window.location.search);
//     const projectId = params.get('project_id');

//     if (!projectId) {
//         addMessage('Error: No project ID found in URL.', 'ai');
//         return;
//     }

//     function scrollToBottom() {
//         chatBox.scrollTop = chatBox.scrollHeight;
//     }

//     // // Function to add a message to the chat box
//     // function addMessage(text, sender, options = {}) {
//     //     const { isLoading = false, typed = false } = options;
//     //     const messageDiv = document.createElement('div');
//     //     messageDiv.classList.add('message', `${sender}-message`);

//     //     if (isLoading) {
//     //         messageDiv.classList.add('thinking');
//     //         messageDiv.textContent = ' ';
//     //         chatBox.appendChild(messageDiv);
//     //         scrollToBottom();
//     //         return messageDiv;
//     //     }

//     //     if (typed && sender === 'ai') {
//     //         messageDiv.textContent = '';
//     //         chatBox.appendChild(messageDiv);
//     //         typeText(messageDiv, text);
//     //     } else {
//     //         messageDiv.textContent = text;
//     //         chatBox.appendChild(messageDiv);
//     //     }

//     //     scrollToBottom();
//     //     return messageDiv;
//     // }
//     // Function to add a message to the chat box
//     function addMessage(text, sender, options = {}) {
//         // Add isHtml to the destructured options, defaulting to false
//         const { isLoading = false, typed = false, isHtml = false } = options;
//         const messageDiv = document.createElement('div');
//         messageDiv.classList.add('message', `${sender}-message`);

//         if (isLoading) {
//             messageDiv.classList.add('thinking');
//             messageDiv.textContent = ' ';
//             chatBox.appendChild(messageDiv);
//             scrollToBottom();
//             return messageDiv;
//         }

//         // NEW: Check if the content is HTML
//         if (isHtml) {
//             // Use innerHTML to parse and render the HTML string
//             messageDiv.innerHTML = text;
//             chatBox.appendChild(messageDiv);
//         } else if (typed && sender === 'ai') {
//             messageDiv.textContent = '';
//             chatBox.appendChild(messageDiv);
//             typeText(messageDiv, text);
//         } else {
//             // Default behavior for plain text
//             messageDiv.textContent = text;
//             chatBox.appendChild(messageDiv);
//         }

//         scrollToBottom();
//         return messageDiv;
//     }

//     // Typewriter effect for AI messages
//     async function typeText(el, fullText) {
//         const maxDurationMs = 2000;
//         const minSpeed = 8;   // ms per char
//         const maxSpeed = 22;  // ms per char
//         const len = (fullText || '').length;
//         if (len === 0) return;

//         // Adaptive speed so long messages don't take forever
//         const approxMsPerChar = Math.max(minSpeed, Math.min(maxSpeed, Math.floor(maxDurationMs / Math.max(1, len)) * 2));
//         for (let i = 1; i <= len; i++) {
//             el.textContent = fullText.slice(0, i);
//             scrollToBottom();
//             await new Promise(r => setTimeout(r, approxMsPerChar));
//         }
//     }

//     // Start the interview process
//     async function startInterview() {
//         // Subtle reveal on the chat box
//         document.querySelectorAll('.reveal-on-scroll').forEach(el => el.classList.add('reveal'));
//         try {
//             const response = await fetch(`${API_URL}/api/interviews`, {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify({ project_id: parseInt(projectId) }),
//             });
//             if (!response.ok) throw new Error('Failed to start interview');

//             const data = await response.json();
//             interviewId = data.interview_id;
//             // addMessage(data.first_question, 'ai', { typed: true });
//             addMessage(data.first_question, 'ai', { isHtml: true });

//         } catch (error) {
//             console.error('Error starting interview:', error);
//             addMessage('Sorry, there was an error starting the interview. Please try again later.', 'ai');
//             userInput.disabled = true;
//         }
//     }

//     // Handle user sending a message
//     chatInputForm.addEventListener('submit', async (e) => {
//         e.preventDefault();
//         const userText = userInput.value.trim();
//         if (!userText || !interviewId) return;

//         addMessage(userText, 'user');
//         userInput.value = '';
//         userInput.disabled = true;

//         const thinkingIndicator = addMessage('', 'ai', { isLoading: true });

//         try {
//             const response = await fetch(`${API_URL}/api/interviews/${interviewId}/message`, {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify({ content: userText }),
//             });

//             if (!response.ok) throw new Error('Failed to get response');

//             const data = await response.json();

//             // Remove thinking indicator and add final AI response
//             chatBox.removeChild(thinkingIndicator);
//             // addMessage(data.response, 'ai', { typed: true });
//             addMessage(data.response, 'ai', { isHtml: true });

//             if (data.status === 'completed') {
//                 userInput.disabled = true;
//                 userInput.placeholder = "Interview complete. Thank you!";
//                 window.fireConfetti?.();
//                 window.showToast?.("Interview complete!");
//             } else {
//                 userInput.disabled = false;
//                 userInput.focus();
//             }

//         } catch (error) {
//             console.error('Error sending message:', error);
//             chatBox.removeChild(thinkingIndicator);
//             addMessage('Sorry, an error occurred. Please try sending your message again.', 'ai');
//             userInput.disabled = false;
//         }
//     });

//     startInterview();
// });







// document.addEventListener('DOMContentLoaded', () => {
//     const chatBox = document.getElementById('chat-box');
//     const chatInputForm = document.getElementById('chat-input');
//     const userInput = document.getElementById('userInput');

//     const API_URL = 'http://127.0.0.1:8000';
//     let interviewId = null;

//     // Get project_id from URL
//     const params = new URLSearchParams(window.location.search);
//     const projectId = params.get('project_id');

//     if (!projectId) {
//         addMessage('Error: No project ID found in URL.', 'ai');
//         return;
//     }

//     function scrollToBottom() {
//         chatBox.scrollTop = chatBox.scrollHeight;
//     }

//     // Function to add a message to the chat box (no changes here)
//     function addMessage(text, sender, options = {}) {
//         const { isLoading = false, typed = false, isHtml = false } = options;
//         const messageDiv = document.createElement('div');
//         messageDiv.classList.add('message', `${sender}-message`);

//         if (isLoading) {
//             messageDiv.classList.add('thinking');
//             messageDiv.textContent = ' ';
//             chatBox.appendChild(messageDiv);
//             scrollToBottom();
//             return messageDiv;
//         }

//         if (isHtml) {
//             messageDiv.innerHTML = text;
//             chatBox.appendChild(messageDiv);
//         } else if (typed && sender === 'ai') {
//             messageDiv.textContent = '';
//             chatBox.appendChild(messageDiv);
//             typeText(messageDiv, text);
//         } else {
//             messageDiv.textContent = text;
//             chatBox.appendChild(messageDiv);
//         }

//         scrollToBottom();
//         return messageDiv;
//     }

//     // Typewriter effect for AI messages (no changes here)
//     async function typeText(el, fullText) {
//         const maxDurationMs = 2000;
//         const minSpeed = 8;
//         const maxSpeed = 22;
//         const len = (fullText || '').length;
//         if (len === 0) return;
//         const approxMsPerChar = Math.max(minSpeed, Math.min(maxSpeed, Math.floor(maxDurationMs / Math.max(1, len)) * 2));
//         for (let i = 1; i <= len; i++) {
//             el.textContent = fullText.slice(0, i);
//             scrollToBottom();
//             await new Promise(r => setTimeout(r, approxMsPerChar));
//         }
//     }
    
//     // Start the interview process (no changes here)
//     async function startInterview() {
//         document.querySelectorAll('.reveal-on-scroll').forEach(el => el.classList.add('reveal'));
//         try {
//             const response = await fetch(`${API_URL}/api/interviews`, {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify({ project_id: parseInt(projectId) }),
//             });
//             if (!response.ok) throw new Error('Failed to start interview');
//             const data = await response.json();
//             interviewId = data.interview_id;
//             addMessage(data.first_question, 'ai', { isHtml: true });
//         } catch (error) {
//             console.error('Error starting interview:', error);
//             addMessage('Sorry, there was an error starting the interview. Please try again later.', 'ai');
//             userInput.disabled = true;
//         }
//     }
    
//     // --- NEW: Reusable function to send a message to the API ---
//     async function sendMessage(contentValue, displayValue) {
//         if (!contentValue || !interviewId) return;

//         // Use the displayValue for the user's message in the chat
//         addMessage(displayValue, 'user');
//         userInput.disabled = true;

//         const thinkingIndicator = addMessage('', 'ai', { isLoading: true });

//         try {
//             const response = await fetch(`${API_URL}/api/interviews/${interviewId}/message`, {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 // Use the contentValue to send to the API
//                 body: JSON.stringify({ content: contentValue }),
//             });

//             if (!response.ok) throw new Error('Failed to get response');

//             const data = await response.json();
//             chatBox.removeChild(thinkingIndicator);
//             addMessage(data.response, 'ai', { isHtml: true });

//             if (data.status === 'completed') {
//                 userInput.disabled = true;
//                 userInput.placeholder = "Interview complete. Thank you!";
//                 window.fireConfetti?.();
//                 window.showToast?.("Interview complete!");
//             } else {
//                 userInput.disabled = false;
//                 userInput.focus();
//             }
//         } catch (error) {
//             console.error('Error sending message:', error);
//             chatBox.removeChild(thinkingIndicator);
//             addMessage('Sorry, an error occurred. Please try sending your message again.', 'ai');
//             userInput.disabled = false;
//         }
//     }

//     // --- MODIFIED: The form submission now uses the new sendMessage function ---
//     chatInputForm.addEventListener('submit', async (e) => {
//         e.preventDefault();
//         const userText = userInput.value.trim();
//         sendMessage(userText, userText); // The value and display text are the same
//         userInput.value = '';
//     });

//     // --- NEW: Event listener on the chatBox to handle MCQ option selection ---
//     chatBox.addEventListener('change', (e) => {
//         // Check if the changed element is a radio button
//         if (e.target.matches('input[type="radio"]')) {
//             const radio = e.target;
//             const selectedValue = radio.value;
            
//             // Find the label associated with the radio button to get its text
//             const label = document.querySelector(`label[for="${radio.id}"]`);
//             const displayText = label ? label.textContent : selectedValue;

//             // Disable all radio buttons in this group to prevent another selection
//             document.querySelectorAll(`input[name="${radio.name}"]`).forEach(rb => {
//                 rb.disabled = true;
//             });

//             // Call the same function to send the data to the API
//             sendMessage(selectedValue, displayText);
//         }
//     });

//     startInterview();
// });


document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const chatInputForm = document.getElementById('chat-input');
    const userInput = document.getElementById('userInput');

    const API_URL = 'http://127.0.0.1:8000';
    let interviewId = null;
    let currentAudio = null; // Manages the currently playing audio

    const params = new URLSearchParams(window.location.search);
    const projectId = params.get('project_id');

    if (!projectId) {
        addMessage('Error: No project ID found in URL.', 'ai');
        return;
    }

    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // --- NEW: Function to handle TTS playback ---
    async function handleTTSPlay(button) {
        const textToSpeak = button.dataset.text;

        // Stop any currently playing audio
        if (currentAudio && !currentAudio.paused) {
            currentAudio.pause();
            document.querySelectorAll('.tts-button').forEach(btn => btn.innerHTML = '🔊');
        }

        if (button.dataset.isPlaying === 'true') {
            button.dataset.isPlaying = 'false';
            return;
        }

        document.querySelectorAll('.tts-button').forEach(btn => {
            btn.innerHTML = '🔊';
            btn.dataset.isPlaying = 'false';
        });

        button.innerHTML = '...';
        button.classList.add('loading');

        try {
            const response = await fetch(`${API_URL}/api/tts`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: textToSpeak }),
            });
            if (!response.ok) throw new Error('Failed to generate audio');

            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            currentAudio = new Audio(audioUrl);
            currentAudio.play();

            button.classList.remove('loading');
            button.innerHTML = '⏹️';
            button.dataset.isPlaying = 'true';

            currentAudio.onended = () => {
                button.innerHTML = '🔊';
                button.dataset.isPlaying = 'false';
            };
        } catch (error) {
            console.error('TTS Error:', error);
            button.classList.remove('loading');
            button.innerHTML = '⚠️';
        }
    }

    // --- MODIFIED: addMessage now injects the TTS button into the AI's HTML ---
    function addMessage(text, sender, options = {}) {
        const { isLoading = false, typed = false, isHtml = false } = options;
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);

        // --- TTS Injection Logic ---
        if (sender === 'ai' && !isLoading && text.trim()) {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = text;
            const plainText = (tempDiv.textContent || tempDiv.innerText).trim();

            if (plainText) {
                const escapedText = plainText.replace(/'/g, "&apos;").replace(/"/g, "&quot;");
                const ttsButtonHtml = `<button class='tts-button' aria-label='Listen to message' data-text='${escapedText}'>🔊</button>`;
                text = `<div class="ai-message-wrapper"><div class="message-content">${text}</div>${ttsButtonHtml}</div>`;
            }
        }
        // --- End of TTS Logic ---

        if (isLoading) {
            messageDiv.classList.add('thinking');
            messageDiv.textContent = ' ';
            chatBox.appendChild(messageDiv);
        } else if (isHtml) {
            messageDiv.innerHTML = text;
            chatBox.appendChild(messageDiv);
        } else if (typed && sender === 'ai') { // Fallback for non-html typed messages
            messageDiv.textContent = '';
            chatBox.appendChild(messageDiv);
            typeText(messageDiv, text);
        } else {
            messageDiv.textContent = text;
            chatBox.appendChild(messageDiv);
        }
        scrollToBottom();
        return messageDiv;
    }

    async function typeText(el, fullText) {
        // (This function remains unchanged, kept for completeness)
        const maxDurationMs = 2000;
        const minSpeed = 8;
        const maxSpeed = 22;
        const len = (fullText || '').length;
        if (len === 0) return;
        const approxMsPerChar = Math.max(minSpeed, Math.min(maxSpeed, Math.floor(maxDurationMs / Math.max(1, len)) * 2));
        for (let i = 1; i <= len; i++) {
            el.textContent = fullText.slice(0, i);
            scrollToBottom();
            await new Promise(r => setTimeout(r, approxMsPerChar));
        }
    }

    async function startInterview() {
        // (This function remains unchanged)
        try {
            const response = await fetch(`${API_URL}/api/interviews`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ project_id: parseInt(projectId) }),
            });
            if (!response.ok) throw new Error('Failed to start interview');
            const data = await response.json();
            interviewId = data.interview_id;
            addMessage(data.first_question, 'ai', { isHtml: true });
        } catch (error) {
            console.error('Error starting interview:', error);
            addMessage('Sorry, there was an error starting the interview.', 'ai');
            userInput.disabled = true;
        }
    }
    
    async function sendMessage(contentValue, displayValue) {
        // (This function remains unchanged)
        if (!contentValue || !interviewId) return;
        addMessage(displayValue, 'user');
        userInput.disabled = true;
        const thinkingIndicator = addMessage('', 'ai', { isLoading: true });
        try {
            const response = await fetch(`${API_URL}/api/interviews/${interviewId}/message`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: contentValue }),
            });
            if (!response.ok) throw new Error('Failed to get response');
            const data = await response.json();
            chatBox.removeChild(thinkingIndicator);
            addMessage(data.response, 'ai', { isHtml: true });
            if (data.status === 'completed') {
                userInput.disabled = true;
                userInput.placeholder = "Interview complete. Thank you!";
            } else {
                userInput.disabled = false;
                userInput.focus();
            }
        } catch (error) {
            console.error('Error sending message:', error);
            chatBox.removeChild(thinkingIndicator);
            addMessage('Sorry, an error occurred. Please try sending your message again.', 'ai');
            userInput.disabled = false;
        }
    }

    chatInputForm.addEventListener('submit', async (e) => {
        // (This function remains unchanged)
        e.preventDefault();
        const userText = userInput.value.trim();
        sendMessage(userText, userText);
        userInput.value = '';
    });
    
    // --- NEW: Event Delegation listener for all dynamic buttons ---
    chatBox.addEventListener('click', (e) => {
        // TTS button clicks
        const ttsButton = e.target.closest('.tts-button');
        if (ttsButton) {
            handleTTSPlay(ttsButton);
        }
    });

    chatBox.addEventListener('change', (e) => {
        // (This function remains unchanged)
        if (e.target.matches('input[type="radio"]')) {
            const radio = e.target;
            const selectedValue = radio.value;
            const label = document.querySelector(`label[for="${radio.id}"]`);
            const displayText = label ? label.textContent : selectedValue;
            document.querySelectorAll(`input[name="${radio.name}"]`).forEach(rb => {
                rb.disabled = true;
            });
            sendMessage(selectedValue, displayText);
        }
    });

    startInterview();
});