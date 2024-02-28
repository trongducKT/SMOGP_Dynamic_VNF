import numpy as np

def knn_predict_mean(X_train, y_train, x_new, k):
    distances = np.sqrt(np.sum((X_train - x_new)**2, axis=1))

    nearest_indices = np.argsort(distances)[:k]
    
    nearest_labels = y_train[nearest_indices]
    
    predicted_objective1 = np.mean(nearest_labels[:,0])
    predicted_objective2 = np.mean(nearest_labels[:,1])
    
    return [predicted_objective1, predicted_objective2]