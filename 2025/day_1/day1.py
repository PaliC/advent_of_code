import os
def part1():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_dir, 'input.txt'), 'r') as file:
        lines = file.readlines()

    rotations = []
    count = 0
    for line in lines:
        direction = line[0]
        steps = int(line[1:]) % 100
        if direction == 'R':
            rotations.append(steps)
        else:
            rotations.append(-steps)
    
    cur_pos = 50
    for rotation in rotations:
        cur_pos += rotation

        if cur_pos < 0:
            cur_pos = cur_pos + 100
        
        cur_pos = cur_pos % 100
        if cur_pos == 0:
            count += 1
    return count

# your answer is too high.
def part2():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_dir, 'input.txt'), 'r') as file:
        lines = file.readlines()

    rotations = []
    count = 0
    for line in lines:
        direction = line[0]
        steps = int(line[1:])
        count += steps // 100
        steps = steps % 100
        if direction == 'R':
            rotations.append(steps)
        else:
            rotations.append(-steps)
    
    cur_pos = 50
    for rotation in rotations:
        assert abs(rotation) < 100
        last_pos = cur_pos
        cur_pos += rotation

        if cur_pos < 0:
            cur_pos = cur_pos + 100
        else:
            cur_pos = cur_pos % 100
        if last_pos == 0:
            continue
        elif cur_pos == 0:
            count += 1
        elif last_pos < cur_pos and rotation < 0:
            count += 1
        elif last_pos > cur_pos and rotation > 0:
            count += 1
    return count

if __name__ == "__main__":
    print(part1())
    print(part2())