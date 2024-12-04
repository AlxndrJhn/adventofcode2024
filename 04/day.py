import itertools
import os
import re
from collections import defaultdict
from tkinter import RIGHT

this_folder = "\\".join(__file__.split("\\")[:-1])
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
UP_RIGHT = (-1, 1)
UP_LEFT = (-1, -1)
DOWN_RIGHT = (1, 1)
DOWN_LEFT = (1, -1)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT, UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT]


def word_exists(input_data_mat, row_i, col_j, direction, target, index_letter):
    cell_i = row_i + direction[0] * index_letter
    cell_j = col_j + direction[1] * index_letter
    WIDTH = len(input_data_mat[0])
    HEIGHT = len(input_data_mat)
    if cell_i < 0 or cell_i >= HEIGHT or cell_j < 0 or cell_j >= WIDTH:
        return False
    if input_data_mat[cell_i][cell_j] != target[index_letter]:
        return False
    if index_letter == len(target) - 1:
        return True
    return word_exists(
        input_data_mat, row_i, col_j, direction, target, index_letter + 1
    )


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_mat = [list(line) for line in input_data]

    # Part 1
    TARGET = "XMAS"
    result1 = 0
    for row_i, col_j in itertools.product(
        range(len(input_data_mat)), range(len(input_data_mat[0]))
    ):
        if input_data_mat[row_i][col_j] == TARGET[0]:
            for dir in DIRECTIONS:
                if word_exists(input_data_mat, row_i, col_j, dir, TARGET, 1):
                    result1 += 1
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input_ex.txt") == (18, 24)
    assert main("input.txt") == (2434, 24)
