from flask import Flask, request, send_file, jsonify
import yt_dlp
import uuid
import os

app = Flask(__name__)

DOWNLOAD_DIR = "/tmp"

@app.route('/')
def home():
    return "🎵 SongNest MP3 Backend is Live!"

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is missing"}), 400

    try:
        filename = str(uuid.uuid4()) + ".mp3"
        output_path = os.path.join(DOWNLOAD_DIR, filename)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path.replace(".mp3", ".%(ext)s"),
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        final_path = output_path
        return send_file(final_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
