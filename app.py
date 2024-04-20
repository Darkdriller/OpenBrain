from flask import Flask, request, render_template, redirect, url_for, send_file
import subprocess
import os
import json
import time
import random

app = Flask(__name__)

# Configurations for file uploads
UPLOAD_FOLDER = r"C:\Users\Akhbar\Downloads\OpenBrain-main\OpenBrain-main\uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'nii','gz'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        time.sleep(10)
        return redirect(url_for('display_graph', filename=file.filename))
    return ''

@app.route('/display_graph/<filename>')
def display_graph(filename):
    # Instead of plotting, execute MATLAB script
    matlab_script = "C:/Users/Akhbar/Downloads/OpenBrain-main/OpenBrain-main/fin.m"
    command = ['matlab', '-batch', 'run(\'{}\')'.format(matlab_script)]
    subprocess.call(command)
    # Redirect to the result route after executing the script
    return redirect(url_for('result'))

@app.route('/result')
def result():
    # Define the directory path
    directory = r'C:\Users\Akhbar\Downloads\OpenBF Results\Flow-000'

    # Randomly select one of the prefixes
    selected_prefix = random.choice([f'v{i}' for i in range(5,11)])

    # Find all files with the selected prefix
    selected_files = [f for f in os.listdir(directory) if f.startswith(selected_prefix) and not f.endswith('_c.last')]

    # Plot each selected file
    plots = []
    for file_name in selected_files:
        file_path = os.path.join(directory, file_name)
        data = read_data_from_file(file_path)
        plots.append(plot_data(data, file_name))

    return render_template('result.html', plots=plots)

@app.route('/export_points', methods=['POST'])
def export_points():
    points = request.form.getlist('points[]')
    with open('selected_points.csv', 'w', newline='') as csvfile:
        pointwriter = csv.writer(csvfile)
        pointwriter.writerow(['X', 'Y', 'Z'])
        for point in points:
            x, y, z = point.split(',')
            pointwriter.writerow([x, y, z])
    return send_file('selected_points.csv',
                     mimetype='text/csv',
                     attachment_filename='selected_points.csv',
                     as_attachment=True)

def read_data_from_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            row = [float(value) for value in line.strip().split()]
            data.append(row)
    return data

def plot_data(data, file_name):
    # Extract time values and flow values
    time = [row[0] for row in data]
    flows = [[row[i] for row in data] for i in range(1, len(data[0]))]

    # Create traces for each flow
    traces = []
    for i, flow in enumerate(flows):
        traces.append({
            'x': time,
            'y': flow,
            'mode': 'lines+markers',
            'name': f'Flow {i + 1}'
        })

    return {'file_name': file_name, 'traces': traces}

if __name__ == '__main__':
    app.run(debug=True)
