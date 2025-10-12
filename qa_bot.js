// document.addEventListener('DOMContentLoaded', () => {
//     const qaBox = document.getElementById('qa-box');
//     const qaInputForm = document.getElementById('qa-input-form');
//     const qaInput = document.getElementById('qa-input');
//     const qaSubmitButton = document.getElementById('qa-submit-button');
//     const syncButton = document.getElementById('sync-button');
//     const syncStatus = document.getElementById('sync-status');

//     const API_URL = 'http://127.0.0.1:8000';

//     // Get the project_id from the URL query parameters
//     const params = new URLSearchParams(window.location.search);
//     const projectId = params.get('project_id');

//     if (!projectId) {
//         addMessage('Error: No project ID specified in the URL.', 'ai');
//         syncButton.disabled = true;
//         return;
//     }

//     /**
//      * Appends a new message to the chat display.
//      * @param {string} text - The message content.
//      * @param {string} sender - 'user' or 'ai'.
//      */
//     function addMessage(text, sender) {
//         const messageDiv = document.createElement('div');
//         messageDiv.classList.add('message', `${sender}-message`);
//         messageDiv.textContent = text;
//         qaBox.appendChild(messageDiv);
//         qaBox.scrollTop = qaBox.scrollHeight;
//     }

//     // --- Step 1: Sync Summaries with the Vector Database ---
//     syncButton.addEventListener('click', async () => {
//         syncButton.disabled = true;
//         syncStatus.textContent = 'Preparing insights... This may take a moment.';
//         syncButton.classList.add('is-loading');

//         try {
//             const response = await fetch(`${API_URL}/api/projects/${projectId}/sync_summaries`, {
//                 method: 'POST'
//             });
//             const result = await response.json();

//             if (!response.ok) {
//                 throw new Error(result.detail || 'Failed to sync summaries.');
//             }
            
//             syncStatus.textContent = `Insights ready! ${result.synced_count || 0} summaries processed. You can now ask questions.`;
//             syncStatus.style.color = '#4CAF50'; // Green for success
            
//             // Enable the question input form now that the backend is ready
//             qaInput.disabled = false;
//             qaSubmitButton.disabled = false;
//             addMessage('Hello! I have analyzed the interview summaries for this project. What would you like to know?', 'ai');

//         } catch (error) {
//             console.error('Error syncing summaries:', error);
//             syncStatus.textContent = `Error: ${error.message}`;
//             syncStatus.style.color = '#FF0033'; // Red for error
//             syncButton.disabled = false; // Allow user to try again
//         } finally {
//              syncButton.classList.remove('is-loading');
//         }
//     });

//     // --- Step 2: Handle User Question Submission ---
//     qaInputForm.addEventListener('submit', async (e) => {
//         e.preventDefault();
//         const question = qaInput.value.trim();
//         if (!question) return;

//         addMessage(question, 'user');
//         qaInput.value = '';
//         qaInput.disabled = true;
//         qaSubmitButton.disabled = true;
        
//         // Add a temporary "thinking" message from the AI
//         const thinkingMessage = document.createElement('div');
//         thinkingMessage.classList.add('message', 'ai-message', 'thinking');
//         thinkingMessage.textContent = 'Analyzing...';
//         qaBox.appendChild(thinkingMessage);
//         qaBox.scrollTop = qaBox.scrollHeight;

//         try {
//             const response = await fetch(`${API_URL}/api/projects/${projectId}/ask`, {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify({ question: question }),
//             });
            
//             const result = await response.json();
//             qaBox.removeChild(thinkingMessage); // Remove "thinking" message

//             if (!response.ok) {
//                 throw new Error(result.detail || 'Failed to get an answer.');
//             }

//             addMessage(result.answer, 'ai');

//         } catch (error) {
//             console.error('Error asking question:', error);
//             qaBox.removeChild(thinkingMessage);
//             addMessage(`Sorry, an error occurred: ${error.message}`, 'ai');
//         } finally {
//             // Re-enable input for the next question
//             qaInput.disabled = false;
//             qaSubmitButton.disabled = false;
//             qaInput.focus();
//         }
//     });
// });

document.addEventListener('DOMContentLoaded', () => {
    const qaBox = document.getElementById('qa-box');
    const qaInputForm = document.getElementById('qa-input-form');
    const qaInput = document.getElementById('qa-input');
    const qaSubmitButton = document.getElementById('qa-submit-button');
    const syncButton = document.getElementById('sync-button');
    const syncStatus = document.getElementById('sync-status');

    const API_URL = 'http://127.0.0.1:8000';
    let currentAudio = null; // Manages the currently playing audio

    const params = new URLSearchParams(window.location.search);
    const projectId = params.get('project_id');

    if (!projectId) {
        addMessage('Error: No project ID specified in the URL.', 'ai');
        syncButton.disabled = true;
        return;
    }

    /**
     * Handles the playback of text-to-speech audio when a TTS button is clicked.
     * @param {HTMLElement} button - The TTS button element that was clicked.
     */
    async function handleTTSPlay(button) {
        const textToSpeak = button.dataset.text;

        // Stop any audio that is currently playing
        if (currentAudio && !currentAudio.paused) {
            currentAudio.pause();
            document.querySelectorAll('.tts-button').forEach(btn => btn.innerHTML = '🔊');
        }

        // If the clicked button was the one playing, stop and return
        if (button.dataset.isPlaying === 'true') {
            button.dataset.isPlaying = 'false';
            return;
        }

        // Reset all button states before playing new audio
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
            button.innerHTML = '⏹️'; // Playing state icon
            button.dataset.isPlaying = 'true';

            // Reset button when audio finishes
            currentAudio.onended = () => {
                button.innerHTML = '🔊';
                button.dataset.isPlaying = 'false';
            };
        } catch (error) {
            console.error('TTS Error:', error);
            button.classList.remove('loading');
            button.innerHTML = '⚠️'; // Error state icon
        }
    }

    /**
     * Appends a new message to the chat display. For AI messages, it also
     * injects a text-to-speech (TTS) button.
     * @param {string} text - The message content, which can include HTML.
     * @param {string} sender - 'user' or 'ai'.
     */
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);

        if (sender === 'ai') {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = text;
            const plainText = (tempDiv.textContent || tempDiv.innerText).trim();

            if (plainText) {
                const escapedText = plainText.replace(/'/g, "&apos;").replace(/"/g, "&quot;");
                const ttsButtonHtml = `<button class='tts-button' aria-label='Listen to message' data-text='${escapedText}'>🔊</button>`;
                messageDiv.innerHTML = `<div class="ai-message-wrapper"><div class="message-content">${text}</div>${ttsButtonHtml}</div>`;
            } else {
                messageDiv.innerHTML = text;
            }
        } else {
            messageDiv.textContent = text;
        }

        qaBox.appendChild(messageDiv);
        qaBox.scrollTop = qaBox.scrollHeight;
    }
    
    syncButton.addEventListener('click', async () => {
        syncButton.disabled = true;
        syncStatus.textContent = 'Preparing insights... This may take a moment.';
        syncButton.classList.add('is-loading');

        try {
            const response = await fetch(`${API_URL}/api/projects/${projectId}/sync_summaries`, {
                method: 'POST'
            });
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || 'Failed to sync summaries.');
            }
            
            syncStatus.textContent = `Insights ready! ${result.synced_count || 0} summaries processed. You can now ask questions.`;
            syncStatus.style.color = '#4CAF50';
            
            qaInput.disabled = false;
            qaSubmitButton.disabled = false;
            addMessage('Hello! I have analyzed the interview summaries for this project. What would you like to know?', 'ai');

        } catch (error) {
            console.error('Error syncing summaries:', error);
            syncStatus.textContent = `Error: ${error.message}`;
            syncStatus.style.color = '#FF0033';
            syncButton.disabled = false;
        } finally {
             syncButton.classList.remove('is-loading');
        }
    });

    qaInputForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = qaInput.value.trim();
        if (!question) return;

        addMessage(question, 'user');
        qaInput.value = '';
        qaInput.disabled = true;
        qaSubmitButton.disabled = true;
        
        const thinkingMessage = document.createElement('div');
        thinkingMessage.classList.add('message', 'ai-message', 'thinking');
        thinkingMessage.textContent = 'Analyzing...';
        qaBox.appendChild(thinkingMessage);
        qaBox.scrollTop = qaBox.scrollHeight;

        try {
            const response = await fetch(`${API_URL}/api/projects/${projectId}/ask`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question }),
            });
            
            const result = await response.json();
            qaBox.removeChild(thinkingMessage);

            if (!response.ok) {
                throw new Error(result.detail || 'Failed to get an answer.');
            }

            addMessage(result.answer, 'ai');

        } catch (error) {
            console.error('Error asking question:', error);
            qaBox.removeChild(thinkingMessage);
            addMessage(`Sorry, an error occurred: ${error.message}`, 'ai');
        } finally {
            qaInput.disabled = false;
            qaSubmitButton.disabled = false;
            qaInput.focus();
        }
    });

    // --- NEW: Event Delegation for TTS button clicks ---
    qaBox.addEventListener('click', (e) => {
        const ttsButton = e.target.closest('.tts-button');
        if (ttsButton) {
            handleTTSPlay(ttsButton);
        }
    });
});

