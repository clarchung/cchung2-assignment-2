from flask import Flask, render_template, jsonify, request
import numpy as np
from kmeans import KMeans 
import plotly.graph_objects as go

app = Flask(__name__)

# Store dataset and centroids globally
data_points = None
centroids = None
kmeans = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_data', methods=['POST'])
def generate_data():
    global data_points
    num_points = 100
    data_points = np.random.rand(num_points, 2) * 10
    return jsonify(data_points.tolist())

@app.route('/initialize', methods=['POST'])
def initialize():
    global centroids, kmeans
    init_method = request.json.get('method')
    kmeans = KMeans(n_clusters=3, init_method=init_method)
    centroids = kmeans.initialize_centroids(data_points)
    return jsonify(centroids.tolist())

@app.route('/step', methods=['POST'])
def step():
    global data_points, centroids, kmeans
    kmeans.step()
    centroids = kmeans.centroids
    return jsonify({
        'data_points': data_points.tolist(),
        'centroids': centroids.tolist(),
        'assignments': kmeans.assignments.tolist()
    })

@app.route('/run_to_completion', methods=['POST'])
def run_to_completion():
    global centroids, kmeans
    kmeans.run_to_completion()
    centroids = kmeans.centroids
    return jsonify({
        'data_points': data_points.tolist(),
        'centroids': centroids.tolist(),
        'assignments': kmeans.assignments.tolist()
    })

@app.route('/manual_select', methods=['POST'])
def manual_select():
    global centroids
    selected_points = request.json.get('points')
    
    # Update centroids based on user-selected points
    centroids = np.array(selected_points)
    
    return jsonify({'message': 'Centroids updated successfully', 'new_centroids': centroids.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
