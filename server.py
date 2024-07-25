from flask import Flask, request, jsonify
import yt_dlp

def get_streams(url):
    ydl = yt_dlp.YoutubeDL()
    info = ydl.extract_info(url, download=False)
    formats = [{"format_id": format['format_id'], "url": format['url']} for format in info['formats']]
    return formats

app = Flask(__name__)

@app.post('/song')
def get_song_streams():
    data = request.json
    song_id = data.get('songid')
    if not song_id:
        return jsonify({"error": "Missing songid parameter"}), 400
    
    try:
        streams = get_streams(f"https://www.youtube.com/watch?v={song_id}")
        for a in streams:
            if(a["format_id"] == "250"):
                audiostream = a["url"]
                break
        return jsonify(audiostream)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
