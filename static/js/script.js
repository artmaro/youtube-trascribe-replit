document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('youtube-form');
    const questionForm = document.getElementById('question-form');
    const transcriptionDiv = document.getElementById('transcription');
    const answerDiv = document.getElementById('answer');
    const errorDiv = document.getElementById('error');
    const exportTranscriptionBtn = document.getElementById('export-transcription');
    const exportQABtn = document.getElementById('export-qa');

    let currentTranscription = '';
    let qaData = [];

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
                exportTranscriptionBtn.style.display = 'block';
                qaData = []; // Reset Q&A data
                exportQABtn.style.display = 'none';
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            errorDiv.textContent = `Error: ${error.message}`;
            transcriptionDiv.textContent = '';
            questionForm.style.display = 'none';
            exportTranscriptionBtn.style.display = 'none';
            exportQABtn.style.display = 'none';
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
                qaData.push({ question, answer: data.answer });
                exportQABtn.style.display = 'block';
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            errorDiv.textContent = `Error: ${error.message}`;
            answerDiv.textContent = '';
        }
    });

    exportTranscriptionBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/export_transcription', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ transcription: currentTranscription }),
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = 'transcription.csv';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            } else {
                throw new Error('Failed to export transcription');
            }
        } catch (error) {
            errorDiv.textContent = `Error: ${error.message}`;
        }
    });

    exportQABtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/export_qa', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ qa_data: qaData }),
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = 'qa_results.csv';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            } else {
                throw new Error('Failed to export Q&A results');
            }
        } catch (error) {
            errorDiv.textContent = `Error: ${error.message}`;
        }
    });
});
