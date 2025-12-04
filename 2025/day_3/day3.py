import os
import heapq
def part1():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_dir, 'input.txt'), 'r') as file:
        lines = file.readlines()
    batteries = []
    for line in lines:
        joltages = []
        for c in line:
            if c.isdigit():
                joltages.append(int(c))
        batteries.append(joltages)
    max_joltages = []
    for battery in batteries:
        look_forward_list = [battery[0]] * len(battery)
        look_backward_list = [battery[-1]] * len(battery)
        for i in range(1, len(battery)):
            look_forward_list[i] = max(look_forward_list[i-1], battery[i])
        for i in range(len(battery)-2, -1, -1):
            look_backward_list[i] = max(look_backward_list[i+1], battery[i])
        max_joltage = 0
        for i in range(len(battery)-1):
            candidate = look_forward_list[i]*10 + look_backward_list[i+1]
            max_joltage = max(max_joltage, candidate)
        max_joltages.append(max_joltage)
    return sum(max_joltages)
    

def part2():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_dir, 'input.txt'), 'r') as file:
        lines = file.readlines()
    batteries = []
    for line in lines:
        joltages = []
        for c in line:
            if c.isdigit():
                joltages.append(int(c))
        batteries.append(joltages)
    max_joltages = []
    for battery in batteries:
        joltages = []
        start = 0
        for i in range(0, 12):
            # get max val between start and i in inclusive
            end = len(battery) - 12 + i
            if start == end:
                joltages.append(battery[start])
                start += 1
                continue
            max_val = max(battery[start:end+1])
            max_val_index = battery[start:end+1].index(max_val) + start
            joltages.append(max_val)
            start = max_val_index + 1
        true_joltage = 0
        for i in range(len(joltages)):
            true_joltage = true_joltage * 10 + joltages[i]
        max_joltages.append(true_joltage)
    # print(max_joltages)
            
    return sum(max_joltages)

if __name__ == "__main__":
    print(part1())
    print(part2())