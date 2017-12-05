import networkx as nx

def jaccard_wt(graph, node):
    
    neighbors = set(graph.neighbors(node))
    deg1 = .0
    for i in neighbors:
            deg1 += graph.degree(i)
            
    scores = []
    for ni in graph.nodes():
        if ni != node and not graph.has_edge(node, ni):
            neighbors2 = set(graph.neighbors(ni))
            
            inner = .0
            for m in neighbors & neighbors2:
                if graph.degree(m) != 0:
                    inner += 1/graph.degree(m)
          
            deg2 = .0
            for j in neighbors2:
                deg2 += graph.degree(j)
                
            if deg1 != 0 and deg2 != 0:
                score = inner/((1/deg1)+(1/deg2)) 
            
            scores.append(((node,ni), score))
    return sorted(scores, key=lambda x: x[1], reverse=True)
