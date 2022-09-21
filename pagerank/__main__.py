import sys 
from pagerank import * 


g = generate(int(sys.argv[1]))


nx.draw(g)
plt.show()

pr = pagerank(g, 100, 0.85)

print("Custom implementation")
print(sorted(g.nodes(), key=lambda x: pr[x]))
print(pr)
pr = nx.pagerank(g, 0.85)
print("NetworkX implementation")
print(pr)
print(sorted(g.nodes(), key=lambda x: pr[x]))
