import os
def _parse_input(file_path: str) -> list[tuple[int, int]]:
    # two sets of lines first is ranges and the second is numbers
    ranges = []
    numbers = []
    file_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            if "-" in line:
                ranges.append(tuple(map(int, line.split('-'))))
            else:
                numbers.append(int(line))
    return ranges, numbers

def part_1(file_path: str) -> int:
    ranges, numbers = _parse_input(file_path)
    ranges.sort(key=lambda x: x[0])
    count = 0
    for number in numbers:
        for range in ranges:
            if range[0] <= number <= range[1]:
                count += 1
                break
    return count

def part_2(file_path: str) -> int:
    ranges, _ = _parse_input(file_path)
    ranges.sort(key=lambda x: x[0])
    ranges = [[range[0], range[1]] for range in ranges]
    merged_ranges = [ranges[0]]
    for range in ranges[1:]:
        if range[0] <= merged_ranges[-1][1]:
            merged_ranges[-1][1] = max(merged_ranges[-1][1], range[1])
        else:
            merged_ranges.append(range)
    return sum(range[1] - range[0] + 1 for range in merged_ranges)

def main():
    # ranges, numbers = _parse_input(os.path.join(os.path.dirname(__file__), 'test_input.txt'))
    print(part_1("test_input.txt"))
    print(part_1("input.txt"))
    print(part_2("test_input.txt"))
    print(part_2("input.txt"))

if __name__ == '__main__':
    main()