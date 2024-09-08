import os
from flask import Flask, render_template, request, jsonify
from utils.youtube_utils import download_audio, is_valid_youtube_url
from utils.transcription_utils import transcribe_audio
from utils.qa_utils import answer_question

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    youtube_url = request.json['youtube_url']
    
    try:
        if not is_valid_youtube_url(youtube_url):
            return jsonify({'success': False, 'error': 'Invalid YouTube URL'})

        # Download audio
        audio_file = download_audio(youtube_url)
        
        # Transcribe audio
        transcription = transcribe_audio(audio_file)
        
        # Clean up the audio file
        os.remove(audio_file)
        
        return jsonify({'success': True, 'transcription': transcription})
    except ValueError as ve:
        return jsonify({'success': False, 'error': str(ve)})
    except Exception as e:
        return jsonify({'success': False, 'error': f"An unexpected error occurred: {str(e)}"})

@app.route('/answer', methods=['POST'])
def answer():
    question = request.json['question']
    transcription = request.json['transcription']
    
    try:
        answer = answer_question(question, transcription)
        return jsonify({'success': True, 'answer': answer})
    except Exception as e:
        return jsonify({'success': False, 'error': f"Error answering question: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
