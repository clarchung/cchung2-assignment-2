import numpy as np

class KMeans:
    def __init__(self, n_clusters=3, init_method="random"):
        self.n_clusters = n_clusters
        self.init_method = init_method
        self.centroids = None
        self.assignments = None

    def initialize_centroids(self, data_points):
        #initialize centroids
        if self.init_method == "random":
            self.centroids = self._init_random(data_points)
        elif self.init_method == "farthest_first":
            self.centroids = self._init_farthest_first(data_points)
        elif self.init_method == "kmeans++":
            self.centroids = self._init_kmeans_plus_plus(data_points)
        elif self.init_method == "manual":
            self.centroids = []  # user input 
        return self.centroids

    def _init_random(self, data_points):
        #chose random centroid
        random_indices = np.random.choice(data_points.shape[0], self.n_clusters, replace=False)
        return data_points[random_indices]

    def _init_farthest_first(self, data_points):
        #choose random centroid first 
        centroids = []
        first_idx = np.random.randint(0, data_points.shape[0])
        centroids.append(data_points[first_idx])
        #find centroid with greatest distance 
        for _ in range(1, self.n_clusters):
            dists = np.array([min([np.linalg.norm(p - c) for c in centroids]) for p in data_points])
            next_centroid = data_points[np.argmax(dists)]
            centroids.append(next_centroid)

        return np.array(centroids)

    def _init_kmeans_plus_plus(self, data_points):
        #choose random centroid 
        centroids = []
        first_idx = np.random.randint(0, data_points.shape[0])
        centroids.append(data_points[first_idx])
        #choose centroid based on probability 
        for _ in range(1, self.n_clusters):
            dists = np.array([min([np.linalg.norm(p - c)**2 for c in centroids]) for p in data_points])
            probs = dists / np.sum(dists)
            next_idx = np.random.choice(data_points.shape[0], p=probs)
            centroids.append(data_points[next_idx])

        return np.array(centroids)

    def assign_clusters(self, data_points):
        #assign each point in data_points to nearest cluster 
        self.assignments = np.array([self._closest_centroid(point) for point in data_points])

    def _closest_centroid(self, point):
        #finds index of closest centroid to a given point 
        distances = np.linalg.norm(point - self.centroids, axis=1)
        return np.argmin(distances)

    def update_centroids(self, data_points):
        #updates centroids based on cluster assignments 
        new_centroids = []
        for k in range(self.n_clusters):
            cluster_points = data_points[self.assignments == k]
            if len(cluster_points) > 0:
                new_centroids.append(np.mean(cluster_points, axis=0))
            else:
                new_centroids.append(self.centroids[k])  # keep  same centroid if the cluster is empty
        self.centroids = np.array(new_centroids)

    def step(self):
        #assign clusters and update centroids 
        self.assign_clusters(self.centroids)
        self.update_centroids(self.centroids)

    def run_to_completion(self, data_points, max_iters=100):
        #run algorithm until convergence or max num iterations is reached 
        for _ in range(max_iters):
            old_centroids = np.copy(self.centroids)
            self.assign_clusters(data_points)
            self.update_centroids(data_points)

            if np.all(old_centroids == self.centroids):  # Convergence check
                break
