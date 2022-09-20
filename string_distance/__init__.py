
from typing import List
import numpy as np 
from document_index import vectorize

def edit_distance(x: str, y: str) -> int:
    d = np.zeros([len(x)+1, len(y) + 1])
    for i in range(len(x) + 1):
        d[i, 0] = i
    for i in range(len(y) + 1):
        d[0, i] = i
    for i, xc in enumerate(x):
        for j, yc in enumerate(y):
            if xc == yc:
                d[i+1,j+1] = d[i, j]
            else:
                d[i+1,j+1] = min(
                    1 + d[i, j+1],
                    1 + d[i+1, j],
                    1 + d[i, j]
                )
    return d[len(x), len(y)]

def char_set_distance(x: str, y: str) -> int:
    if len(set(x) & set(y)) == 0:
        return np.inf
    else:
        return len(set(x) | set(y)) / len(set(x) & set(y)) - 1

def vector_distance(x: str, y: str, collection) -> float:
    vx = vectorize(x, collection)
    vy = vectorize(y, collection)
    return np.dot(vx, vy) / np.sqrt(np.dot(vx, vx) * np.dot(vy, vy))