import re

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    gate_states_str, logic_str = (
        open(f"{this_folder}/{filename}", "r").read().strip().split("\n\n")
    )
    gate_states = {}
    for gate_state_str in gate_states_str.split("\n"):
        gate, state = gate_state_str.split(": ")
        gate_states[gate] = int(state)
    logic = []
    re_pattern = re.compile(r"([\w]+) (AND|OR|XOR) ([\w]+) -> ([\w]+)")
    all_z_gates = set()
    for line in logic_str.split("\n"):
        i1, op, i2, out = re_pattern.match(line).groups()
        logic.append((i1, op, i2, out))
        if out.startswith("z"):
            all_z_gates.add(out)

    # Part 1
    while not all(gate_states.get(gate) is not None for gate in all_z_gates):
        for i1, op, i2, out in logic:
            i1 = gate_states.get(i1)
            i2 = gate_states.get(i2)
            if i1 is None or i2 is None:
                continue
            if op == "AND":
                gate_states[out] = i1 & i2
            elif op == "OR":
                gate_states[out] = i1 | i2
            elif op == "XOR":
                gate_states[out] = i1 ^ i2
            else:
                raise ValueError(f"Unknown op {op}")
    sorted_z_asc = sorted(
        [(gate, state) for gate, state in gate_states.items() if gate.startswith("z")],
        reverse=True,
        key=lambda x: x[0],
    )
    result1 = int("".join(map(str, [x[1] for x in sorted_z_asc])), 2)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (4, 24)
        assert main("input_example2.txt") == (2024, 24)
        assert main("input.txt") == (48063513640678, 24)
    except AssertionError:
        print("❌ wrong")
