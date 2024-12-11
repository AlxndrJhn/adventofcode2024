this_folder = "\\".join(__file__.split("\\")[:-1])


def str_to_arr(string):
    return [int(x) for x in string.split(" ")]


def mapping(value):
    value_str = str(value)
    value_str_len = len(value_str)

    if value == 0:
        return [1]
    elif value_str_len % 2 == 0:
        left_half = int(value_str[: value_str_len // 2])
        right_half = int(value_str[value_str_len // 2 :])
        return [left_half, right_half]
    else:
        return [value * 2024]


lookup = {}


def apply_blink_get_stone_count(input_nodes, times):
    if times == 0:
        return len(input_nodes)
    count = 0
    for node in input_nodes:
        remaining_times = times - 1
        if (node, remaining_times) in lookup:
            count += lookup[(node, remaining_times)]
            continue
        count_of_leave = apply_blink_get_stone_count(mapping(node), times - 1)
        lookup[(node, remaining_times)] = count_of_leave
        count += count_of_leave
    return count


assert apply_blink_get_stone_count(str_to_arr("0 1 10 99 999"), times=1) == 7
assert apply_blink_get_stone_count(str_to_arr("0 1 10 99 999"), times=1) == len(
    str_to_arr("1 2024 1 0 9 9 2021976")
)
assert apply_blink_get_stone_count(str_to_arr("125 17"), times=25) == 55312


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read()

    # Part 1
    result1 = apply_blink_get_stone_count(str_to_arr(input_data), times=25)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = apply_blink_get_stone_count(str_to_arr(input_data), times=75)
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input.txt") == (191690, 228651922369703)
    except AssertionError:
        print("❌ wrong")
