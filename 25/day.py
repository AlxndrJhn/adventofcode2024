import itertools
import os
import re
from collections import defaultdict

from tqdm import tqdm

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().strip().split("\n\n")
    input_data_arr = [list(map(list, x.split("\n"))) for x in input_data]

    keys = set()
    locks = set()

    for obj in input_data_arr:
        is_key = all(x == "#" for x in obj[-1])

        if is_key:
            obj = list(zip(*obj[::-1]))
        else:
            obj = list(zip(*obj[::]))
        combination = []
        for row in obj:
            count = row.count("#") - 1
            combination.append(count)
        if is_key:
            keys.add(tuple(combination))
        else:
            locks.add(tuple(combination))
    # Part 1
    result1 = 0
    for lock, key in itertools.product(locks, keys):
        if all(x + y <= 5 for x, y in zip(lock, key)):
            result1 += 1
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (3, 24)
        assert main("input.txt") == (3320, 24)
    except AssertionError:
        print("❌ wrong")
