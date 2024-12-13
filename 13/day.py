import itertools
import math
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


def get_numbers(button):
    pattern = r"(-?\d+)"
    return tuple(map(int, re.findall(pattern, button)))


A_COST = 3
B_COST = 1
MAX_PUSHES = 100


def main(filename):
    device_infos = open(f"{this_folder}/{filename}", "r").read().split("\n\n")
    device_ab_prizes = []
    for device_info in device_infos:
        device_ab_prizes.append([get_numbers(part) for part in device_info.split("\n")])
    # Part 1
    result1 = 0
    for button_a, button_b, prize_loc in device_ab_prizes:
        lowest_option = math.inf
        for a in range(1, MAX_PUSHES + 1):
            for b in range(1, MAX_PUSHES + 1):
                final_loc = (
                    a * button_a[0] + b * button_b[0],
                    a * button_a[1] + b * button_b[1],
                )
                if final_loc == prize_loc:
                    current_cost = a * A_COST + b * B_COST
                    if current_cost < lowest_option:
                        lowest_option = current_cost
        if lowest_option != math.inf:
            result1 += lowest_option
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (480, 24)
        assert main("input.txt") == (26299, 24)
    except AssertionError:
        print("❌ wrong")
