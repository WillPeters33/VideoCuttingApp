from flask import Flask, render_template, jsonify, request, send_file, abort
import psutil
import threading
import os
import lightDetect
from flask_socketio import SocketIO, emit
import zipfile
import io
import sys

progress = 0
iteration = 0
lock = threading.Lock()

def process_file_helper():
    global progress
    global iteration
    global lock
    print('Processing Files pid: ', os.getpid())
    lock.acquire()
    # Files Successfully Uploaded, Time to Process them
    total_files = len(os.listdir('inputVids'))
    filename = None
    i = 0
    for file in os.listdir('inputVids'):
        print(i, progress, file)
        if i == progress:
            filename = file
            break
        i += 1
    print(filename)
    iteration = lightDetect.lightDetect(iteration, filename)
    lock.release()
    progress += 1
    print(progress/total_files*100)

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'inputVids'
app.config['OUTPUT_FOLDER'] = 'outputVids'


@app.route('/')
def index():
    lock.acquire()
    lock.release()
    print("Main thread still going")
    global progress
    progress = 0
    global iteration 
    iteration = 0
    lock.acquire()
    for file in os.listdir('inputVids'):
        os.remove('inputVids/' + file)
    for file in os.listdir('outputVids'):
        os.remove('outputVids/' + file)
    lock.release()
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
        return jsonify({'error': 'No files of correct type uploaded'}), 400
    return jsonify({'data': 'upload_done'}), 200

@app.route('/process', methods=['POST'])
def process_file():
    global progress
    global process_to_kill
    total_files = len(os.listdir('inputVids'))
    print('Main pid: ', os.getpid())
    p = threading.Thread(target=process_file_helper)
    p.start()
    p.join()
    return jsonify({'progress': round(progress/total_files*100)}), 200


@app.route('/download_all')
def download_all():
    global progress
    progress = 0
    global iteration 
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
    app.run()
