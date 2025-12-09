import os
import math

def parse_input(file_path):
    with open(file_path, 'r') as file:
        return [tuple(map(int, line.strip().split(','))) for line in file.readlines()]

def part1(file_path):
    input = parse_input(file_path)
    largest_rectangle = 0
    for i in range(len(input)):
        for j in range(i + 1, len(input)):
            if input[i][0] == input[j][0] or input[i][1] == input[j][1]:
                continue
            area = abs(input[i][0] - input[j][0] + 1) * abs(input[i][1] - input[j][1] + 1)
            if area > largest_rectangle:
                largest_rectangle = area
                # print(f"New largest rectangle: {largest_rectangle} from {input[i]} and {input[j]}")
    return largest_rectangle

def point_in_polygon(point, polygon):
    """Ray casting - works for convex AND concave polygons."""
    x, y = point
    n = len(polygon)
    inside = False
    
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        
        # Check if ray crosses this edge
        if ((yi > y) != (yj > y)) and \
           (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    
    return inside

def edges_cross(e1, e2):
    """Check if two segments properly cross (not just touch)"""
    def sign(x):
        if x > 1e-9: return 1
        if x < -1e-9: return -1
        return 0
    
    def cross_product(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    a, b = e1
    c, d = e2
    
    d1 = sign(cross_product(c, d, a))
    d2 = sign(cross_product(c, d, b))
    d3 = sign(cross_product(a, b, c))
    d4 = sign(cross_product(a, b, d))
    
    # Proper crossing: points strictly on opposite sides
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    
    return False

def point_in_polygon_tolerant(point, polygon):
    x, y = point
    
    # First check if it's exactly a vertex
    if (x, y) in polygon:
        return True
    
    # Offset toward centroid
    cx = sum(p[0] for p in polygon) / len(polygon)
    cy = sum(p[1] for p in polygon) / len(polygon)
    
    dx = (cx - x) * 0.000001
    dy = (cy - y) * 0.000001
    
    return point_in_polygon((x + dx, y + dy), polygon)

def _is_completely_inside(inner, outer):
    # Both checks required for concave shapes
    # 1. All inner vertices must be inside outer
    for v in inner:
        if not point_in_polygon_tolerant(v, outer):
            return False
    
    # 2. No edge crossings
    for i in range(len(inner)):
        e1 = (inner[i], inner[(i + 1) % len(inner)])
        for j in range(len(outer)):
            e2 = (outer[j], outer[(j + 1) % len(outer)])
            if edges_cross(e1, e2):
                return False
    
    return True



def sort_clockwise(points):
    # 1. Find centroid
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    
    # 2. Sort by angle from centroid (descending = clockwise)
    def angle(p):
        return math.atan2(p[1] - cy, p[0] - cx)
    
    return sorted(points, key=angle, reverse=True)

def part2(file_path):
    outer_points = parse_input(file_path)
    possible_rectangles = []
    max_area = 0
    for i in range(len(outer_points)):
        for j in range(i + 1, len(outer_points)):
            point1 = outer_points[i]
            point2 = outer_points[j]
            point3 = (point1[0], point2[1])
            point4 = (point2[0], point1[1])
            area = (abs(point1[0] - point2[0]) + 1) * (abs(point1[1] - point2[1]) + 1)

            points = sort_clockwise((point1, point2, point3, point4))
            if _is_completely_inside(points, outer_points):
                if area > max_area:
                    max_area = area
    return max_area

if __name__ == "__main__":
    print(part1("test_input.txt"))
    print(part1("input.txt"))
    print(part2("test_input.txt"))
    print(part2("input.txt"))