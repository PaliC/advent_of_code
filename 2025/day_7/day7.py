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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = []
        self.children = []
        self.paths = 1

    def add_child(self, child):
        # check if child is already in children
        x, y = child.get_location()
        if (x, y) in [c.get_location() for c in self.children]:
            return
        self.children.append(child)

    def add_parent(self, parent):
        # check if parent is already in parents
        x, y = parent.get_location()
        if (x, y) in [p.get_location() for p in self.parent]:
            return
        self.parent.append(parent)

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

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def part2(input_file):
    grid, start = _parse_input(input_file)
    root = TreeNode(start[0], start[1])
    stack = [root]
    treeNodes = {}  # (x, y) -> TreeNode

    while len(stack) > 0:
        node = stack.pop()
        x, y = node.get_location()

        if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]):
            continue

        loc = node.get_location()
        
        # Check for existing node FIRST
        if loc in treeNodes:
            existing = treeNodes[loc]
            for parent in node.parent:
                parent.add_child(existing)
                existing.add_parent(parent)
            continue

        # Only now add as child and register in treeNodes
        if node.parent:
            for parent in node.parent:
                parent.add_child(node)

        treeNodes[loc] = node

        if grid[x][y] == '^':
            t1 = TreeNode(x, y + 1)
            t2 = TreeNode(x, y - 1)
            t1.add_parent(node)
            t2.add_parent(node)
            stack.append(t1)
            stack.append(t2)

        if grid[x][y] == '.' or grid[x][y] == 'S':
            t = TreeNode(x + 1, y)
            t.add_parent(node)
            stack.append(t)

    # Count how many children each node has that still need processing
    children_remaining = {}
    for loc, node in treeNodes.items():
        children_remaining[loc] = len(node.get_children())

    # Start with leaf nodes (nodes with 0 children)
    queue = deque([node for node in treeNodes.values() if len(node.get_children()) == 0])
    visited = set()

    while len(queue) > 0:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        node.update_paths()

        for parent in node.parent:
            parent_loc = parent.get_location()
            children_remaining[parent_loc] -= 1
            # Only add parent when ALL its children have been processed
            if children_remaining[parent_loc] == 0:
                queue.append(parent)

    return root.paths

if __name__ == "__main__":
    print(part1("test_input.txt"))
    print(part1("input.txt"))
    print(part2("test_input.txt"))
    print(part2("input.txt"))