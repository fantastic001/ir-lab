import networkx as nx 
from matplotlib import pyplot as plt

def generate(n):
    g: nx.DiGraph = nx.stochastic_block_model(
        sizes = [n // 5, n, n // 5],
        p = [
            [0.2, 0.40,   0    ],
            [0,   0.6,   0.40 ],
            [0,   0,      0.2  ]
        ],
        directed = True
    )
    return g


def pagerank(g: nx.DiGraph, niter: int, alpha: float):
    pr = {n: 1/g.number_of_nodes() for n in g.nodes()}
    for i in range(niter):
        for n in g:
            pr[n] = (1 - alpha) / g.number_of_nodes() + alpha * sum(pr[z] / g.out_degree()[z] for z in g.predecessors(n))
    return pr 