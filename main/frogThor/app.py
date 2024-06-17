from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import pygame
import threading
import time

app = Flask(__name__)
CORS(app)

music_dir = r'C:\Users\10843\OneDrive\文档\GitHub\evocative-nexus-426416-k0\output\5500-words\en-US-Journey-D'
music_explain_dir = r'C:\Users\10843\OneDrive\文档\GitHub\evocative-nexus-426416-k0\output\5500-words-and-explain'
music_files = [f for f in os.listdir(music_dir) if f.endswith((".mp3", ".wav"))]
current_track = 0
playing = False
shuffle = False
loop = False

pygame.mixer.init()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/music_files', methods=['GET'])
def get_music_files():
    return jsonify(music_files)


@app.route('/play', methods=['POST'])
def play():
    global playing, current_track
    track = request.json.get('track')
    current_track = music_files.index(track)
    file_path = os.path.join(music_dir, track)
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    playing = True
    return jsonify({"status": "playing", "track": track})


@app.route('/pause', methods=['POST'])
def pause():
    global playing
    if playing:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    playing = not playing
    return jsonify({"status": "paused" if not playing else "playing"})


@app.route('/stop', methods=['POST'])
def stop():
    global playing
    pygame.mixer.music.stop()
    playing = False
    return jsonify({"status": "stopped"})


@app.route('/toggle_loop', methods=['POST'])
def toggle_loop():
    global loop
    loop = not loop
    return jsonify({"loop": loop})


@app.route('/toggle_shuffle', methods=['POST'])
def toggle_shuffle():
    global shuffle
    shuffle = not shuffle
    return jsonify({"shuffle": shuffle})


@app.route('/select_all', methods=['POST'])
def select_all():
    selected_indices = request.json.get('selected_indices')
    return jsonify({"selected_indices": selected_indices})


@app.route('/explain/<track>', methods=['GET'])
def get_explain(track):
    explain_file = f'{music_explain_dir}/{track}.txt'
    if os.path.exists(explain_file):
        with open(explain_file, 'r', encoding='utf-8') as file:
            content = file.read()
        return jsonify({"content": content})
    else:
        return jsonify({"content": ''})


def run_scheduler():
    while True:
        if loop and not pygame.mixer.music.get_busy():
            file_path = os.path.join(music_dir, music_files[current_track])
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
        time.sleep(1)


scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

if __name__ == '__main__':
    app.run(port=80, debug=True)
