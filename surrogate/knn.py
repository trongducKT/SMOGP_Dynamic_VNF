import numpy as np
import time

def knn_predict_mean(X_train, y_train, x_new, k):
    print("Dữ liệu train")
    print(X_train)
    print(y_train)
    distances = []
    for i in range(len(X_train)):
        difference = X_train[i] - x_new
        distance = len(difference) - np.count_nonzero(difference)
        # distance = np.linalg.norm(X_train[i] - x_new)
        distances.append(-distance)
    nearest_indices = np.argsort(distances)[:k]
    print("********************************")
    print(nearest_indices)
    nearest_labels = y_train[nearest_indices]
    print(x_new)
    nearest_data = X_train[nearest_indices]
    for data in nearest_indices:
        print(data)

    time.sleep(100)
    predicted_objective1 = np.mean(nearest_labels[:,0])
    predicted_objective2 = np.mean(nearest_labels[:,1])
    
    return [predicted_objective1, predicted_objective2]