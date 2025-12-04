import os

def _load_input(file_path):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(cur_dir, file_path)
    grid = []
    with open(file_path, 'r') as file:
        for line in file:
            grid_line = []
            line = line.strip()
            for char in line:
                if char == '@':
                    grid_line.append(True)
                else:
                    grid_line.append(False)
            grid.append(grid_line)
    return grid
                    

def _count_surrounding_true(grid, i, j):
    count = 0
    for di in range(max(0, i-1), min(len(grid), i+2)):
        for dj in range(max(0, j-1), min(len(grid[0]), j+2)):
            if di == i and dj == j:
                continue
            if grid[di][dj]:
                count += 1
    return count

def _find_removable_tp(grid):
    removable_cells = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]:
                if _count_surrounding_true(grid, i, j) < 4:
                    removable_cells.append((i, j))
    return removable_cells

def part1(input_file):
    grid = _load_input(input_file)
    removable_cells = _find_removable_tp(grid)
    return len(removable_cells)

def part2(input_file):
    grid = _load_input(input_file)
    removable_cells = _find_removable_tp(grid)
    removed_tp = len(removable_cells)
    while len(removable_cells) > 0:
        for i, j in removable_cells:
            grid[i][j] = False
        removable_cells = _find_removable_tp(grid)
        removed_tp += len(removable_cells)
    return removed_tp

if __name__ == "__main__":
    print(part1('test_input.txt'))
    print(part1('input.txt'))
    print(part2('test_input.txt'))
    print(part2('input.txt'))