import os
from collections import deque

def _parse_input(input_file):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(cur_dir, input_file)
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    lines = [list(line.strip()) for line in lines]
    # find S in first line
    start_index = lines[0].index('S')
    return lines, (0, start_index)

def part1(input_file):
    grid, start = _parse_input(input_file)
    stack = [start]
    visited = set()
    splits = 0
    while len(stack) > 0:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]):
            continue
        if grid[x][y] == '^':
            stack.append((x, y+1))
            stack.append((x, y-1))
            splits +=1
        if grid[x][y] == '.' or grid[x][y] == 'S':
            stack.append((x+1, y))
    return splits

class TreeNode:
    def __init__(self, x, y, parent=None, children=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.children = children if children is not None else []
        self.paths = 1

    def add_child(self, child):
        # check if child is already in children
        x, y = child.get_location()
        if (x, y) in [c.get_location() for c in self.children]:
            return
        self.children.append(child)

    def get_children(self):
        return self.children
    
    def get_parent(self):
        return self.parent
    
    def get_location(self):
        return (self.x, self.y)
    
    def update_paths(self):
        if len(self.children) == 0:
            return
        self.paths = sum(child.paths for child in self.children)

def part2(input_file):
    grid, start = _parse_input(input_file)
    root = TreeNode(start[0], start[1])
    stack = [root]
    treeNodes = []
    visited = set()
    splits = 0
    while len(stack) > 0:
        node = stack.pop()
        x, y = node.get_location()
        if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]):
            continue
        # found a valid child
        if node.parent is not None:
            node.parent.add_child(node)
            print(f"adding child {node.get_location()} to {node.parent.get_location()}")
            print(len(node.parent.get_children()))
        if (x, y) in visited:
            continue
        visited.add((x, y))
        treeNodes.append(node)
        if grid[x][y] == '^':
            stack.append(TreeNode(x, y+1, node))
            stack.append(TreeNode(x, y-1, node))
        if grid[x][y] == '.' or grid[x][y] == 'S':
            stack.append(TreeNode(x+1, y, node))

    queue = deque([node for node in treeNodes if len(node.get_children()) == 0])
    visited = set()
    while len(queue) > 0:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        node.update_paths()
        print(f"node {node.get_location()} has {node.paths} paths and is parent of {len(node.get_children())} nodes")
        # print(node.paths)
        if node.parent is not None:
            queue.append(node.parent)
    return root.paths
if __name__ == "__main__":
    print(part1("test_input.txt"))
    print(part1("input.txt"))
    print(part2("test_input.txt"))
    # print(part2("input.txt"))