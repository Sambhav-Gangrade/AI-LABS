import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('cities.csv', header=None)
coords = df.values
n_points = len(coords)
k = 3
N_RUNS = 10

best_labels  = None
best_centers = None
best_inertia = np.inf

for run in range(N_RUNS):
    np.random.seed(run+25)
    
    random_indices = np.random.choice(n_points, size=k, replace=False)
    centers = coords[random_indices].copy()
    labels  = np.zeros(n_points, dtype=int)
    
    converged = False
    while not converged:
        distances = np.zeros((n_points, k))
        for i in range(k):
            distances[:, i] = np.sum((coords - centers[i])**2, axis=1)

        new_labels = np.argmin(distances, axis=1)

        if np.array_equal(labels, new_labels):
            converged = True
        labels = new_labels

        for i in range(k):
            cluster_points = coords[labels == i]
            if len(cluster_points) > 0:
                centers[i] = np.mean(cluster_points, axis=0)

    inertia = sum(
        np.sum((coords[labels == i] - centers[i])**2)
        for i in range(k)
    )
    
    print(f"Run {run+1:2d} | Inertia: {inertia:.2f}")

    if inertia < best_inertia:
        best_inertia = inertia
        best_labels  = labels.copy()
        best_centers = centers.copy()

print(f"\nBest inertia across {N_RUNS} runs: {best_inertia:.2f}\n")

clusters = [coords[best_labels == i] for i in range(k)]

print("=== FINAL AIRPORT LOCATIONS ===")
for i, cluster in enumerate(clusters):
    m     = len(cluster)
    sum_x = np.sum(cluster[:, 0])
    sum_y = np.sum(cluster[:, 1])

    mu_gd = np.array([0.0, 0.0])
    mu_nr = np.array([0.0, 0.0])

    learning_rate = 0.01
    epochs        = 1000
    for _ in range(epochs):
        grad_x = 2 * m * mu_gd[0] - 2 * sum_x
        grad_y = 2 * m * mu_gd[1] - 2 * sum_y
        mu_gd  = mu_gd - learning_rate * np.array([grad_x, grad_y])

    grad_nr = np.array([
        2 * m * mu_nr[0] - 2 * sum_x,
        2 * m * mu_nr[1] - 2 * sum_y
    ])    
    H_inv  = np.array([[1 / (2*m), 0],
                       [0,         1 / (2*m)]])
    mu_nr  = mu_nr - np.dot(H_inv, grad_nr)

    ssd_gd = np.sum((cluster - mu_gd)**2)
    ssd_nr = np.sum((cluster - mu_nr)**2)
    
    print(f"\nAirport {i+1} (Serving {m} cities)")
    print(f"  Gradient Descent : ({mu_gd[0]:.4f}, {mu_gd[1]:.4f}) | SSD: {ssd_gd:.4f}")
    print(f"  Newton-Raphson   : ({mu_nr[0]:.4f}, {mu_nr[1]:.4f}) | SSD: {ssd_nr:.4f}")