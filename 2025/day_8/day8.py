import os
import math
import heapq

def _parse_input(input_file):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(cur_dir, input_file)
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    junction_box_points = [(int(line.split(',')[0]), int(line.split(',')[1]), int(line.split(',')[2])) for line in lines]
    return junction_box_points

def part1(input_file, max_inputs):
    junction_box_points = _parse_input(input_file)
    # calculate point wise distance between all points
    distance_to_points = []
    for i in range(len(junction_box_points)):
        for j in range(i+1, len(junction_box_points)):
            point1 = junction_box_points[i]
            point2 = junction_box_points[j]
            distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)
            points_and_distance = (distance, point1, point2)
            heapq.heappush_max(distance_to_points, points_and_distance)
            if len(distance_to_points) > max_inputs:
                heapq.heappop_max(distance_to_points)
    
    unique_points = set()
    for distance, point1, point2 in distance_to_points:
        unique_points.add(point1)
        unique_points.add(point2)
    groupings = [set([point]) for point in unique_points]

    for _, point1, point2 in distance_to_points:
        group1 = None
        group2 = None
        for group in groupings:
            if point1 in group:
                group1 = group
            if point2 in group:
                group2 = group
            if group1 is not None and group2 is not None:
                break
        # merge groups if they are not the same
        if group1 is not None and group2 is not None and group1 != group2:
            group1.update(group2)
            groupings.remove(group2)
    # get the three largest groups
    largest_groups = sorted(groupings, key=lambda x: len(x), reverse=True)[:3]
    return math.prod([len(group) for group in largest_groups])


def part2(input_file):
    junction_box_points = _parse_input(input_file)
    # calculate point wise distance between all points
    distance_to_points = []
    for i in range(len(junction_box_points)):
        for j in range(i+1, len(junction_box_points)):
            point1 = junction_box_points[i]
            point2 = junction_box_points[j]
            distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)
            points_and_distance = (distance, point1, point2)
            distance_to_points.append(points_and_distance)
    
    distance_to_points = sorted(distance_to_points, key=lambda x: x[0])
    groupings = [set([point]) for point in junction_box_points]
    last_p1 = None
    last_p2 = None

    for _, point1, point2 in distance_to_points:
        group1 = None
        group2 = None
        for group in groupings:
            if point1 in group:
                group1 = group
            if point2 in group:
                group2 = group
            if group1 is not None and group2 is not None:
                break
        # merge groups if they are not the same
        if group1 is not None and group2 is not None and group1 != group2:
            group1.update(group2)
            groupings.remove(group2)
            last_p1 = point1
            last_p2 = point2
    return last_p1[0] * last_p2[0]



def main():
    print(part1("test_input.txt", 10))
    print(part1("input.txt", 1000))
    print(part2("test_input.txt"))
    print(part2("input.txt"))

if __name__ == "__main__":
    main()