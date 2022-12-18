"""https://adventofcode.com/2022/day/13#part2"""
from typing import List, Any, Union, Optional, Callable
import os


def parse_all_packets(path: str) -> List[Any]:
    """Parse the provided filepath and return a list of packets. """
    packets: List[Any] = []

    print(f"parsing file '{path}'")
    with open(path, "r") as f:
        for line in f:
            line = line.strip()

            # if the line is not empty, it is a new packet to keep
            if line:
                packets.append(eval(line))
                print(f"    new packet: {packets[-1]}")

    return packets


def compare_values(left: Union[int, list], right: Union[int, list]) -> Optional[bool]:
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
    # rules if both are integers
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right

    # rules if both are lists
    if isinstance(left, list) and isinstance(right, list):
        # determine what the return value will be if we run out of items
        if len(left) == len(right):
            rval_if_no_verdict = None
        else:
            rval_if_no_verdict = len(left) < len(right)

        # compare each element until there is a verdict
        for l, r in zip(left, right):
            rval = compare_values(l, r)
            if rval is not None:
                return rval
        else:
            return rval_if_no_verdict

    # rules if only one input.txt is an int
    l = [left] if isinstance(left, int) else left
    r = [right] if isinstance(right, int) else right
    return compare_values(l, r)


def sort_packets(packets: List[Any]) -> List[any]:
    """Sort the provided list of packets a la Bubble Sort.

    Args:
        packets: list of Packets to sort
    """
    start_index = 0
    while start_index < len(packets):

        # loop over the range, looking for the smallest value
        smallest_value_idx = start_index
        for idx in range(start_index, len(packets)):
            if not compare_values(packets[smallest_value_idx], packets[idx]):
                smallest_value_idx = idx

        # swap the starting value with the newly found smallest value
        packets[start_index], packets[smallest_value_idx] = (
            packets[smallest_value_idx],
            packets[start_index],
        )
        start_index += 1
    return packets


def find_packet_index(
    packets: List[Any], value: Any, start_from: int = 1
) -> Optional[int]:
    """Returns the index of the desired packet in the provided packet list."""
    for idx, packet in enumerate(packets, start=start_from):
        if packet == value:
            return idx
    return None


if __name__ == "__main__":
    puzzle_input = "input.txt"  # or "example.txt"

    print(f"parsing puzzle input: {puzzle_input}")
    packets = parse_all_packets(os.path.join(__file__, "..", puzzle_input))

    print("\nadding divider packets...")
    packets.append([[2]])
    packets.append([[6]])

    print("\nsorting packets...")
    sorted_packets = sort_packets(packets)
    print("\n".join(str(packet) for packet in sorted_packets))

    print("\nfinding divider packets: ")
    divider_1 = find_packet_index(sorted_packets, [[2]])
    divider_2 = find_packet_index(sorted_packets, [[6]])
    print(f"  {divider_1} * {divider_2} = {divider_1 * divider_2}")
