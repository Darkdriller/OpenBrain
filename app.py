from flask import Flask, request, render_template, redirect, url_for, send_file
import plotly
import plotly.graph_objs as go
import pandas as pd
import csv
import os
import json
import time
import graph # Import the functions from graph.py

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
    # Here you would generate your 3D plot based on the uploaded file
    # For demonstration, we're generating a static 3D scatter plot
    filename = r"C:\Users\Akhbar\Downloads\OpenBrain-main\OpenBrain-main\files\BG001.swc"
    neuron_data = graph.read_swc(filename)
    fig = graph.plot_neuron(neuron_data)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('display_graph.html', graphJSON=graphJSON)

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

if __name__ == '__main__':
    app.run(debug=True)
