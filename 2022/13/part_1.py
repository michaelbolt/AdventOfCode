"""https://adventofcode.com/2022/day/13"""
from typing import List, Any, Union, Optional
import os


def parse_packet_pairs(path: str) -> List[Any]:
    """Parse the provided filepath and return pairs of packets, separated by blank lines."""
    list_of_pairs: List[List[Any]] = []
    packet_pair: List[Any] = []

    print(f"parsing file '{path}'")
    with open(path, "r") as f:
        for line in f:
            line = line.strip()

            # if the line is not empty, it is a new packet to add to the pair
            if line:
                packet_pair.append(eval(line))
                print(f"    new packet: {packet_pair[-1]}")

            # start a new packet set on empty lines
            else:
                print("storing pair of packets")
                list_of_pairs.append(packet_pair)
                packet_pair = []

        # don't leave any packets on the table!
        else:
            if packet_pair:
                list_of_pairs.append(packet_pair)

    return list_of_pairs


def compare_values(
    left: Union[int, list], right: Union[int, list], indent: int = 0
) -> Optional[bool]:
    """Compare two values according to the provided rules.

    Rules:
        - If both values are integers, the lower integer should come first. If the left
            integer is lower than the right integer, the inputs are in the right order.
            If the left integer is higher than the right integer, the inputs are not in
            the right order. Otherwise, the inputs are the same integer; continue
            checking the next part of the input.txt.
        - If both values are lists, compare the first value of each list, then the second
            value, and so on. If the left list runs out of items first, the inputs are in
            the right order. If the right list runs out of items first, the inputs are not
            in the right order. If the lists are the same length and no comparison makes
            a decision about the order, continue checking the next part of the input.txt.
        - If exactly one value is an integer, convert the integer to a list which contains
            that integer as its only value, then retry the comparison. For example, if
            comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2);
            the result is then found by instead comparing [0,0,0] and [2].

    Returns:
        True if values are in the right order, False if values are in the wrong order, or
        None if the search should continue
    """
    print(" " * indent + f"- Compare {left} vs. {right}")
    indent += 4

    # rules if both are integers
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            print(" " * indent + "- (/) left side is smaller")
            return True
        if left > right:
            print(" " * indent + "- (x) right side is smaller")
            return False
        return None

    # rules if both are lists
    if isinstance(left, list) and isinstance(right, list):
        # determine what the return value will be if we run out of items
        if len(left) == len(right):
            rval_if_no_verdict = None
        else:
            rval_if_no_verdict = len(left) < len(right)

        # compare each element until there is a verdict
        for l, r in zip(left, right):
            rval = compare_values(l, r, indent)
            if rval is not None:
                return rval
        else:
            if rval_if_no_verdict is not None:
                print(
                    " " * indent + f"- {'(/)' if rval_if_no_verdict else '(x)'} "
                    f"{'left' if rval_if_no_verdict else 'right'} "
                    f"side ran out of items."
                )
            return rval_if_no_verdict

    # rules if only one input is an int
    # convert the int to a list containing the int
    if isinstance(left, int):
        l = [left]
        r = right
        print(" " * indent + f"- Mixed types; convert left to {l} and retry comparison")
    else:
        l = left
        r = [right]
        print(
            " " * indent + f"- Mixed types; convert right to {r} and retry comparison"
        )
    return compare_values(l, r, indent)


if __name__ == "__main__":
    puzzle_input = "input.txt"  # or "example.txt"

    print(f"parsing puzzle input: {puzzle_input}")
    packet_pairs = parse_packet_pairs(os.path.join(__file__, "..", puzzle_input))

    print("\n\nChecking which pairs are correctly ordered")
    correctly_ordered_pairs = []
    for idx, pair in enumerate(packet_pairs, start=1):
        print(f"\n== Pair {idx} ==")
        correct_order = compare_values(pair[0], pair[1], 0)
        if correct_order:
            correctly_ordered_pairs.append(idx)
    print(f"\nCorrectly ordered pairs: {correctly_ordered_pairs}")
    print(f"Sum of correctly ordered pairs: {sum(correctly_ordered_pairs)}")
