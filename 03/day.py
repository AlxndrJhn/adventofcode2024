import itertools
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read()

    # Part 1
    result1 = 0
    r_pattern = re.compile(r"mul\(([-\d]{1,3}),([-\d]{1,3})\)")
    for match in r_pattern.finditer(input_data):
        result1 += int(match.group(1)) * int(match.group(2))

    print(f"Part 1 {filename}: ", result1)

    # Part 2
    r_pattern = re.compile(r"mul\(([-\d]{1,3}),([-\d]{1,3})\)|don't\(\)|do\(\)")
    is_active = True
    result2 = 0
    while True:
        match = r_pattern.search(input_data)
        if match is None:
            break
        input_data = input_data[match.end() :]
        if match.group() == "do()":
            is_active = True
        elif match.group() == "don't()":
            is_active = False
        else:
            if is_active:
                result2 += int(match.group(1)) * int(match.group(2))
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input_example.txt") == (161, 161)
    assert main("input_example2.txt") == (161, 48)
    assert main("input.txt") == (178794710, 76729637)
