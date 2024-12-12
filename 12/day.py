import itertools
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


def get_group(input_data, i, j):
    to_explore = [(i, j)]
    visited = set()
    group = set()
    type = input_data[i][j]
    while to_explore:
        i, j = to_explore.pop()
        if (i, j) in visited:
            continue
        visited.add((i, j))
        if input_data[i][j] == type:
            group.add((i, j))
            if i > 0:
                to_explore.append((i - 1, j))
            if i < len(input_data) - 1:
                to_explore.append((i + 1, j))
            if j > 0:
                to_explore.append((i, j - 1))
            if j < len(input_data[i]) - 1:
                to_explore.append((i, j + 1))
    return group


def area(group):
    return len(group)


def perimeter(group):
    peri = 0
    for i, j in group:
        if (i - 1, j) not in group:
            peri += 1
        if (i + 1, j) not in group:
            peri += 1
        if (i, j - 1) not in group:
            peri += 1
        if (i, j + 1) not in group:
            peri += 1
    return peri


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_mat = [list(line) for line in input_data]

    # Part 1
    result1 = 0
    groups = []
    for i in range(len(input_data_mat)):
        for j in range(len(input_data_mat[i])):
            if any((i, j) in group for group in groups):
                continue
            group = get_group(input_data_mat, i, j)
            groups.append(group)
            result1 += area(group) * perimeter(group)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (140, 24)
        assert main("input_example2.txt") == (772, 24)
        assert main("input.txt") == (1485656, 24)
    except AssertionError:
        print("❌ wrong")
