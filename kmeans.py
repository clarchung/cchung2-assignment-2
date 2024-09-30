# kmeans.py
import random
import math

class KMeans:
    def __init__(self, k, max_iterations=100):
        self.k = k
        self.max_iterations = max_iterations
        self.centroids = []
        self.clusters = []

    @staticmethod
    def euclidean_distance(point1, point2):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2)))

    def kmeans_single_step(self, data):
        self.clusters = [[] for _ in range(self.k)]

        for point in data:
            distances = [self.euclidean_distance(point, centroid) for centroid in self.centroids]
            closest_index = distances.index(min(distances))
            self.clusters[closest_index].append(point)

        new_centroids = []
        for cluster in self.clusters:
            if cluster:
                new_centroid = [sum(coord) / len(cluster) for coord in zip(*cluster)]
                new_centroids.append(new_centroid)
            else:
                new_centroids.append(random.choice(data))

        self.centroids = new_centroids

    def run(self, data):
        # Initialize centroids randomly from the data
        self.centroids = random.sample(data, self.k)
        
        for _ in range(self.max_iterations):
            old_centroids = self.centroids[:]
            self.kmeans_single_step(data)
            if self.centroids == old_centroids:
                break  # Convergence
        return self.centroids, self.clusters
