import os
import re


def _parse_inputs(filename: str) -> tuple[dict[int, list[list[bool]]], list[tuple[int, int, list[int]]]]:
    """
    Parse the input file containing shape definitions and region specifications.
    
    Returns:
        shapes: dict mapping shape index to 2D grid of bools (True = part of shape)
        regions: list of (width, height, quantities) where quantities[i] = count of shape i needed
    """
    with open(filename, 'r') as f:
        content = f.read()
    
    # Split into sections by double newline (shapes vs regions)
    sections = content.strip().split('\n\n')
    
    # Parse shapes from all sections except the last part that contains regions
    shapes = {}
    region_lines = []
    
    for section in sections:
        lines = section.strip().split('\n')
        # Check if this section starts with a shape definition (digit followed by colon)
        if lines[0].strip() and lines[0].strip()[0].isdigit() and ':' in lines[0] and 'x' not in lines[0]:
            # This is a shape definition
            shape_idx = int(lines[0].strip().rstrip(':'))
            grid = []
            for line in lines[1:]:
                row = [c == '#' for c in line]
                grid.append(row)
            shapes[shape_idx] = grid
        else:
            # These are region definitions
            region_lines.extend(lines)
    
    # Parse regions
    regions = []
    for line in region_lines:
        if not line.strip():
            continue
        # Format: "WxH: q0 q1 q2 q3 q4 q5"
        dims_part, quantities_part = line.split(':')
        width, height = map(int, dims_part.strip().split('x'))
        quantities = list(map(int, quantities_part.strip().split()))
        regions.append((width, height, quantities))
    
    return shapes, regions


def part1(filename: str) -> int:
    shapes, regions = _parse_inputs(filename)
    shape_to_area = {shape_idx: sum(1 for row in shape for cell in row if cell) for shape_idx, shape in shapes.items()}
    count = 0
    for region in regions:
        width, height, quantities = region
        max_area = width * height
        area_needed = 0
        for shape_idx, quantity in enumerate(quantities):
            area_needed += shape_to_area[shape_idx] * quantity
        if area_needed <= max_area:
            count += 1
    return count

if __name__ == "__main__":
    print(part1("test_input.txt"))
    print(part1("input.txt"))