import itertools
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_mat = [list(line) for line in input_data]

    # Part 1
    results = set()
    FREE = "."
    unique_frequencies = set()
    [[unique_frequencies.add(x) for x in line] for line in input_data_mat]
    unique_frequencies.remove(FREE)
    for frequency in unique_frequencies:
        frequency_locations = [
            (i, j)
            for i in range(len(input_data_mat))
            for j in range(len(input_data_mat[0]))
            if input_data_mat[i][j] == frequency
        ]
        for f1, f2 in list(itertools.combinations(frequency_locations, 2)):
            diff = (f1[0] - f2[0], f1[1] - f2[1])
            new_loc1 = (f1[0] + diff[0], f1[1] + diff[1])
            new_loc2 = (f2[0] - diff[0], f2[1] - diff[1])
            for i, j in [new_loc1, new_loc2]:
                if 0 <= i < len(input_data_mat) and 0 <= j < len(input_data_mat[0]):
                    results.add((i, j))
    result1 = len(results)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (14, 24)
        assert main("input.txt") == (318, 24)
    except AssertionError:
        print("❌ wrong")
