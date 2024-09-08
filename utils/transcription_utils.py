import os
from openai import OpenAI
from pydub import AudioSegment

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def split_audio(audio_file_path, chunk_length_ms=300000):  # 5 minutes
    audio = AudioSegment.from_mp3(audio_file_path)
    chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

def transcribe_audio_chunk(chunk):
    with open('temp_chunk.mp3', 'wb') as f:
        chunk.export(f, format='mp3')
    with open('temp_chunk.mp3', 'rb') as audio_file:
        transcript = openai_client.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file
        )
    os.remove('temp_chunk.mp3')
    return transcript.text

def transcribe_audio(audio_file_path):
    try:
        chunks = split_audio(audio_file_path)
        transcriptions = []
        for i, chunk in enumerate(chunks):
            print(f"Transcribing chunk {i+1}/{len(chunks)}...")
            transcriptions.append(transcribe_audio_chunk(chunk))
        return ' '.join(transcriptions)
    except Exception as e:
        raise Exception(f'Error transcribing audio: {str(e)}')
