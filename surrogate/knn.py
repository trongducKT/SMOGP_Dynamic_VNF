import numpy as np
import time

def knn_predict_mean(X_train, y_train, x_new, k):
    distances = []
    for i in range(len(X_train)):
        difference = X_train[i] - x_new
        if np.count_nonzero(difference) == 0:
            return y_train[i]
        distance = len(difference) - np.count_nonzero(difference)
        # distance = np.linalg.norm(X_train[i] - x_new)
        distances.append(-distance)
    nearest_indices = np.argsort(distances)[:k]
    nearest_labels = y_train[nearest_indices]
    predicted_objective1 = np.mean(nearest_labels[:,0])
    predicted_objective2 = np.mean(nearest_labels[:,1])
    
    return [predicted_objective1, predicted_objective2]