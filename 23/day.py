import itertools
import os
import re
from collections import defaultdict

from tqdm import tqdm

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().strip().split("\n")

    # Part 1
    pc_to_pcs = defaultdict(set)
    for connection in input_data:
        pc1, pc2 = connection.split("-")
        pc_to_pcs[pc1].add(pc2)
        pc_to_pcs[pc2].add(pc1)
    # find groups of 3
    groups_of_3 = set()
    for pc1 in pc_to_pcs:
        for pc2 in pc_to_pcs[pc1]:
            for pc3 in pc_to_pcs[pc2]:
                if pc3 in pc_to_pcs[pc1]:
                    if any(t.startswith("t") for t in [pc1, pc2, pc3]):
                        groups_of_3.add(tuple(sorted([pc1, pc2, pc3])))

    result1 = len(groups_of_3)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (7, 24)
        assert main("input.txt") == (1238, 24)
    except AssertionError:
        print("❌ wrong")
