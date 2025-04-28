import os
from flask import Flask, render_template, request, jsonify
import yt_dlp
from moviepy.editor import VideoFileClip
import json
from pathlib import Path

app = Flask(__name__)

# Dossier par défaut pour les téléchargements et conversions
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.'))

def download_video(url, output_dir=DEFAULT_OUTPUT_DIR):
    """Download video using yt-dlp"""
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    ydl_opts = {
        'format': 'best',
        'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist'
    }

    downloaded_files = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Extract info first to handle both single videos and playlists
            info = ydl.extract_info(url, download=False)

            if '_type' in info and info['_type'] == 'playlist':
                # Handle playlist
                for entry in info['entries']:
                    if entry:
                        video_info = ydl.extract_info(entry['url'], download=True)
                        filename = ydl.prepare_filename(video_info)
                        downloaded_files.append({
                            'path': filename,
                            'name': os.path.basename(filename),
                            'status': 'downloaded'
                        })
            else:
                # Handle single video
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                downloaded_files.append({
                    'path': filename,
                    'name': os.path.basename(filename),
                    'status': 'downloaded'
                })

            return {'success': True, 'files': downloaded_files}

        except Exception as e:
            return {'success': False, 'error': str(e)}

def convert_to_mp3(video_path, output_dir=DEFAULT_OUTPUT_DIR):
    """Convert video to MP3"""
    try:
        video = VideoFileClip(video_path)
        filename = os.path.splitext(os.path.basename(video_path))[0]
        mp3_path = os.path.join(output_dir, sanitize_filename(f"{filename}.mp3"))

        video.audio.write_audiofile(mp3_path, logger=None)
        video.close()

        # Remove original video file
        os.remove(video_path)

        return {'success': True, 'path': mp3_path}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        urls = data.get('urls', [])

        if not urls:
            return jsonify({'success': False, 'error': 'Aucune URL fournie'})

        all_downloaded_files = []
        for url in urls:
            if url.strip():
                result = download_video(url.strip())
                if result['success']:
                    all_downloaded_files.extend(result['files'])
                else:
                    return jsonify({'success': False, 'error': f"Erreur pour {url}: {result['error']}"})

        return jsonify({'success': True, 'files': all_downloaded_files})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        files = data.get('files', [])

        if not files:
            return jsonify({'success': False, 'error': 'Aucun fichier à convertir'})

        converted_files = []
        for file in files:
            result = convert_to_mp3(file['path'])
            if result['success']:
                converted_files.append(result['path'])
            else:
                return jsonify({'success': False, 'error': f"Erreur lors de la conversion de {file['name']}: {result['error']}"})

        return jsonify({'success': True, 'files': converted_files})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Créer le dossier de téléchargement au démarrage
    os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
    app.run(debug=True)
