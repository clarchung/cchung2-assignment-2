from flask import Flask, jsonify, request, render_template
import random
from kmeans import KMeans  # Import the KMeans class

app = Flask(__name__)

# KMeans state storage
kmeans_state = {
    'data': [],
    'kmeans': None,  # Store KMeans instance here
    'iteration': 0
}

# Function to generate random 2D data points
def generate_random_data(num_points=100, x_range=(0, 10), y_range=(0, 10)):
    return [[random.uniform(x_range[0], x_range[1]), random.uniform(y_range[0], y_range[1])] for _ in range(num_points)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_data', methods=['POST'])
def generate_data():
    data = generate_random_data()
    kmeans_state['data'] = data
    return jsonify(data)

@app.route('/initialize_kmeans', methods=['POST'])
def initialize_kmeans():
    global kmeans_state
    data = request.json['data']
    k = request.json['k']
    initialization_method = request.json['initialization']

    if initialization_method == 'random':
        initial_centroids = random.sample(data, k)
    elif initialization_method == 'farthest':
        initial_centroids = [random.choice(data)]
        for _ in range(1, k):
            farthest_point = max(data, key=lambda point: min(KMeans.euclidean_distance(point, c) for c in initial_centroids))
            initial_centroids.append(farthest_point)
    elif initialization_method == 'kmeans++':
        initial_centroids = [random.choice(data)]
        for _ in range(1, k):
            distances = [min(KMeans.euclidean_distance(point, c) for c in initial_centroids) for point in data]
            weighted_probabilities = [d / sum(distances) for d in distances]
            next_centroid = random.choices(data, weights=weighted_probabilities)[0]
            initial_centroids.append(next_centroid)
    elif initialization_method == 'manual':
        initial_centroids = request.json['initial_centroids']

    kmeans_state['kmeans'] = KMeans(k)
    kmeans_state['kmeans'].centroids = initial_centroids
    kmeans_state['data'] = data
    kmeans_state['iteration'] = 0
    
    return jsonify({
        'centroids': kmeans_state['kmeans'].centroids,
        'clusters': kmeans_state['kmeans'].clusters
    })

@app.route('/step_kmeans', methods=['POST'])
def step_kmeans():
    global kmeans_state
    kmeans = kmeans_state['kmeans']
    data = kmeans_state['data']
    
    kmeans.kmeans_single_step(data)
    
    kmeans_state['iteration'] += 1
    
    return jsonify({
        'centroids': kmeans.centroids,
        'clusters': kmeans.clusters
    })

@app.route('/run_kmeans_final', methods=['POST'])
def run_kmeans_final():
    global kmeans_state
    data = kmeans_state['data']
    kmeans = kmeans_state['kmeans']
    
    centroids, clusters = kmeans.run(data)
    kmeans_state['iteration'] = kmeans_state['iteration'] + kmeans.max_iterations  # Update iterations count
    
    return jsonify({
        'centroids': centroids,
        'clusters': clusters
    })

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3000)
