from functools import lru_cache
from collections import defaultdict
import networkx as nx
import os

def _parse_input(input_file):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    G = nx.DiGraph()
    input_file = os.path.join(cur_dir, input_file)
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            parent, rest = line.split(':')
            children = rest.split()
            for child in children:
                G.add_edge(parent, child)
    return G

def part1(input_file):
    graph = _parse_input(input_file)
    paths = nx.all_simple_paths(graph, 'you', 'out')
    count = 0
    for _ in paths:
        count += 1
    return count

def part2(input_file):
    graph = _parse_input(input_file)
    
    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("Graph has cycles - need different approach")
    
    topo_order = list(nx.topological_sort(graph))
    
    # dp[node][phase] = number of paths from svr to node in given phase
    # phase 0: before fft
    # phase 1: after fft, before dac  
    # phase 2: after dac
    dp = defaultdict(lambda: [0, 0, 0])
    dp['svr'][0] = 1
    
    for node in topo_order:
        counts = dp[node]
        if not any(counts):
            continue
            
        for neighbor in graph.successors(node):
            if neighbor == 'fft':
                # Can only enter fft in phase 0 → transition to phase 1
                dp['fft'][1] += counts[0]
            elif neighbor == 'dac':
                # Can only enter dac in phase 1 → transition to phase 2
                # Phase 0 → dac means we skipped fft, invalid path (dies here)
                dp['dac'][2] += counts[1]
            else:
                # Regular node: propagate all phases
                for phase in range(3):
                    dp[neighbor][phase] += counts[phase]
    
    return dp['out'][2]
    
    # Count: svr → fft → dac → out
    # This is trickier with DP, enumeration might be simpler

if __name__ == "__main__":
    print(part1('test_input.txt'))
    print(part1('input.txt'))
    print(part2('test_input2.txt'))
    print(part2('input.txt'))