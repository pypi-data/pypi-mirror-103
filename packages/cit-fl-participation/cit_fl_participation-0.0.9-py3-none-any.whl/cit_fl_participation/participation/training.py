from abc import ABC, abstractmethod
from numpy import ndarray
import numpy as np
import random
import math
from scipy.spatial import distance_matrix

class AbstractTrainer(ABC):
    @abstractmethod
    def train(self, import_weights: ndarray, epochs: int) -> (ndarray, int):
        raise NotImplementedError
    
    @abstractmethod
    def training_finished(self, final_weights: ndarray) -> None:
        raise NotImplementedError

##### DCore #####
# trainer
class FederatedDCoreTrainer(AbstractTrainer):
    def __init__(self, X, r1, r2, density_threshold, alpha):
        self.X = X
        self.num_samples = self.X.shape[0]
        self.num_features = self.X.shape[1]

        # DCore parameters
        self.r1 = r1
        self.r2 = r2
        self.density_threshold = density_threshold
        self.alpha = alpha

        self.density_threshold_relation = math.log(self.alpha) + self.num_features * (math.log(self.r2/self.r1))

        # store
        self.dist   = None
        self.labels = np.ones(shape=(self.num_samples), dtype=int)
        self.cpv    = np.zeros(shape=(self.num_samples), dtype=int)
        self.cp     = np.zeros(shape=(self.num_samples), dtype=int)
        self.dens1  = np.zeros(shape=(self.num_samples), dtype=float)
        self.dens2  = np.zeros(shape=(self.num_samples), dtype=float)
        self.lps    = set()
        self.flp    = set()
        self.rcp    = set()
        self.outcp  = set()

        self.to_cluster = None
        self.to_assign  = None

        #normalization
        self.means = None
        self.stds = None

        # federated parameter
        self.id = np.random.randint(0, 9999999)

        self.round_number = 0
    
    def compute_core_points(self) -> None:
        self.dist = distance_matrix(self.X, self.X)

        # compute cpv, dens1, dens2
        for i in range(self.num_samples):
            neigh = list()
            for j in range(self.num_samples):
                if self.dist[i, j] < self.r1:
                    neigh.append(j)
                    self.dens1[i] += 1
                if self.dist[i, j] < self.r2:
                    self.dens2[i] += 1
            # find point nearest the center (mean)
            self.cpv[i] = neigh[np.argmin(np.linalg.norm(self.X[neigh] - np.mean(self.X[neigh], axis=0), axis=1))]

        # compute cp
        for i in range(self.num_samples):
            self.cp[i] = i
            visited = list()
            while self.cp[i] != self.cpv[self.cp[i]] and not self.cp[i] in visited:
                visited.append(self.cp[i])
                self.cp[i] = self.cpv[self.cp[i]]

        # compute lps and flp
        for i in range(self.num_samples):
            if i == self.cp[i]:
                if self.dens1[i] > self.density_threshold:
                    self.lps.add(i)
                    if math.log(self.dens2[i]) < self.density_threshold_relation + math.log(self.dens1[i]):
                        self.flp.add(i)
                else:
                    self.outcp.add(i)

        #compute real core points
        self.rcp = self.lps - self.flp

        # compute points to clutser and points to assign
        self.to_cluster = np.array(list(self.rcp), dtype=int)
        self.to_assign = np.array(list(self.flp), dtype=int)


        
        


    def train(self, import_weights: np.ndarray, epochs: int) -> (np.ndarray, int):
        if self.round_number == 0:
            result = np.mean(self.X, axis=0)
        elif self.round_number == 1:
            self.means = import_weights
            result = np.sum(np.square(self.X - self.means), axis=0) / self.num_samples
        elif self.round_number == 2:
            self.stds = np.sqrt(import_weights)
            self.X = (self.X - self.means) / self.stds
            self.compute_core_points()

            # DEBUG:
            if True:
                self.labels = np.ones(shape=(self.num_samples), dtype=int)
                for idx in self.to_cluster:
                    self.labels[idx] = 2
            
            result = np.concatenate((np.array([[self.id] * self.num_features]), np.array(self.X[self.to_cluster])), axis=0)
        else:
            result = np.array([])

        self.round_number = self.round_number + 1

        return (result, self.num_samples)

    def training_finished(self, final_weights: np.ndarray) -> None:
        # final weight is a set of [id, label] data
        # 0. reset labels
        self.labels = np.zeros(shape=(self.num_samples), dtype=int)

        # 1. find the correct set
        core_point_labels = final_weights[np.where(final_weights[:, 0] == self.id)][:, 1]

        # 2. assign the core point labels
        for label, index in zip(core_point_labels, self.to_cluster):
            self.labels[index] = label
        
        # 3. cluster remaining points
        clustered_points = self.X[self.to_cluster]
        for i in self.to_assign:
            if self.labels[i] == 0:
                dist = distance_matrix([self.X[i]], clustered_points)
                self.labels[i] = self.labels[self.to_cluster[np.argmin(dist)]]

        for i in range(self.num_samples):
            self.labels[i] = self.labels[self.cp[i]]
        
        # 4. handle outliers
        # 4.1 assign outlier core points to nearest cluster if in radius
        # outliers left: list of tuples (outlier_core_point, coverging points, sorted neigbourhood)
        outliers_left = [
            (
                i,
                [j for j in range(self.num_samples) if self.cp[j] == i],
                sorted(
                    [j for j in range(self.num_samples) if not i == j and self.dist[i, j] < self.r1],
                    key=lambda x: self.dist[i, x]
                )
            )
            for i in self.outcp
        ]
        old_len = len(outliers_left) + 1
        while old_len > len(outliers_left):
            old_len = len(outliers_left)
            if old_len > 0:
                for _ in range(old_len):
                    i, conv, neigh = outliers_left.pop(0)
                    assigned = False
                    for j in neigh:
                        if self.labels[j] > 0:
                            for k in conv:
                                self.labels[k] = self.labels[j]
                            assigned = True
                            break

                    if not assigned:
                        outliers_left.append((i, conv, neigh))

        # 4.2 treat remaining points regardless of being a core point
        outliers_left = [
            (
                i,
                sorted(
                    [j for j in range(self.num_samples) if not i == j and self.dist[i, j] < self.r1],
                    key=lambda x: self.dist[i, x]
                )
            ) 
            for _, conv, _ in outliers_left for i in conv
        ]
        old_len = len(outliers_left) + 1
        while old_len > len(outliers_left):
            old_len = len(outliers_left)
            if old_len > 0:
                for _ in range(old_len):
                    i, neigh = outliers_left.pop(0)
                    assigned = False
                    for j in neigh:
                        if self.labels[j] > 0:
                            self.labels[i] = self.labels[j]
                            assigned = True
                            break

                    if not assigned:
                        outliers_left.append((i, neigh))




    def get_labels(self):
        return self.labels

    def predict(self, X):
        pass