import itertools
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])

FREE = "."


def inflate(data):
    length = sum(data)
    buffer = [None] * length
    idx_buffer = 0
    file_id = 0
    for i, x in enumerate(data):
        is_file = i % 2 == 0
        for j in range(x):
            if is_file:
                buffer[idx_buffer] = file_id
            idx_buffer += 1
        if is_file:
            file_id += 1
    return buffer


def compact(data):
    for i in range(len(data) - 1, -1, -1):
        if data[i] is not None:
            last_not_none_idx = i
            break
    first_none_idx = data.index(None)
    while True:
        if first_none_idx - 1 == last_not_none_idx:
            break
        data[first_none_idx], data[last_not_none_idx] = (
            data[last_not_none_idx],
            data[first_none_idx],
        )
        while data[last_not_none_idx] is None:
            last_not_none_idx -= 1
        while data[first_none_idx] is not None:
            first_none_idx += 1
    return data


def checksum(data):
    hash_ = 0
    for i, x in enumerate(data):
        if x is None:
            continue
        hash_ += i * x
    return hash_


def main(filename):
    input_data = [
        int(x) for x in list(open(f"{this_folder}/{filename}", "r").read().strip())
    ]

    # Part 1

    inflated = inflate(input_data)
    compacted = compact(inflated)
    result1 = checksum(compacted)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (1928, 24)
        assert main("input.txt") == (42, 24)
    except AssertionError:
        print("❌ wrong")
