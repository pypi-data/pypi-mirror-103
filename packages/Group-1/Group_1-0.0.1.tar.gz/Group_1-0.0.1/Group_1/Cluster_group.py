import numpy as np
import pandas as pd

import tensorflow as tf
import tensorflow.keras.backend as K
import tensorflow.keras.layers as L
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.keras.models import Model

from sklearn.cluster import KMeans as kmeans
from sklearn import metrics

# Module for Emmanuel
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler

# style.use('ggplot')

import math
import random
from sklearn import datasets

import collections
#from utils import CorrelationClusteringError


def autoencoder(DIM, act='relu', initializer='glorot_uniform'):
    inp = L.Input(shape=(DIM[0],), name='input_')
    e = inp

    # Encoding Layers
    for i in range(len(DIM) - 2):
        e = L.Dense(DIM[i + 1], act, kernel_initializer=initializer, name="encoding_layer_%i" % (i))(e)

    e = L.Dense(DIM[-1], kernel_initializer=initializer, name='encoder_output')(e)
    encoder_out = e

    d = e
    # Decoding Layers
    for i in range(len(DIM) - 2, 0, -1):
        d = L.Dense(DIM[i], act, kernel_initializer=initializer, name="decoding_layer_%i" % (i))(d)

    decoder_out = L.Dense(DIM[0], kernel_initializer=initializer, name='decoder_ouput')(d)

    encoder = Model(inp, encoder_out, name="Encoder")
    autoencoder = Model(inp, decoder_out, name="Autoencoder")

    return autoencoder, encoder


class ClusteringLayer(tf.keras.layers.Layer):

    def __init__(self, nclusters, weights=None, alpha=1.0, **kwargs):
        if 'input_shape' not in kwargs and 'input_dim' in kwargs:
            kwargs['input_shape'] = (kwargs.pop('input_dim'),)
        super().__init__(**kwargs)
        self.nclusters = nclusters
        self.init_weights = weights
        self.alpha = alpha

    def build(self, input_shape):
        self.inp_dim = input_shape[1]
        self.clusters = self.add_weight(shape=(self.nclusters, self.inp_dim), initializer='glorot_uniform',
                                        name='clusters')
        if self.init_weights is not None:
            self.set_weights(self.init_weights)
            self.built = True

    def call(self, inputs, **kwargs):
        q = 1.0 / (1.0 + (K.sum(K.square(K.expand_dims(inputs, axis=1) - self.clusters), axis=2) / self.alpha))
        q = K.pow(q, (self.alpha + 1.0) / 2.0)
        q = K.transpose(K.transpose(q) / K.sum(q, axis=1))
        return q


class DEC(object):

    def __init__(self, DIM, nclusters=10, alpha=1.0, initializer='glorot_uniform'):
        self.DIM = DIM
        self.input_dim = DIM[0]
        self.nclusters = nclusters
        self.alpha = alpha
        self.autoencoder, self.encoder = autoencoder(DIM, initializer=initializer)

        clustering_layer = ClusteringLayer(self.nclusters, name='cluster_layer')(self.encoder.output)
        self.model = Model(inputs=self.encoder.input, outputs=clustering_layer)

    def train_autoencoder(self, x, optimizer='adam', epochs=100, batch_size=256, dir=None):
        self.autoencoder.compile(optimizer=optimizer, loss='mse')
        hist = self.autoencoder.fit(x, x, epochs=epochs, batch_size=batch_size, verbose=0)
        print("loss : %.5f" % hist.history["loss"][-1])
        self.autoencoder.save_weights(dir + "/autoencoder_weights.h5")
        print("Weights saved to %s/autoencoder_weights.h5" % (dir))

    def target_distribution(self, q):
        weight = q ** 2 / q.sum(0)
        return (weight.T / weight.sum(1)).T

    def compile(self, optimizer='sgd', loss='kld'):
        self.model.compile(optimizer=optimizer, loss=loss)

    def predict(self, x):
        q = self.model.predict(x)
        return np.argmax(q, axis=1)

    def fit(self, x, y=None, epochs=200, batch_size=256, dir=None):
        print('Initializing cluster centers with k-means.........')
        km = kmeans(n_clusters=self.nclusters, n_init=5)
        y_pred = km.fit_predict(self.encoder.predict(x))
        self.model.summary()
        self.model.get_layer('cluster_layer').set_weights([km.cluster_centers_])
        loss = 0
        indx = 0
        idx_arr = np.arange(x.shape[0])

        for i in range(epochs):
            q = self.model.predict(x)
            p = self.target_distribution(q)
            idx = idx_arr[indx * batch_size:min((indx + 1) * batch_size, x.shape[0])]
            loss = self.model.train_on_batch(x[idx], p[idx])
            indx = indx + 1 if (indx + 1) * batch_size <= x.shape[0] else 0
        print('Loss : %.5f' % loss)
        print('saving model to:', dir + "/DEC_model.h5")
        self.model.save_weights(dir + "/DEC_model.h5")


np.seterr(divide='ignore', invalid='ignore')
style.use('ggplot')
"""
Author Emmmanuel Bonsu.
This class implements the tradition K Means Algorithm
"""

class KMeans:
    def __init__(self, k=2, iterations=200, tolerance=0.001):
        self.k = k
        self.iterations = iterations
        self.classifications = {}
        self.centroids = {}
        self.tolerance = tolerance

    def fit(self, data_frame):
        # Optimization: Initializing centroid based on data distribution
        self.centroids = self.initialize_centroids(data_frame)

        data = data_frame.to_numpy()
        centroid = 0
        while centroid < self.k:
            # to assign random numbers. first shuffle and pick the first 2
            self.centroids[centroid] = data[centroid]
            centroid += 1

        for iteration in range(1, self.iterations):
            print(iteration)

            # Initialize clusters to empty lists
            self.initialize_clusters()

            for sample in data:
                distance_to_clusters = [np.linalg.norm(sample - self.centroids[centroid]) for centroid in
                                        self.centroids]
                classification = distance_to_clusters.index(min(distance_to_clusters))
                self.classifications[classification].append(sample)
            prev_centroids = dict(self.centroids)

            for classification in self.classifications:
                self.centroids[classification] = np.average(self.classifications[classification], axis=0)

            # Stopping Criteria
            optimized = True
            for index in self.centroids:
                previous_centroid = prev_centroids[index]
                current_centroid = self.centroids[index]
                if np.sum((current_centroid - previous_centroid) / previous_centroid * 100.0) > self.tolerance:
                    print(np.sum((current_centroid - previous_centroid) / previous_centroid * 100.0))
                    optimized = False

            if optimized:
                break

    def predict(self, data):
        distance_to_clusters = [np.linalg.norm(data - self.centroids[centroid]) for centroid in self.centroids]
        cluster_group = distance_to_clusters.index(min(distance_to_clusters))
        return cluster_group

    def initialize_centroids(self, data_frame):
        max_column = (data_frame.max() - data_frame.min()).idxmax()
        df_sorted = data_frame.sort_values(by=[max_column])
        df_partition = np.array_split(df_sorted, self.k)
        df_mean = [np.mean(arr) for arr in df_partition]
        centroid_dict = {}
        for index in range(self.k):
            centroid_dict[index] = df_mean[index]
        return centroid_dict

    def initialize_clusters(self):
        for cluster in range(self.k):
            self.classifications[cluster] = []

    def display_result(self):
        colors = 10 * ["g", "r", "c", "b", "k"]
        for centroid in self.centroids:
            plt.scatter(self.centroids[centroid][0], self.centroids[centroid][1],
                        marker="o", color="k", s=150, linewidths=5)

        for classification in self.classifications:
            color = colors[classification]
            for featureset in self.classifications[classification]:
                plt.scatter(featureset[0], featureset[1], marker="x", color=color, s=150, linewidths=5)

        plt.show()

"""
Author: Emmanuel Bonsu
The class implements the EnhancedCentroidInitialization clustering algorithm
"""
class EnhancedCentroidInitialization:
    def __init__(self, k=2, iterations=200, tolerance=0.000001):
        self.k = k
        self.iterations = iterations
        self.classifications = {}
        self.centroids = {}
        self.tolerance = tolerance

    def fit(self, data_frame):
        # Optimization: Initializing centroid based on data distribution
        self.centroids = self.initialize_centroids(data_frame)
        print('INITIALIZATION', self.centroids)

        data = data_frame.to_numpy()

        for iteration in range(1, self.iterations):
            print(iteration)

            # Initialize clusters to empty lists
            self.initialize_clusters()

            for sample in data:
                distance_to_clusters = [np.linalg.norm(sample - self.centroids[centroid]) for centroid in
                                        self.centroids]
                classification = distance_to_clusters.index(min(distance_to_clusters))
                self.classifications[classification].append(sample)
            prev_centroids = dict(self.centroids)

            for classification in self.classifications:
                self.centroids[classification] = np.average(self.classifications[classification], axis=0)

            # Stopping Criteria
            optimized = True
            for index in self.centroids:
                previous_centroid = prev_centroids[index]
                current_centroid = self.centroids[index]
                if np.sum((current_centroid - previous_centroid) / previous_centroid * 100.0) > self.tolerance:
                    print(np.sum((current_centroid - previous_centroid) / previous_centroid * 100.0))
                    optimized = False

            if optimized:
                break

    def predict(self, data):
        distance_to_clusters = [np.linalg.norm(data - self.centroids[centroid]) for centroid in self.centroids]
        cluster_group = distance_to_clusters.index(min(distance_to_clusters))
        return cluster_group

    def initialize_centroids(self, data_frame):
        max_column = (data_frame.max() - data_frame.min()).idxmax()
        print("ranges", data_frame.max() - data_frame.min())
        print(max_column)
        df_sorted = data_frame.sort_values(by=[max_column], kind='heapsort')  # Use kind = 'heapSort'
        # Re-indexing ensures that splitting in done vertically, therefore preserving the order of sorting
        # df_sorted = df_sorted.reset_index().drop("index", axis=1)
        df_partition = np.array_split(df_sorted, self.k)  # Change to vsplit
        df_mean = [arr.mean() for arr in df_partition]  # Double Check like your life depends on it
        centroid_dict = {}
        for index in range(self.k):
            centroid_dict[index] = df_mean[index].to_numpy()
        return centroid_dict

    def initialize_clusters(self):
        for cluster in range(self.k):
            self.classifications[cluster] = []

    def display_result(self):
        colors = ["g", "r", "c", "b", "y", "m", "g", "c"]
        plt.figure(figsize=(15, 15), dpi=80)
        for centroid in self.centroids:
            plt.scatter(self.centroids[centroid][0], self.centroids[centroid][1],
                        marker="o", color="k", s=300, linewidths=5, label=centroid)

        for classification in self.classifications:
            color = colors[classification]
            for featureset in self.classifications[classification]:
                plt.scatter(featureset[0], featureset[1], marker="o", color=color, s=50, linewidths=5)
        plt.show()

    def calculate_accuracy(self, df, labels):
        result = []
        for data in df.values:
            cl = self.predict(data)
            result.append(cl)
        matrix = confusion_matrix(labels, result)
        print('**************** DISPLAYING CONFUSION MATRIX **************')
        print(matrix)
        print('**************** CALCULATING ACCURACY OF CLUSTER ******************')
        correct_predictions = 0
        for arr in matrix:
            correct_predictions += max(arr)
        print('ACCURACY: ', correct_predictions / len(labels))


# This clustering algorithm is implemented by Jiaming Chen
class improved_Cluster:
        
    def Eu_Distance(self, dataOne, dataTwo):
        """
        computing the Euclidean distance for each instances
        """
        distance = 0
        for i in range(len(dataOne)):
            distance += pow(dataOne[i] - dataTwo[i], 2)
        return math.sqrt(distance)
    
    #step1 generate first cluster center randomly within data
    def first_center(self, data):
        first_C = random.choice(data)
        return first_C

    def predict(self, data, Theta=0.5):
        
        maxDistance = 0
        # initially choosing a centre.
        index = 0
        # store number of clusters
        k = 0

        data_Num = len(data) # number of samples
        distance = np.zeros((data_Num,))
        minDistance = np.zeros((data_Num,))
        classes = np.zeros((data_Num,))
        centerIndex = [index]

        # choose the first center of cluster within data randomly
        first_C = self.first_center(data)

        # find the second centre of cluster
        for i in range(len(data)):
            ptr1 = data[i]
            d = self.Eu_Distance(ptr1, first_C) # compute eu distance
            distance[i] = d
            classes[i] = k
            if (maxDistance < d):
                maxDistance = d
                # locate the instance which have maximum distance.
                index = i
#             print("distance between first with cluster", distance[i])
                

        minDistance = distance.copy()
        maxVal = maxDistance
#         print(maxDistance)
        while maxVal > (maxDistance * Theta):
            k += 1
            centerIndex += [index] # new cluster centre
            for i in range(data_Num):
                ptr1 = data[i]
                first_C = data[centerIndex[k]]
                d = self.Eu_Distance(ptr1, first_C)
                distance[i] = d

                if minDistance[i] > distance[i]:
                    minDistance[i] = distance[i]
                    classes[i] = k
            '''
            search maximum value within minDistance, 
            if maxVal > (maxDistance * Theta) means existing next cluster centre
            '''
            index = np.argmax(minDistance)
            maxVal = minDistance[index]
        return classes, centerIndex
    
    def acc_clustering(self, cm, y):
        df = pd.DataFrame(cm)
        true = 0
        max_val = []
        for col in df:
            sorted = df[col].sort_values(ascending = False)
            i = 0
            while sorted.index[i] in max_val:
                i += 1
            true += sorted.values[i]
            max_val.append(sorted.index[i])
        accuracy = (true/len(y))*100
        return accuracy


# This clustering algorithm is implemented by Jiajing Chen
class MyKmeans(object):
    
    def __init__(self, n_class, n_iter, tol=1e-10):
        self.n_class = n_class
        self.n_iter = n_iter
        self.tol = tol
    
    def distance(self, x1, x2):
        return np.sqrt(np.sum((x1-x2)**2))
    
    def fit(self, X):
        ''' X by row '''
        X = np.array(X)
        n = X.shape[0]
        
        # initialization
        center = np.random.choice(n, self.n_class, replace=False)  # which are center
        center = [X[c] for c in center]
        label = np.array(list(map(lambda x : np.argmin([self.distance(x, xc) for xc in center]), X)))
        
        for _ in range(self.n_iter):
            center_old = center.copy()
            # new center
            for c in range(self.n_class):
                idx = (label == c)
                center[c] = np.mean(X[idx], axis=0)
                label = np.array(list(map(lambda x : np.argmin([self.distance(x, xc) for xc in center]), X)))
            # whether center changes
            change_cnt_dist = 0
            for i in range(self.n_class):
                change_cnt_dist += self.distance(center_old[i], center[i])
            if change_cnt_dist < self.tol:
                # print("tolerance achieve : ", _)
                break

        self.center = center
        self.label = self.predict(X)
        
        return self
    
    def predict(self, X):
        label = np.array(list(map(lambda x : np.argmin([self.distance(x, xc) for xc in self.center]), X)))
        return label


class MyBlob(object):

    def __init__(self, center=((0,0), (1,1)), sd=((0.1,0.1), (0.1,0.1))):
        self.center = center
        self.sd = sd
        self.d = len(self.center[0])

    def make_blob(self, n=(50, 50)):
        blobs = []
        for i in range(len(n)):
            blob_tmp = np.random.randn( n[i], self.d )

            for j in range( self.d ):
                blob_tmp[:, j] = self.sd[i][j] * blob_tmp[:, j] + self.center[i][j]
            
            blobs.extend( blob_tmp.tolist() )

        return blobs


def MMM(kfrom, kto):
    ''' calculate MMM index for optimal k selection
    :param kfrom: labels of keams with k
    :param kto:   labels of keans with k+1 or k-1
    :return:      transition matrix from k to k+1 or k-1 (with the sum of row is 1)
    '''
    label_from, label_to = np.unique(kfrom), np.unique(kto)
    transition_matrix = np.zeros((len(label_from), len(label_to)))
    for i in range(len(label_from)):
        idx = kto[kfrom == label_from[i]]
        for j in range(len(label_to)):
            transition_matrix[i, j] = np.mean(idx == label_to[j])
            
    return transition_matrix


def PivotAlgorithm(graph):
    """The well-known pivot algorithm for correlation clustering.

    Run the pivot algorithm on graph.
    Args:
      graph: the graph in nx.Graph format.
    Returns:
      The solution.
    """
    # This is to ensure consistency of random runs with same seed.
    nodes = sorted(list(graph.nodes()))
    random.shuffle(nodes)
    clusters = []
    clustered = set()

    for node in nodes:
        if node in clustered:
            continue
        cluster = [node]
        clustered.add(node)

        for neighbor in graph.neighbors(node):
            if graph.edges[node,
                           neighbor]['weight'] > 0 and neighbor not in clustered:
                cluster.append(neighbor)
                clustered.add(neighbor)
        clusters.append(cluster)
    assert len(clustered) == sum(len(c) for c in clusters)
    assert clustered == set(nodes)
    return clusters


def LocalSearchAlgorithm(graph, attempts=10):
    """Run the local search heuristic for correlation clustering.

    The algorithm is a simple local search heuristic that tries to improve the
    clustering by local moves of individual nodes until a certain number of
    iterations over the graph are completed.

    Args:
      graph: the graph in nx.Graph format.
      attempts: number of times local search is run.
    Returns:
      The solution.
    """
    best_sol = None
    best_sol_value = None
    for _ in range(attempts):
        ls = LocalSearchCorrelationClustering(graph, 20)
        sol = ls.RunClustering()
        cost = CorrelationClusteringError(graph, sol)
        if best_sol_value is None or best_sol_value > cost:
            best_sol_value = cost
            best_sol = sol
    return best_sol


# This algorithm is implemented by Faizan Butt
def PivotAlgorithm(graph):
    """The well-known pivot algorithm for correlation clustering.

    Run the pivot algorithm on graph.
    Args:
      graph: the graph in nx.Graph format.
    Returns:
      The solution.
    """
    # This is to ensure consistency of random runs with same seed.
    nodes = sorted(list(graph.nodes()))
    random.shuffle(nodes)
    clusters = []
    clustered = set()

    for node in nodes:
        if node in clustered:
            continue
        cluster = [node]
        clustered.add(node)

        for neighbor in graph.neighbors(node):
            if graph.edges[node,
                           neighbor]['weight'] > 0 and neighbor not in clustered:
                cluster.append(neighbor)
                clustered.add(neighbor)
        clusters.append(cluster)
    assert len(clustered) == sum(len(c) for c in clusters)
    assert clustered == set(nodes)
    return clusters


def LocalSearchAlgorithm(graph, attempts=10):
    """Run the local search heuristic for correlation clustering.

    The algorithm is a simple local search heuristic that tries to improve the
    clustering by local moves of individual nodes until a certain number of
    iterations over the graph are completed.

    Args:
      graph: the graph in nx.Graph format.
      attempts: number of times local search is run.
    Returns:
      The solution.
    """
    best_sol = None
    best_sol_value = None
    for _ in range(attempts):
        ls = LocalSearchCorrelationClustering(graph, 20)
        sol = ls.RunClustering()
        cost = CorrelationClusteringError(graph, sol)
        if best_sol_value is None or best_sol_value > cost:
            best_sol_value = cost
            best_sol = sol
    return best_sol


class LocalSearchCorrelationClustering(object):
    """Single run of the the local search heuristic for correlation clustering.

    The algorithm performs a series of passes over the nodes in the graph in
    arbitrary order.
    For each node in the order, it checks if the solution can be improved by
    moving the node to another cluster.
    """

    def __init__(self, graph, iterations):
        self.graph = graph
        self.iterations = iterations
        self.node_to_cluster_id = {}
        self.cluster_uid = 0
        self.cluster_id_nodes = collections.defaultdict(set)
        for node in self.graph.nodes():
            self.node_to_cluster_id[node] = self.cluster_uid
            self.cluster_id_nodes[self.cluster_uid].add(node)
            self.cluster_uid += 1

    def MoveNodeToCluster(self, node, cluster_id):
        """Moves a node to a cluster."""
        self.cluster_id_nodes[self.node_to_cluster_id[node]].remove(node)
        self.node_to_cluster_id[node] = cluster_id
        self.cluster_id_nodes[cluster_id].add(node)

    def DoOnePassMoves(self):
        """Completes one pass over the graph."""
        nodes = sorted(list(self.graph.nodes()))
        random.shuffle(nodes)
        for node in nodes:
            positive_to_clusters = collections.defaultdict(int)
            best_cluster = None
            best_cluster_cost = self.graph.number_of_nodes() + 1
            positives = 0
            for neighbor in self.graph.neighbors(node):
                if self.graph.edges[node, neighbor]['weight'] > 0:
                    positives += 1
                    positive_to_clusters[self.node_to_cluster_id[neighbor]] += 1
            curr_cluster = self.node_to_cluster_id[node]
            curr_cluster_cost = positives + len(
                self.cluster_id_nodes[curr_cluster]
            ) - 1 - 2 * positive_to_clusters[curr_cluster]
            for c, pos in positive_to_clusters.items():
                if c != curr_cluster:
                    cluster_cost = positives + len(self.cluster_id_nodes[c]) - 2 * pos
                    if cluster_cost < best_cluster_cost:
                        best_cluster_cost = cluster_cost
                        best_cluster = c

            if best_cluster_cost < curr_cluster_cost:
                self.MoveNodeToCluster(node, best_cluster)

    def RunClustering(self):
        for _ in range(self.iterations):
            self.DoOnePassMoves()
        return self.cluster_id_nodes.values()
