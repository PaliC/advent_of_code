import math
import os
def part1():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_dir, 'input.txt'), 'r') as file:
        lines = file.readlines()
    ranges = []
    invalid_vals = set()
    for line in lines:
        line = line.split(',')
        for pair in line:
            pair = pair.split('-')
            ranges.append((int(pair[0]), int(pair[1])))
    ranges.sort(key=lambda x: x[0])
    for start, end in ranges:
        for i in range(start, end + 1):
            zeros = int(math.log(i, 10)) + 1
            if zeros % 2 == 1:
                continue
            half_of_zeros = zeros // 2
            
            if i // (10 ** half_of_zeros) == i % (10 ** half_of_zeros):
                invalid_vals.add(i)

    return sum(invalid_vals)

def _check_if_repeated_pattern(i, pat_size):
    i_str = str(i)
    if len(i_str) % pat_size != 0:
        return False
    for j in range(0, len(i_str) - pat_size, pat_size):
        if i_str[j:j+pat_size] != i_str[j+pat_size:j+2*pat_size]:
            return False
    return True


def part2():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_dir, 'input.txt'), 'r') as file:
        lines = file.readlines()
    ranges = []
    invalid_vals = set()
    for line in lines:
        line = line.split(',')
        for pair in line:
            pair = pair.split('-')
            ranges.append((int(pair[0]), int(pair[1])))
    ranges.sort(key=lambda x: x[0])
    for start, end in ranges:
        for i in range(start, end + 1):
            str_i = str(i)
            for pat_size in range(1, len(str_i)):
                if _check_if_repeated_pattern(i, pat_size):
                    invalid_vals.add(i)
                    break

    return sum(invalid_vals)

if __name__ == "__main__":
    print(part1())
    print(part2())

# your answer is too low 3348721680