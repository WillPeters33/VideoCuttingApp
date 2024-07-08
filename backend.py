from flask import Flask, render_template, jsonify, request, send_file, abort
import psutil
import subprocess
import os
import lightDetect
from flask_socketio import SocketIO, emit
import zipfile
import io


for file in os.listdir('inputVids'):
    os.remove('inputVids/' + file)
for file in os.listdir('outputVids'):
    os.remove('outputVids/' + file)

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'inputVids'
app.config['OUTPUT_FOLDER'] = 'outputVids'

socketio = SocketIO(app)

def ack():
    print('emit was received!')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        print('No file part')
        return jsonify('No file part'), 400
    
    files = request.files.getlist('files[]')
    for file in files:
        filename = file.filename
        pos = filename.find('/')
        if pos != -1:
            filename = filename[pos+1:]
        if filename == '' or (not '.mp4' in filename and not '.m4a' in filename and not '.avi' in filename and not '.m4v' in filename):
            continue
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(filename + ' uploaded')
    if not os.listdir('inputVids'):
        print('No files of correct type uploaded')
        return jsonify('No files of correct type uploaded'), 400
    return jsonify({'upload_done'}), 200

@app.route('/process', methods=['POST'])
def process_file():
    # Files Successfully Uploaded, Time to Process them
    iteration = 0
    i = 0
    total_files = len(os.listdir('inputVids'))
    print("emit upload_done")
    socketio.emit('upload_done', {}, callback=ack)
    for filename in os.listdir('inputVids'):
        print(filename)
        socketio.emit('upload_progress', {'progress': (i + 1) / float(total_files) * 100}, callback=ack)
        iteration = lightDetect.lightDetect(iteration, filename)
        i += 1
    return jsonify({}), 200

@app.route('/download_all')
def download_all():
    iteration = 0
    # Create an in-memory zip file
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for video in os.listdir(app.config['OUTPUT_FOLDER']):
            if video.endswith(('.mp4', '.avi', '.mkv')):
                video_path = os.path.join(app.config['OUTPUT_FOLDER'], video)
                zf.write(video_path, arcname=video)
    memory_file.seek(0)
    return send_file(memory_file, download_name='cut_videos.zip')

if __name__ == '__main__':
    app.debug = True
    socketio.run(app)
    # Start App Using this: waitress-serve --listen=127.0.0.1:5000

