import itertools
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


def str_to_arr(string):
    return [int(x) for x in string.split(" ")]


def blink(input_arr, times=1):
    input_arr = input_arr.copy()
    for _ in range(times):
        idx = 0
        while idx < len(input_arr):
            value = input_arr[idx]
            value_str = str(value)
            value_str_len = len(value_str)
            if value == 0:
                input_arr[idx] = 1
            elif value_str_len % 2 == 0:
                left_half = int(value_str[: value_str_len // 2])
                right_half = int(value_str[value_str_len // 2 :])
                input_arr[idx] = left_half
                input_arr.insert(idx + 1, right_half)
                idx += 1
            else:
                input_arr[idx] *= 2024
            idx += 1
    return input_arr


assert len(blink(str_to_arr("0 1 10 99 999"))) == 7
assert blink(str_to_arr("0 1 10 99 999")) == str_to_arr("1 2024 1 0 9 9 2021976")
assert len(blink(str_to_arr("125 17"), times=25)) == 55312


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read()

    # Part 1
    result1 = len(blink(str_to_arr(input_data), times=25))
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input.txt") == (191690, 24)
    except AssertionError:
        print("❌ wrong")
