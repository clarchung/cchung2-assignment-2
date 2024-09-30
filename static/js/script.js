let data_points = [];
let centroids = [];

function showMessage(msg) {
    const messageDiv = document.getElementById('message');
    messageDiv.innerText = msg;
}

function plotData() {
    let trace1 = {
        x: data_points.map(p => p[0]),
        y: data_points.map(p => p[1]),
        mode: 'markers',
        type: 'scatter',
        name: 'Data Points',
        marker: { size: 8 }
    };

    let trace2 = {
        x: centroids.map(c => c[0]),
        y: centroids.map(c => c[1]),
        mode: 'markers',
        type: 'scatter',
        name: 'Centroids',
        marker: { size: 10, color: 'red' }
    };

    let layout = {
        title: 'KMeans Clustering',
        xaxis: { title: 'X' },
        yaxis: { title: 'Y' }
    };

    Plotly.newPlot('plot', [trace1, trace2], layout);
}

function generateData() {
    fetch('/generate_data', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            data_points = data;
            plotData();
            showMessage("New data generated!");
        });
}

function initialize() {
    let method = document.getElementById('init_method').value;
    fetch('/initialize_kmeans', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: data_points, k: 3, initialization: method })
    })
    .then(response => response.json())
    .then(data => {
        centroids = data.centroids;
        plotData();
        showMessage("Centroids initialized!");
    });
}

// Implement similar functions for step, run_to_completion, etc.
