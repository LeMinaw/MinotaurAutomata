import numpy as np
from typing import Tuple, Iterable, Generator


# A little bit of sugar for type hints
Array = np.ndarray


def all_equals(iterable: Iterable) -> bool:
    """Return `True` if all elements of a given `iterable` are equals,
    otherwise return `False`.
    """
    return len(set(iterable)) <= 1


def enumerate_arrays(*arrays: Tuple[Array]) -> Generator:
    """Same as NumPy's `ndenumerate` function, except it allows enumerating
    multiple `ndarray`s.
    """
    assert all_equals(a.shape for a in arrays), "Array shape mismatch"
    
    for indexes in np.ndindex(arrays[0].shape):
        yield indexes, (a[indexes] for a in arrays)
