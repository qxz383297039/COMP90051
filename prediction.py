import math
import pandas as pd
from collections import Counter
from networkx import DiGraph
from networkx.algorithms.simple_paths import all_simple_paths

# import the graph
G = DiGraph()
with open("train.txt", 'r') as f:
    for line in f.read().split('\n'):
        if line:
            line = line.split()
            src = line[0]
            G.add_edges_from((src, dest) for dest in line[1:])
print("---- Read Finish ----")

beta = 0.5
ids, scores = [], []
with open("test-public.txt", 'r') as f:
    lines = f.read().split('\n')
    for line in lines[1:]:
        if line:
            pid, p1, p2 = list(line.split())
            ids.append(pid)
            print(f"{pid}: {p1} -> {p2}")
            cn = set(G.successors(p1)).intersection(set(G.predecessors(p2)))
            s = math.tanh(sum(1 / math.log(G.out_degree(z) + 1) for z in cn))
            print(f"Adamic/Adar: {s}")
            scores.append(s)
print("---- Process Finish ----")

s = pd.Series(scores, ids)
s.name = "Prediction"
s.index.name = "Id"
s.to_csv("output.csv", header=True)
