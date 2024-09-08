import os
import re
import logging
import shutil
from pytube import YouTube
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_valid_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    youtube_regex_match = re.match(youtube_regex, url)
    return bool(youtube_regex_match)

def download_audio(youtube_url):
    if not is_valid_youtube_url(youtube_url):
        raise ValueError("Invalid YouTube URL")

    logger.info(f"Attempting to download audio from: {youtube_url}")

    ffmpeg_path = shutil.which('ffmpeg')
    if not ffmpeg_path:
        raise Exception('ffmpeg not found. Please install ffmpeg.')

    def download_with_pytube():
        try:
            yt = YouTube(youtube_url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            
            if not audio_stream:
                raise ValueError("No audio stream available for this video")

            audio_file = audio_stream.download(output_path='/tmp', filename='temp_audio')
            
            base, ext = os.path.splitext(audio_file)
            new_file = base + '.mp3'
            os.rename(audio_file, new_file)
            
            logger.info(f"Successfully downloaded audio using pytube: {new_file}")
            return new_file
        except Exception as e:
            logger.error(f"Error downloading with pytube: {str(e)}")
            raise

    def download_with_yt_dlp():
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '/tmp/temp_audio.%(ext)s',
            'ffmpeg_location': ffmpeg_path,
        }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            
            new_file = '/tmp/temp_audio.mp3'
            logger.info(f"Successfully downloaded audio using yt-dlp: {new_file}")
            return new_file
        except Exception as e:
            logger.error(f"Error downloading with yt-dlp: {str(e)}")
            raise

    try:
        return download_with_pytube()
    except Exception as pytube_error:
        logger.warning(f"Pytube download failed. Attempting with yt-dlp. Error: {str(pytube_error)}")
        try:
            return download_with_yt_dlp()
        except Exception as yt_dlp_error:
            error_message = f"Both pytube and yt-dlp failed to download the audio. Pytube error: {str(pytube_error)}. yt-dlp error: {str(yt_dlp_error)}"
            logger.error(error_message)
            raise Exception(error_message)
