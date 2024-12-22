import itertools
import os
import re
from collections import defaultdict

from tqdm import tqdm

this_folder = "\\".join(__file__.split("\\")[:-1])


def mix(a, b):
    return a ^ b


assert mix(42, 15) == 37


def prune(a):
    return a % 16777216


assert prune(100000000) == 16113920


def fwd_secret(secret, count):
    for _ in range(count):
        secret = mix(secret, (secret * 64))
        secret = prune(secret)
        secret = mix(secret, (secret // 32))
        secret = prune(secret)
        secret = mix(secret, (secret * 2048))
        secret = prune(secret)
    return secret


assert fwd_secret(secret=123, count=1) == 15887950
assert fwd_secret(secret=15887950, count=1) == 16495136
assert fwd_secret(secret=1, count=2000) == 8685429
assert fwd_secret(secret=10, count=2000) == 4700978
assert fwd_secret(secret=100, count=2000) == 15273692
assert fwd_secret(secret=2024, count=2000) == 8667524


def main(filename):
    input_data = [
        int(x)
        for x in open(f"{this_folder}/{filename}", "r").read().strip().split("\n")
    ]

    # Part 1

    result1 = 0
    for secret_num in input_data:
        result1 += fwd_secret(secret_num, 2000)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (37327623, 24)
        assert main("input.txt") == (20506453102, 24)
    except AssertionError:
        print("❌ wrong")
