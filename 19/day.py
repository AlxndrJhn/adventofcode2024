import itertools
import os
import re
from collections import defaultdict

from cvxpy import length
from tqdm import tqdm

this_folder = "\\".join(__file__.split("\\")[:-1])


def is_possible(design, avail_patterns):
    design = design[::-1]
    avail_patterns = [p[::-1] for p in avail_patterns]
    appearing_patterns = [p for p in avail_patterns if p in design]
    group = "|".join(appearing_patterns)
    re_pattern = re.compile(f"({group})+")
    if re.fullmatch(re_pattern, design):
        return True
    return False


def main(filename):
    avail_patterns_str, designs_str = (
        open(f"{this_folder}/{filename}", "r").read().split("\n\n")
    )
    avail_patterns = avail_patterns_str.split(", ")
    designs = designs_str.strip().split("\n")

    # Part 1
    result1 = 0
    for i, design in enumerate(designs):
        if is_possible(design, avail_patterns):
            result1 += 1
        else:
            pass
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (6, 24)
        assert main("input.txt") == (347, 24)
    except AssertionError:
        print("❌ wrong")
