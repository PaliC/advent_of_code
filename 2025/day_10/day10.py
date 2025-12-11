import heapq
import os
import numpy as np
import cvxpy as cp

def _parse_input(input_file):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(cur_dir, input_file)
    target_lights_list = []
    buttons_list = []
    voltages_list = []
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            # get part in between []
            target_lights = line[line.index('[')+1:line.index(']')]
            buttons_string = line[line.index(']')+1:line.index('{')].strip()
            voltages = line[line.index('{')+1:line.index('}')]
            target_lights = [light == '.' for light in target_lights]
            # serialize buttons string to list of tuples
            buttons = [[int(switch) for switch in button.strip()[1:-1].split(',')] for button in buttons_string.split()]
            voltages = voltages.split(",")
            voltages = [int(voltage) for voltage in voltages]
            target_lights_list.append(target_lights)
            buttons_list.append(buttons)
            voltages_list.append(voltages)
    return target_lights_list, buttons_list, voltages_list 

def _find_min_switches(target_light, buttons):
    visited_configs = set()
    heap = [(0, target_light)]
    while heap:
        switchs, current_config = heapq.heappop(heap)
        if tuple(current_config) in visited_configs:
            continue
        visited_configs.add(tuple(current_config))

        if all(current_config):
            return switchs
        for button in buttons:
            new_config = current_config.copy()
            for switch in button:
                new_config[switch] = not new_config[switch]
            heapq.heappush(heap, (switchs + 1, new_config))
    return -1

def _find_min_voltage(buttons, voltages):
    equations = np.zeros((len(buttons), len(voltages)))
    for i, button in enumerate(buttons):
        for switch in button:
            equations[i, switch] = 1
    voltages = np.array(voltages)
    
    A = equations.T
    n = A.shape[1]
    
    x = cp.Variable(n, integer=True)
    constraints = [A @ x == voltages, x >= 0]
    objective = cp.Minimize(cp.sum(x))  # minimize total button presses
    
    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.SCIP)
    
    return x.value.sum()

def part1(input_file):
    target_lights, buttons, _ = _parse_input(input_file)
    total_switches = 0
    for target_light, button in zip(target_lights, buttons), total=len(target_lights):
        min_switches = _find_min_switches(target_light, button)
        # print(min_switches)
        total_switches += min_switches
    return total_switches

def part2(input_file):
    _, buttons_list, voltages_list = _parse_input(input_file)
    total_switches = 0
    for buttons, voltages in zip(buttons_list, voltages_list):
        min_switches = _find_min_voltage(buttons, voltages)
        # print(min_switches)
        total_switches += min_switches
    return int(total_switches)

if __name__ == "__main__":
    print(part1('test_input.txt'))
    print(part1('input.txt'))
    print(part2('test_input.txt'))
    print(part2('input.txt'))