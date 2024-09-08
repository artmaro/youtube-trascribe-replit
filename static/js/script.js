document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('youtube-form');
    const questionForm = document.getElementById('question-form');
    const transcriptionDiv = document.getElementById('transcription');
    const answerDiv = document.getElementById('answer');
    const errorDiv = document.getElementById('error');

    let currentTranscription = '';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const youtubeUrl = document.getElementById('youtube-url').value;

        try {
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ youtube_url: youtubeUrl }),
            });

            const data = await response.json();

            if (data.success) {
                currentTranscription = data.transcription;
                transcriptionDiv.textContent = currentTranscription;
                errorDiv.textContent = '';
                questionForm.style.display = 'block';
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            errorDiv.textContent = `Error: ${error.message}`;
            transcriptionDiv.textContent = '';
            questionForm.style.display = 'none';
        }
    });

    questionForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = document.getElementById('question').value;

        try {
            const response = await fetch('/answer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question, transcription: currentTranscription }),
            });

            const data = await response.json();

            if (data.success) {
                answerDiv.textContent = data.answer;
                errorDiv.textContent = '';
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            errorDiv.textContent = `Error: ${error.message}`;
            answerDiv.textContent = '';
        }
    });
});
