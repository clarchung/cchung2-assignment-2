let data_points = [];
let centroids = [];

// Function to plot data points and centroids
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
        yaxis: { title: 'Y' },
        clickmode: 'event+select' // Enable click events on the plot
    };

    Plotly.newPlot('plot', [trace1, trace2], layout);

    // Event listener for manual centroid selection
    const plotDiv = document.getElementById('plot');
    plotDiv.on('plotly_click', function(data) {
        const point = data.points[0];
        const selectedPoint = [point.x, point.y];

        // Only process manual selection if the selected method is manual
        if (document.getElementById('init_method').value === 'manual') {
            fetch('/manual_select', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ points: [selectedPoint] })
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
                // Optionally, you can add the new centroid to the centroids array and re-plot
                centroids.push(selectedPoint);
                plotData(); // Re-plot to show the newly added centroid
            });
        } else {
            alert("Switch to 'Manual' initialization method to select centroids.");
        }
    });
}

// Function to generate new data points
function generateData() {
    fetch('/generate_data', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            data_points = data;
            plotData();
        });
}

// Function to initialize centroids based on the selected method
function initialize() {
    let method = document.getElementById('init_method').value;
    fetch('/initialize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ method: method })
    })
    .then(response => response.json())
    .then(data => {
        centroids = data;
        plotData();
    });
}

// Function to step through the KMeans algorithm
function step() {
    fetch('/step', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            centroids = data.centroids;
            plotData();
        });
}

// Function to run the algorithm to completion
function runToCompletion() {
    fetch('/run_to_completion', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            centroids = data.centroids;
            plotData();
        });
}

// Function to reset the plot and data
function reset() {
    data_points = [];
    centroids = [];
    Plotly.purge('plot');
}
