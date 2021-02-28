"""General purpose module to deal with binary cellular automatas."""

import numpy as np
from numpy.random import default_rng
from scipy import signal
from typing import Callable, Tuple, Union

from utils import Array, enumerate_arrays


kernel_3x3 = np.ones((3, 3), dtype=bool)
kernel_3x3[1, 1] = False


def game_of_life_rule(cell: bool, neighbors: int) -> Union[bool, None]:
    """Classic rule of John Conway's Game of Life.\n
    Common notation: `B3/S23`.
    """
    # A low cell switches to high state if is has 3 neighbors
    if not cell and neighbors == 3:
        return True
    # A high cell switches to low state if does not have 2 or 3 neighbors
    elif cell and not neighbors in (2, 3):
        return False


class Automata:
    """Binary cellular automata.\n
    Parameters:
    - shape: Size of the cellular automata world.\n
    - rule: Transition function that will be called on each cell when ticking
        the world. It will be provided the current cell state and the number of
        neighbors it has, and must return either the new cell state as a bool
        or None if no change to the state is required.\n
    - kernel: An array denoting the neighborhood kernel that will be used when
        ticking the world thru convolution. This basically describes where to
        'look' for neighbors.
    """
    def __init__(self,
            shape: Tuple[int, int],
            rule: Callable[[bool, int], Union[bool, None]],
            kernel: Array = kernel_3x3
        ):
        self.shape = shape
        self.rule = rule
        self.kernel = kernel

        self.rng = default_rng()
        self.empty() # Init world attribute
    
    def __str__(self):
        return '\n'.join(
            ''.join('█' if cell else ' ' for cell in line)
            for line in self.world.T
        )

    def empty(self) -> None:
        """Fill in the world with cells at low state."""
        self.world = np.zeros(self.shape, dtype=bool)
    
    def randomize(self, density: float=.5) -> None:
        """Populate the world with random data. Density corresponds to the
        probability for each cell to be in a 'high' state.
        """
        self.world = self.rng.random(self.shape) < density
    
    def count_neighbors(self) -> Array:
        """Return an array of integers depicting how many neighbors each
        cell of the world has.
        """
        # Peform a 2D convolution by the search kernel
        # The 'same' mode ensures the output array has the same shape as the
        # input world
        # By default, world input array will be padded to match kernel size;
        # values over the edges of the world array are condidered to be null
        return signal.convolve2d(
            self.world.astype('u1'), self.kernel, mode='same'
        )

    def tick_world(self) -> None:
        """Compute next cellular automata state."""
        # Neighbors count array
        neighbors = self.count_neighbors()

        for indexes, (cell, neighb) in enumerate_arrays(self.world, neighbors):
            state = self.rule(cell, neighb)
            # Only write to array if the rule returns something meaningful
            if state is not None:
                self.world[indexes] = state


class GameOfLife(Automata):
    """The classical, intemporal Game of Life from John Conway."""
    def __init__(self, shape: Tuple[int, int]):
        super().__init__(shape, game_of_life_rule)


if __name__ == '__main__':
    automata = GameOfLife((80, 20))
    automata.randomize()
    
    while True:
        print(automata)
        automata.tick_world()
        input("Enter to compute next iteration, ^C to quit")
    