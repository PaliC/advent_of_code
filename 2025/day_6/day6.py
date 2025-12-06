import os
import math
from collections import defaultdict
import re

def _parse_input(input_file):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(cur_dir, input_file)
    lines = []
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    ops = lines[-1].split()
    nums = [line.split() for line in lines[:-1]]
    # switch rows and columns
    nums = [list(row) for row in zip(*nums)]
    nums = [[int(num) for num in row] for row in nums]
    return ops, nums

def _parse_input_part2(input_file):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(cur_dir, input_file)
    lines = []
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    ops = lines[-1].split()
    num_lines = [line for line in lines[:-1]]

    nums = []
    start_index = 0
    # split num_lines where all lines have spaces at the same index
    for i in range(len(num_lines[0])):
        if all(line[i] == ' ' for line in num_lines):
            end_index = i
            nums.append([line[start_index:end_index] for line in num_lines])
            start_index = end_index + 1
    # captrue the last num_list
    nums.append([line[start_index:] for line in num_lines])
    # flip indices of inner lists
    nums = [[int("".join(row).strip()) for row in zip(*num_list)] for num_list in nums]
    # nums = [[int(num) for num in row] for row in nums]
    return ops, nums

def part1(input_file):
        ops, nums = _parse_input(input_file)
        results = []
        for op, num_combo in zip(ops, nums):
            if op == '+':
                result = sum(num_combo)
            elif op == '*':
                result = 1
                for num in num_combo:
                    result *= num
            results.append(result)
        return sum(results)
        

def part2(input_file):
    ops, nums = _parse_input_part2(input_file)

    results = []
    for op, num_combo in zip(ops, nums):
        if op == '+':
            result = sum(num_combo)
        elif op == '*':
            result = 1
            for num in num_combo:
                result *= num
        results.append(result)
    return sum(results)

if __name__ == "__main__":
    print(part1("test_input.txt"))
    print(part1("input.txt"))
    print(part2("test_input.txt"))
    print(part2("input.txt"))