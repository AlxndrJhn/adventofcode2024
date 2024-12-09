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


def checksum(data):
    hash_ = 0
    for i, x in enumerate(data):
        if x is None:
            continue
        hash_ += i * x
    return hash_


def split_intervals(data):
    file_intervals, free_intervals = [], []
    file_id = 0
    idx_buffer = 0
    for i, x in enumerate(data):
        is_file = i % 2 == 0
        if is_file:
            file_intervals.append(
                (
                    idx_buffer,
                    x,
                )
            )
            file_id += 1
        else:
            free_intervals.append(
                (
                    idx_buffer,
                    x,
                )
            )
        idx_buffer += x
    return file_intervals, free_intervals


def compact_intervals(file_intervals, free_intervals):
    for file_arr_pos, (file_start, file_length) in enumerate(file_intervals[::-1]):
        file_id = len(file_intervals) - file_arr_pos - 1
        for free_i, (free_start, length) in enumerate(free_intervals):
            if free_start > file_start:
                break
            if length >= file_length:
                free_intervals[free_i] = (
                    free_start + file_length,
                    length - file_length,
                )
                file_intervals[file_id] = (free_start, file_length)
                break


def checksum_intervals(file_intervals):
    hash_ = 0
    for file_id, (start, file_length) in enumerate(file_intervals):
        for i in range(file_length):
            hash_ += (i + start) * file_id
    return hash_


def main(filename):
    input_data = [
        int(x) for x in list(open(f"{this_folder}/{filename}", "r").read().strip())
    ]

    # Part 1
    data = inflate(input_data)
    compact(data)
    result1 = checksum(data)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    file_intervals, free_intervals = split_intervals(input_data)
    compact_intervals(file_intervals, free_intervals)
    result2 = checksum_intervals(file_intervals)
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (1928, 2858)
        assert main("input.txt") == (6353658451014, 6382582136592)
    except AssertionError:
        print("❌ wrong")
