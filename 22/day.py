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


def part1(filename):
    input_data = [
        int(x)
        for x in open(f"{this_folder}/{filename}", "r").read().strip().split("\n")
    ]
    result1 = 0
    for secret_num in input_data:
        result1 += fwd_secret(secret_num, 2000)
    print(f"Part 1 {filename}: ", result1)

    return result1


def gen_secrets(secret, count):
    secrets = []
    for _ in range(count):
        secret = mix(secret, (secret * 64))
        secret = prune(secret)
        secret = mix(secret, (secret // 32))
        secret = prune(secret)
        secret = mix(secret, (secret * 2048))
        secret = prune(secret)
        secrets.append(secret)
    return secrets


def part2(filename):
    input_data = [
        int(x)
        for x in open(f"{this_folder}/{filename}", "r").read().strip().split("\n")
    ]

    def num_to_price(num):
        return int(str(num)[-1])

    available_seqs = defaultdict(set)
    batch_to_win = defaultdict(dict)
    for secret_num in input_data:
        sec_seq = gen_secrets(secret_num, 2000)
        prices = [num_to_price(secret_num)] + [num_to_price(s) for s in sec_seq]
        price_changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
        for batch_of_4 in range(len(price_changes) - 4):
            batch = tuple(price_changes[batch_of_4 : batch_of_4 + 4])
            if batch in batch_to_win[secret_num]:
                continue
            price_at_4 = prices[batch_of_4 + 4]
            batch_to_win[secret_num][batch] = price_at_4
            available_seqs[secret_num].add(batch)
    union_all = set.union(*available_seqs.values())
    best_sum = 0
    for batch in tqdm(union_all):
        sum_of_batch = 0
        for secret_num in input_data:
            sum_of_batch += batch_to_win[secret_num].get(batch, 0)
        if sum_of_batch > best_sum:
            best_sum = sum_of_batch
    result2 = best_sum
    print(f"Part 2 {filename}: ", result2)

    return result2


if __name__ == "__main__":
    try:
        assert part1("input_example.txt") == 37327623
        assert part1("input.txt") == 20506453102
        assert part2("input_example2.txt") == 23
        assert part2("input.txt") == 2423
    except AssertionError:
        print("❌ wrong")
