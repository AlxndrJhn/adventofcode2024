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


def get_perimeter(group):
    peri = set()
    DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for i, j in group:
        for dir in DIRECTIONS:
            other_point = (i + dir[0], j + dir[1])
            point_in_between = (i + dir[0] * 0.51, j + dir[1] * 0.51)
            if other_point not in group:
                peri.add(point_in_between)
    return peri


def get_linked_points(point, perimeter):
    linked_points = set()
    linked_points.add(point)
    to_explore = [point]
    while to_explore:
        point = to_explore.pop()
        for point2 in perimeter:
            distance = (
                (point[0] - point2[0]) ** 2 + (point[1] - point2[1]) ** 2
            ) ** 0.5
            if distance != 1:
                continue
            if point2 in linked_points:
                continue
            linked_points.add(point2)
            to_explore.append(point2)
    return linked_points


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_mat = [list(line) for line in input_data]

    # Part 1
    result1 = 0
    groups = []
    perimeters = []
    for i in range(len(input_data_mat)):
        for j in range(len(input_data_mat[i])):
            if any((i, j) in group for group in groups):
                continue
            group = get_group(input_data_mat, i, j)
            groups.append(group)
            perimeter = get_perimeter(group)
            perimeters.append(perimeter)
            result1 += area(group) * len(perimeter)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 0
    for group, perimeter in zip(groups, perimeters):
        processed = set()
        perimeter_sides = 0
        for point in perimeter:
            if point in processed:
                continue
            linked_points = get_linked_points(point, perimeter)
            processed.update(linked_points)
            perimeter_sides += 1
        result2 += area(group) * perimeter_sides
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (140, 80)
        assert main("input_example2.txt") == (772, 436)
        assert main("input.txt") == (1485656, 899196)
    except AssertionError:
        print("❌ wrong")
