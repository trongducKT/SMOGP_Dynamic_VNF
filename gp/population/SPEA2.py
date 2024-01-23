import heapq

import numpy as np

from gp.population.individual import Individual


def distance(p1: Individual, p2: Individual):
    return np.linalg.norm(p1.objectives - p2.objectives)


def fitness_assignment(P: list):
    N = len(P)
    # calculate raw fitness R
    dominators = np.empty(N, dtype=object)
    S = np.zeros(N, dtype=int)
    R = np.empty(N, dtype=float)
    for i, p in enumerate(P):
        dominators[i] = []
        for j, q in enumerate(P):
            if i != j and q.dominate(p):
                dominators[i].append(j)
                S[j] += 1
    for i in range(N):
        R[i] = sum(S[j] for j in dominators[i])

    # Calculate density D
    k = int(np.sqrt(N))
    D = np.empty(N, dtype=float)
    for i, p in enumerate(P):
        distances = [distance(p, q) for q in P if p != q]
        if len(distances) == 0:
            print(P)
        assert k <= len(distances)
        sigma = heapq.nsmallest(k, distances)[-1]
        D[i] = 1 / (sigma + 2)

    F = R + D
    return F


def environmental_selection(P: list, N: int):
    F = fitness_assignment(P)
    P1_idx = [i for i, p in enumerate(P) if p.F < 1]

    # add
    if len(P1_idx) < N:
        dominated = [i for i, p in enumerate(P) if p.F >= 1]
        dominated.sort(key=lambda i: F[i])
        P1_idx.extend(dominated[:N - len(P1_idx)])
    # truncate
    else:
        while len(P1_idx) > N:
            N1 = len(P1_idx)
            mat = np.empty([N1, N1], dtype=float)
            for i in range(N1):
                for j in range(N1):
                    mat[i, j] = float('inf') if i == j else distance(P[P1_idx[i]], P[P1_idx[j]])
            np.sort(mat, axis=0)
            candidates = list(range(N1))
            for j in range(N1):
                candidates = [i for i in candidates if mat[i, j] ==
                              min([mat[i, j] for i in candidates])]
                if len(candidates) == 1:
                    break
            del P1_idx[candidates[0]]

    return [P[idx] for idx in P1_idx]
