"""Module relying on binary cellular automatas to generate labyrinthic
patterns.
"""

from typing import Union, Tuple
from random import random

from automatas import Automata


def minotaur_rule(cell: bool, neighbors: int) -> Union[bool, None]:
    """This rule, found with machine-learing black magic, generates a nice
    labyrinth that percolates reasonably well when used with a 3*3 kernel.\n
    Common rulestring notation: `B3/S01234`.
    """    
    # A low cell switches to high state if is has 3 neighbors
    if not cell and neighbors == 3:
        return True
    # A high cell switches to low state if is has 5 neighbors or more
    elif cell and neighbors >= 5:
        return False


def minotaur_rule_randomized(*args):
    """Slight variation of `minotaur_rule` adding randomly a tiny amount of
    empty cells."""   
    if random() < .001:
        return False
    return minotaur_rule(*args)


def labyrinth_rule(cell: bool, neighbors: int) -> Union[bool, None]:
    """This rule, commonly found in the litterature, generates a labyrinth when
    used with a 3*3 kernel,.\n
    Common rulestring notation: `B3/S12345`.
    """
    # A low cell switches to high state if is has 3 neighbors
    if not cell and neighbors == 3:
        return True
    # A high cell switches to low state if is has no neighbors or more than 6
    elif cell and not (1 <= neighbors <= 5):
        return False


class MinotaurLabyrinth(Automata):
    """This cellular automata generates quite nice labyrinth patterns when
    seeded properly.
    """
    def __init__(self, shape: Tuple[int, int]):
        super().__init__(shape, minotaur_rule)
    
    def seed(self, size: int=3, density: float=.5) -> None:
        """Seeds the world by overwriting a square of `size` by `size` with a
        random pattern at its center."""
        pattern = self.rng.random((size, size)) < density
        
        # Coords of up-left point of the 'seed square'
        x, y = ((s-size) // 2 for s in self.shape)
        self.world[x:x+size, y:y+size] = pattern


if __name__ == '__main__':
    automata = MinotaurLabyrinth((120, 20))
    automata.seed(5)

    while True:
        print(automata)
        automata.tick_world()
        input("Enter to compute next iteration, ^C to quit")
