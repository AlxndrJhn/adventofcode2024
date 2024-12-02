from collections import Counter
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_lists = [list(int(x) for x in line.split()) for line in input_data]
    col1, col2 = zip(*input_data_lists)

    # Part 1
    sorted_col1 = sorted(col1)
    sorted_col2 = sorted(col2)

    _sum = 0
    for val1, val2 in zip(sorted_col1, sorted_col2):
        _sum += abs(val1 - val2)
    result1 = _sum
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    counter = Counter(col2)
    result2 = sum([num_left * counter[num_left] for num_left in col1])
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input_example.txt") == (11, 31)
    assert main("input.txt") == (1590491, 22588371)
    # main("input.txt")
