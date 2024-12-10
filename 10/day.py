import itertools
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIR = [UP, DOWN, LEFT, RIGHT]


def get_reachable_9s(input_data_mat, current_loc, reachable_9s: set):
    H, W = len(input_data_mat), len(input_data_mat[0])
    i, j = current_loc
    if input_data_mat[i][j] == 9:
        reachable_9s.add((i, j))
        return reachable_9s
    for di, dj in DIR:
        new_i, new_j = i + di, j + dj
        if new_i < 0 or new_i >= H or new_j < 0 or new_j >= W:
            continue
        diff = input_data_mat[new_i][new_j] - input_data_mat[i][j]
        if diff != 1:
            continue
        reachable_9s = get_reachable_9s(input_data_mat, (new_i, new_j), reachable_9s)
    return reachable_9s


def get_distict_routes(input_data_mat, current_loc, route_so_far, all_routes):
    H, W = len(input_data_mat), len(input_data_mat[0])
    i, j = current_loc
    route_so_far = route_so_far + ((i, j),)
    if input_data_mat[i][j] == 9:
        all_routes.add(route_so_far)
        return all_routes
    for di, dj in DIR:
        new_i, new_j = i + di, j + dj
        if new_i < 0 or new_i >= H or new_j < 0 or new_j >= W:
            continue
        diff = input_data_mat[new_i][new_j] - input_data_mat[i][j]
        if diff != 1:
            continue
        potentioal_route = route_so_far + ((new_i, new_j),)
        all_routes = get_distict_routes(
            input_data_mat, (new_i, new_j), potentioal_route, all_routes
        )
    return all_routes


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_mat = [[-1 if x == "." else int(x) for x in line] for line in input_data]
    H, W = len(input_data_mat), len(input_data_mat[0])
    # Part 1
    zero_locs = []
    for i, j in itertools.product(range(H), range(W)):
        if input_data_mat[i][j] == 0:
            zero_locs.append((i, j))

    result1 = 0
    for zero_loc in zero_locs:
        result1 += len(get_reachable_9s(input_data_mat, zero_loc, set()))
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 0
    for zero_loc in zero_locs:
        result2 += len(get_distict_routes(input_data_mat, zero_loc, (), set()))
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (1, 16)
        assert main("input.txt") == (778, 1925)
        assert main("input_example2.txt") == (1, 3)
        assert main("input_example3.txt") == (4, 13)
        assert main("input_example4.txt") == (2, 227)
    except AssertionError:
        print("❌ wrong")
