import itertools
import os
import re
from collections import defaultdict

from tqdm import tqdm

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().strip().split("\n")

    # Part 1
    pc_to_pcs = defaultdict(set)
    for connection in input_data:
        pc1, pc2 = connection.split("-")
        pc_to_pcs[pc1].add(pc2)
        pc_to_pcs[pc2].add(pc1)
    # find groups of 3
    groups_of_3 = set()
    for pc1 in pc_to_pcs:
        for pc2 in pc_to_pcs[pc1]:
            for pc3 in pc_to_pcs[pc2]:
                if pc3 in pc_to_pcs[pc1]:
                    if any(t.startswith("t") for t in [pc1, pc2, pc3]):
                        groups_of_3.add(tuple(sorted([pc1, pc2, pc3])))

    result1 = len(groups_of_3)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    def bron_kerbosch(r, p, x):
        if not p and not x:
            return tuple(sorted(r))
        largest = None
        for v in p.copy():
            r_v = r.copy()
            r_v.add(v)
            p_v = p.intersection(pc_to_pcs[v])
            x_v = x.intersection(pc_to_pcs[v])
            largest_clique = bron_kerbosch(r_v, p_v, x_v)
            if largest_clique is not None and (
                largest is None or len(largest_clique) > len(largest)
            ):
                largest = largest_clique
            p.remove(v)
            x.add(v)
        return largest

    result2 = ",".join(bron_kerbosch(set(), set(pc_to_pcs.keys()), set()))

    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (7, "co,de,ka,ta")
        assert main("input.txt") == (1238, "bg,bl,ch,fn,fv,gd,jn,kk,lk,pv,rr,tb,vw")
    except AssertionError:
        print("❌ wrong")
