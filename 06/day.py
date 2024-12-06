import itertools
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_mat = [list(line) for line in input_data]

    # Part 1
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"
    DIR = [UP, DOWN, LEFT, RIGHT]
    FREE = "."
    DIR_TO_OFFSET = {
        UP: (-1, 0),
        DOWN: (1, 0),
        LEFT: (0, -1),
        RIGHT: (0, 1),
    }

    def is_outside(loc, input_data_mat):
        i, j = loc
        return not (0 <= i < len(input_data_mat) and 0 <= j < len(input_data_mat[0]))

    def is_free_loc(loc, input_data_mat):
        if is_outside(loc, input_data_mat):
            return True  # outside is always ok
        i, j = loc
        return input_data_mat[i][j] == FREE

    def get_guard_loc(input_data_mat):
        return next(
            (i, j)
            for i, row in enumerate(input_data_mat)
            for j, x in enumerate(row)
            if x in DIR
        )

    def rotate_90deg_right(direction):
        if direction == UP:
            return RIGHT
        if direction == RIGHT:
            return DOWN
        if direction == DOWN:
            return LEFT
        if direction == LEFT:
            return UP

    input_data_mat = [list(row) for row in input_data]
    guard_loc = initial_guard_loc = get_guard_loc(input_data_mat)
    unique_locs_part1 = set()

    while not is_outside(guard_loc, input_data_mat):
        i, j = guard_loc
        unique_locs_part1.add(guard_loc)
        guard_dir = input_data_mat[i][j]
        movement = DIR_TO_OFFSET[guard_dir]
        next_loc = (i + movement[0], j + movement[1])
        if is_free_loc(next_loc, input_data_mat):
            input_data_mat[i][j] = FREE
            if not is_outside(next_loc, input_data_mat):
                input_data_mat[next_loc[0]][next_loc[1]] = guard_dir
            guard_loc = next_loc
        else:
            # rotate 90deg right
            input_data_mat[i][j] = rotate_90deg_right(guard_dir)

    result1 = len(unique_locs_part1)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    def is_a_loop(input_data):
        input_data = [list(row) for row in input_data]
        guard_loc = initial_guard_loc

        unique_loc_dir = set()
        while not is_outside(guard_loc, input_data):
            i, j = guard_loc
            guard_dir = input_data[i][j]
            if (i, j, guard_dir) in unique_loc_dir:
                return True
            unique_loc_dir.add((i, j, guard_dir))
            movement = DIR_TO_OFFSET[guard_dir]
            next_loc = (i + movement[0], j + movement[1])
            if is_free_loc(next_loc, input_data):
                input_data[i][j] = FREE
                if not is_outside(next_loc, input_data):
                    input_data[next_loc[0]][next_loc[1]] = guard_dir
                guard_loc = next_loc
            else:
                # rotate 90deg right
                input_data[i][j] = rotate_90deg_right(guard_dir)
        return False

    result2 = 0
    for new_obstacle in unique_locs_part1:
        input_data_mat = [list(row) for row in input_data]
        if new_obstacle == initial_guard_loc:
            continue
        i, j = new_obstacle
        assert input_data_mat[i][j] == FREE
        input_data_mat[i][j] = "#"
        if is_a_loop(input_data_mat):
            result2 += 1
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input_example.txt") == (41, 6)
    assert main("input.txt") == (5564, 1976)
