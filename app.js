// document.addEventListener('DOMContentLoaded', () => {
//     const projectForm = document.getElementById('projectForm');
//     const projectLinkDiv = document.getElementById('projectLink');
//     const shareableLink = document.getElementById('shareableLink');
//     const copyShareableLinkBtn = document.getElementById('copyShareableLinkBtn');
//     const projectsContainer = document.getElementById('projectsContainer');

//     const API_URL = 'http://127.0.0.1:8000';

//     // Helper: add skeletons
//     function showSkeletons(count = 3) {
//         projectsContainer.innerHTML = '';
//         for (let i = 0; i < count; i++) {
//             const sk = document.createElement('div');
//             sk.className = 'skeleton-card reveal-on-scroll';
//             sk.innerHTML = `
//                 <div class="skeleton skeleton-title"></div>
//                 <div class="skeleton skeleton-line"></div>
//                 <div class="skeleton skeleton-line short"></div>
//                 <div class="skeleton skeleton-line"></div>
//             `;
//             projectsContainer.appendChild(sk);
//         }
//         window.setupRevealOnScroll?.();
//     }

//     // Handle form submission to create a new project
//     projectForm.addEventListener('submit', async (e) => {
//         e.preventDefault();
//         const formData = new FormData(projectForm);
//         const projectData = Object.fromEntries(formData.entries());
//         const submitBtn = projectForm.querySelector('button[type="submit"]');
//         submitBtn.classList.add('is-loading');

//         try {
//             const response = await fetch(`${API_URL}/api/projects`, {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify(projectData),
//             });

//             if (!response.ok) throw new Error('Failed to create project');

//             const result = await response.json();
//             const interviewLink = `${window.location.origin}/interview.html?project_id=${result.id}`;

//             shareableLink.href = interviewLink;
//             shareableLink.textContent = interviewLink;
//             if (copyShareableLinkBtn) {
//                 copyShareableLinkBtn.dataset.copy = interviewLink;
//             }
//             projectLinkDiv.style.display = 'block';

//             // Subtle gsap pop + confetti
//             try {
//                 if (window.gsap) {
//                     gsap.fromTo(projectLinkDiv, { y: -8, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: 'power2.out' });
//                 }
//             } catch {}
//             window.fireConfetti?.();

//             projectForm.reset();
//             loadProjects(); // Refresh the list of projects

//         } catch (error) {
//             console.error('Error creating project:', error);
//             alert('Could not create project. See console for details.');
//         } finally {
//             submitBtn.classList.remove('is-loading');
//         }
//     });

//     // Copy newly created link
//     copyShareableLinkBtn?.addEventListener('click', () => {
//         const text = copyShareableLinkBtn.dataset.copy || shareableLink.href;
//         window.copyToClipboard?.(text);
//     });

//     // Function to load and display all projects
//     async function loadProjects() {
//         try {
//             showSkeletons(3);
//             const response = await fetch(`${API_URL}/api/projects`);
//             if (!response.ok) throw new Error('Failed to fetch projects');

//             const projects = await response.json();
//             projectsContainer.innerHTML = ''; // Clear current content

//             if (!projects || projects.length === 0) {
//                 const empty = document.createElement('div');
//                 empty.className = 'section-card reveal-on-scroll';
//                 empty.innerHTML = '<p>No projects found. Create one above!</p>';
//                 projectsContainer.appendChild(empty);
//                 window.setupRevealOnScroll?.();
//                 return;
//             }

//             projects.forEach(project => {
//                 const projectCard = document.createElement('div');
//                 projectCard.className = 'project-card reveal-on-scroll';
//                 const idea = project.product_idea || '';
//                 const title = idea.length > 60 ? `${idea.substring(0, 60)}…` : idea;
//                 const interviewLink = `${window.location.origin}/interview.html?project_id=${project.id}`;

//                 projectCard.innerHTML = `
//                     <h3>Project #${project.id}: ${title}</h3>
//                     <p><strong>Core Problem:</strong> ${project.core_problem || ''}</p>
//                     <p><strong>Interviews Conducted:</strong> ${project.interviews?.length ?? 0}</p>
//                     <div class="shareable-link-container">
//                         <p><strong>Shareable Interview Link:</strong></p>
//                         <div class="shareable-row">
//                             <a href="${interviewLink}" target="_blank">${interviewLink}</a>
//                             <button class="btn btn-secondary btn-sm copy-link-btn" type="button" data-copy="${interviewLink}">Copy</button>
//                         </div>
//                     </div>
//                     <div class="project-summary-section">
//                         <button class="btn btn-primary generate-summary-btn" data-project-id="${project.id}">Generate Project Summary</button>
//                         <div class="summary-result-content interview-summary"></div>
//                     </div>
//                 `;
//                 projectsContainer.appendChild(projectCard);
//             });

//             window.setupRevealOnScroll?.();

//         } catch (error) {
//             console.error('Error loading projects:', error);
//             projectsContainer.innerHTML = '<p>Error loading projects. Is the backend running?</p>';
//         }
//     }

//     // Event delegation for project buttons
//     // projectsContainer.addEventListener('click', async (e) => {
//     //     const copyBtn = e.target.closest('.copy-link-btn');
//     //     if (copyBtn) {
//     //         window.copyToClipboard?.(copyBtn.dataset.copy);
//     //         return;
//     //     }

//     //     const genBtn = e.target.closest('.generate-summary-btn');
//     //     if (genBtn) {
//     //         const button = genBtn;
//     //         const projectId = button.dataset.projectId;
//     //         const resultContainer = button.nextElementSibling;

//     //         // Loading state
//     //         button.classList.add('is-loading');
//     //         resultContainer.classList.remove('show');
//     //         resultContainer.style.display = 'block';
//     //         resultContainer.textContent = 'Generating summary, please wait...';

//     //         try {
//     //             const response = await fetch(`${API_URL}/api/projects/${projectId}/generate_summary`, { method: 'POST' });

//     //             if (!response.ok) {
//     //                 let errorMessage = 'Failed to generate summary';
//     //                 try {
//     //                     const errorData = await response.json();
//     //                     errorMessage = errorData.detail || errorMessage;
//     //                 } catch {}
//     //                 throw new Error(errorMessage);
//     //             }

//     //             const result = await response.json();
//     //             // resultContainer.textContent = result.final_summary || 'No summary returned.';
//     //             resultContainer.innerHTML=result.final_summary || 'No summary returned.';

                
                

//     //             resultContainer.classList.add('show');

//     //             try {
//     //                 if (window.gsap) {
//     //                     gsap.fromTo(resultContainer, { y: 6, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35 });
//     //                 }
//     //             } catch {}

//     //         } catch (error) {
//     //             console.error(`Error generating summary for project ${projectId}:`, error);
//     //             resultContainer.textContent = `An error occurred: ${error.message}`;
//     //             resultContainer.classList.add('show');
//     //         } finally {
//     //             button.classList.remove('is-loading');
//     //         }
//     //         //
            
//     //     }
//     // });
//             // Replace the existing event listener in app.js with this one
//     projectsContainer.addEventListener('click', async (e) => {
//         const copyBtn = e.target.closest('.copy-link-btn');
//         if (copyBtn) {
//             window.copyToClipboard?.(copyBtn.dataset.copy);
//             return;
//         }

//         const genBtn = e.target.closest('.generate-summary-btn');
//         if (genBtn) {
//             const button = genBtn;
//             const projectId = button.dataset.projectId;
//             const resultContainer = button.nextElementSibling;

//             // --- 1. Set initial loading state ---
//             button.classList.add('is-loading');
//             resultContainer.classList.remove('show');
//             resultContainer.style.display = 'block';
//             resultContainer.innerHTML = '<p>Generating summary, please wait...</p>';

//             try {
//                 // --- 2. Fetch the summary from the backend ---
//                 const summaryResponse = await fetch(`${API_URL}/api/projects/${projectId}/generate_summary`, { method: 'POST' });
//                 if (!summaryResponse.ok) {
//                     const err = await summaryResponse.json();
//                     throw new Error(err.detail || 'Failed to generate summary');
//                 }
//                 const result = await summaryResponse.json();

//                 // --- 3. Display summary and prepare audio container ---
//                 resultContainer.innerHTML = `
//                     <div class="summary-content">${result.final_summary || '<p>No summary returned.</p>'}</div>
//                     <div class="audio-player-container" style="margin-top: 15px;">
//                         <p>Generating audio...</p>
//                     </div>
//                 `;
//                 resultContainer.classList.add('show');
                
//                 const audioPlayerContainer = resultContainer.querySelector('.audio-player-container');

//                 // --- 4. Automatically fetch the audio ---
//                 // Extract plain text from the summary HTML for the TTS service
//                 const tempDiv = document.createElement('div');
//                 tempDiv.innerHTML = result.final_summary;
//                 const plainTextSummary = tempDiv.textContent || tempDiv.innerText || '';

//                 if (plainTextSummary.trim()) {
//                     const ttsResponse = await fetch(`${API_URL}/api/tts`, {
//                         method: 'POST',
//                         headers: { 'Content-Type': 'application/json' },
//                         body: JSON.stringify({ text: plainTextSummary })
//                     });

//                     if (!ttsResponse.ok) throw new Error('Could not generate audio.');

//                     const audioBlob = await ttsResponse.blob();
//                     const audioUrl = URL.createObjectURL(audioBlob);

//                     // Create the audio player and replace the loading message
//                     const audio = document.createElement('audio');
//                     audio.setAttribute('controls', '');
//                     audio.src = audioUrl;
//                     audio.style.width = '100%';
                    
//                     audioPlayerContainer.innerHTML = ''; // Clear "Generating audio..."
//                     audioPlayerContainer.appendChild(audio);
//                 } else {
//                     audioPlayerContainer.remove(); // No summary text, so no need for a player
//                 }

//             } catch (error) {
//                 console.error(`Error in summary/audio generation for project ${projectId}:`, error);
//                 resultContainer.innerHTML = `<p style="color: #FF0033;">An error occurred: ${error.message}</p>`;
//                 resultContainer.classList.add('show');
//             } finally {
//                 button.classList.remove('is-loading');
//             }
//         }
//     });

//     // Initial load of projects
//     loadProjects();
// });


document.addEventListener('DOMContentLoaded', () => {
    const projectForm = document.getElementById('projectForm');
    const projectLinkDiv = document.getElementById('projectLink');
    const shareableLink = document.getElementById('shareableLink');
    const copyShareableLinkBtn = document.getElementById('copyShareableLinkBtn');
    const projectsContainer = document.getElementById('projectsContainer');

    const API_URL = 'http://127.0.0.1:8000';

    // Helper: add skeletons
    function showSkeletons(count = 3) {
        projectsContainer.innerHTML = '';
        for (let i = 0; i < count; i++) {
            const sk = document.createElement('div');
            sk.className = 'skeleton-card reveal-on-scroll';
            sk.innerHTML = `
                <div class="skeleton skeleton-title"></div>
                <div class="skeleton skeleton-line"></div>
                <div class="skeleton skeleton-line short"></div>
                <div class="skeleton skeleton-line"></div>
            `;
            projectsContainer.appendChild(sk);
        }
        window.setupRevealOnScroll?.();
    }

    // Handle form submission to create a new project
    projectForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(projectForm);
        const projectData = Object.fromEntries(formData.entries());
        const submitBtn = projectForm.querySelector('button[type="submit"]');
        submitBtn.classList.add('is-loading');

        try {
            const response = await fetch(`${API_URL}/api/projects`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(projectData),
            });

            if (!response.ok) throw new Error('Failed to create project');

            const result = await response.json();
            const interviewLink = `${window.location.origin}/interview.html?project_id=${result.id}`;

            shareableLink.href = interviewLink;
            shareableLink.textContent = interviewLink;
            if (copyShareableLinkBtn) {
                copyShareableLinkBtn.dataset.copy = interviewLink;
            }
            projectLinkDiv.style.display = 'block';

            try {
                if (window.gsap) {
                    gsap.fromTo(projectLinkDiv, { y: -8, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: 'power2.out' });
                }
            } catch {}
            window.fireConfetti?.();

            projectForm.reset();
            loadProjects();

        } catch (error) {
            console.error('Error creating project:', error);
            alert('Could not create project. See console for details.');
        } finally {
            submitBtn.classList.remove('is-loading');
        }
    });

    copyShareableLinkBtn?.addEventListener('click', () => {
        const text = copyShareableLinkBtn.dataset.copy || shareableLink.href;
        window.copyToClipboard?.(text);
    });

    // Function to load and display all projects
    async function loadProjects() {
        try {
            showSkeletons(3);
            const response = await fetch(`${API_URL}/api/projects`);
            if (!response.ok) throw new Error('Failed to fetch projects');

            const projects = await response.json();
            projectsContainer.innerHTML = ''; 

            if (!projects || projects.length === 0) {
                const empty = document.createElement('div');
                empty.className = 'section-card reveal-on-scroll';
                empty.innerHTML = '<p>No projects found. Create one above!</p>';
                projectsContainer.appendChild(empty);
                window.setupRevealOnScroll?.();
                return;
            }

            projects.forEach(project => {
                const projectCard = document.createElement('div');
                projectCard.className = 'project-card reveal-on-scroll';
                const idea = project.product_idea || '';
                const title = idea.length > 60 ? `${idea.substring(0, 60)}…` : idea;
                const interviewLink = `${window.location.origin}/interview.html?project_id=${project.id}`;

                // --- MODIFIED: Added a new button "Ask Insights Q&A" linking to the new bot page ---
                projectCard.innerHTML = `
                    <h3>Project #${project.id}: ${title}</h3>
                    <p><strong>Core Problem:</strong> ${project.core_problem || ''}</p>
                    <p><strong>Interviews Conducted:</strong> ${project.interviews?.length ?? 0}</p>
                    <div class="shareable-link-container">
                        <p><strong>Shareable Interview Link:</strong></p>
                        <div class="shareable-row">
                            <a href="${interviewLink}" target="_blank">${interviewLink}</a>
                            <button class="btn btn-secondary btn-sm copy-link-btn" type="button" data-copy="${interviewLink}">Copy</button>
                        </div>
                    </div>
                    <div class="project-summary-section">
                        <button class="btn btn-primary generate-summary-btn" data-project-id="${project.id}">Generate Project Summary</button>
                        <a href="qa_bot.html?project_id=${project.id}" class="btn btn-secondary" target="_blank">Ask Insights Q&A</a>
                        <div class="summary-result-content interview-summary"></div>
                    </div>
                `;
                projectsContainer.appendChild(projectCard);
            });

            window.setupRevealOnScroll?.();

        } catch (error) {
            console.error('Error loading projects:', error);
            projectsContainer.innerHTML = '<p>Error loading projects. Is the backend running?</p>';
        }
    }

    // Event delegation for project buttons
    projectsContainer.addEventListener('click', async (e) => {
        const copyBtn = e.target.closest('.copy-link-btn');
        if (copyBtn) {
            window.copyToClipboard?.(copyBtn.dataset.copy);
            return;
        }

        const genBtn = e.target.closest('.generate-summary-btn');
        if (genBtn) {
            const button = genBtn;
            const projectId = button.dataset.projectId;
            const resultContainer = button.parentElement.querySelector('.summary-result-content');

            button.classList.add('is-loading');
            resultContainer.classList.remove('show');
            resultContainer.style.display = 'block';
            resultContainer.innerHTML = '<p>Generating summary, please wait...</p>';

            try {
                const summaryResponse = await fetch(`${API_URL}/api/projects/${projectId}/generate_summary`, { method: 'POST' });
                if (!summaryResponse.ok) {
                    const err = await summaryResponse.json();
                    throw new Error(err.detail || 'Failed to generate summary');
                }
                const result = await summaryResponse.json();

                resultContainer.innerHTML = `
                    <div class="summary-content">${result.final_summary || '<p>No summary returned.</p>'}</div>
                    <div class="audio-player-container" style="margin-top: 15px;">
                        <p>Generating audio...</p>
                    </div>
                `;
                resultContainer.classList.add('show');
                
                const audioPlayerContainer = resultContainer.querySelector('.audio-player-container');
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = result.final_summary;
                const plainTextSummary = tempDiv.textContent || tempDiv.innerText || '';

                if (plainTextSummary.trim()) {
                    const ttsResponse = await fetch(`${API_URL}/api/tts`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text: plainTextSummary })
                    });

                    if (!ttsResponse.ok) throw new Error('Could not generate audio.');

                    const audioBlob = await ttsResponse.blob();
                    const audioUrl = URL.createObjectURL(audioBlob);
                    
                    const audio = document.createElement('audio');
                    audio.setAttribute('controls', '');
                    audio.src = audioUrl;
                    audio.style.width = '100%';
                    
                    audioPlayerContainer.innerHTML = '';
                    audioPlayerContainer.appendChild(audio);
                } else {
                    audioPlayerContainer.remove();
                }

            } catch (error) {
                console.error(`Error in summary/audio generation for project ${projectId}:`, error);
                resultContainer.innerHTML = `<p style="color: #FF0033;">An error occurred: ${error.message}</p>`;
                resultContainer.classList.add('show');
            } finally {
                button.classList.remove('is-loading');
            }
        }
    });

    loadProjects();
});
