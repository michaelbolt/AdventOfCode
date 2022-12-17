"""https://adventofcode.com/2022/day/12"""
import os
import numpy as np
from enum import Enum
from copy import copy


def letter_to_height(char: str) -> int:
    """Cast a letter to an integer distance from 'a' """
    return int(ord(char) - ord("a"))


class Directions(tuple, Enum):
    """TupleEnum to make it easy to walk through 2 dimensions"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    @property
    def np(self):
        return np.array(self.value)


def shortest_path_between(topo, start, stop, path):
    """ Find the shortest path on the topography map """
    # update path with current step
    path.append(start)

    # if we're there, return the path
    if np.all(start == stop):
        return path

    # find the shortest path - worst case is visiting every square
    shortest_path = [1] * topo.size

    # iterate over directions
    for direction in Directions:
        new_position = start + direction.np

        # no loops
        if any(np.all(step == new_position) for step in path):
            continue

        # no leaving the map
        if not 0 <= new_position[0] < topo.shape[0]:
            continue
        if not 0 <= new_position[1] < topo.shape[1]:
            continue

        # can only climb up/down by 1 unit
        if abs(topo[tuple(new_position)] - topo[tuple(start)]) > 1:
            continue

        # search from the new point - keep the shortest
        new_path = shortest_path_between(topo, new_position, stop, copy(path))
        if len(new_path) < len(shortest_path):
            shortest_path = new_path

    return shortest_path


# make a 2D array of data
with open(os.path.join(__file__, "..", "input.txt"), "r") as f:
    topography = np.array(
        [
            [
                letter_to_height(char)
                for char in line.strip()
            ] for line in f
        ]
    )

# find start / stop and replace with real heights
start = np.argwhere(topography == -14)[0]  # S
stop = np.argwhere(topography == -28)[0]  # E
topography[tuple(start)] = 0
topography[tuple(stop)] = 25

# print map and the number of steps on the shortest path
print(topography)
print(len(shortest_path_between(topography, start, stop, [])) - 1)
