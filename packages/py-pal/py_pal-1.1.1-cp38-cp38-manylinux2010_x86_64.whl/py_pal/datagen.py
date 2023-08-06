import random
import string
from random import sample
from typing import List, Any

import networkx
from networkx import to_dict_of_lists, fast_gnp_random_graph, path_graph


class KeySelectionType:
    MIDDLE = 'middle'
    LAST = 'last'
    NOT_INCLUDED = 'not included'
    RANDOM = 'random'


def n_(n: int) -> int:
    """Return N."""
    return n


def range_n(n: int, start: int = 0) -> List[int]:
    """Return the sequence [start, start+1, ..., start+N-1]."""
    return list(range(start, start + n))


def integers(n: int, _min: int, _max: int) -> List[int]:
    """Return sequence of N random integers between _min and _max (included)."""
    return [random.randint(_min, _max) for _ in range(n)]


def large_integers(n: int) -> List[int]:
    """Return sequence of N large random integers."""
    return [random.randint(-50, 50) * 1000000 + random.randint(0, 10000) for _ in range(n)]


def strings(n: int, chars=string.ascii_letters) -> str:
    """Return random string of N characters, sampled at random from `chars`."""
    return ''.join([random.choice(chars) for _ in range(n)])


def gen_growing_ints(_range=range(10, 100, 10)):
    """Return lists of argument ints with increasing value."""
    return [[i] for i in _range]


def args_growing_lists(interval=range(-10000, 10000), _range=range(10, 100, 10), sort=False) -> List[List[Any]]:
    """Return lists of arguments lists of random ints with increasing length."""
    return [[sample(interval, i) if not sort else list(sorted(sample(interval, i)))] for i in _range]


def args_growing_lists_with_search_key(interval=range(-10000, 10000), _range=range(10, 100, 10), sort=False,
                                       key=KeySelectionType.NOT_INCLUDED):
    """Return lists of arguments lists of random ints with increasing length and a search key."""
    return [[*gen_search_args(interval, i, key=key, sort=sort)] for i in _range]


def args_growing_graphs(_range=range(2, 20, 2), directed=True, p=0.5) -> List[List[dict]]:
    """Return list of arguments of random graphs with increasing amount of nodes."""
    return [[to_dict_of_lists(fast_gnp_random_graph(n, p, directed=directed))] for n in _range]


def args_growing_graphs_with_source(_range=range(2, 20, 2)) -> List[List[networkx.Graph]]:
    """Return list of arguments of path graphs with increasing amount of nodes and the first node as source node."""
    return [[path_graph(n), 0] for n in _range]


def gen_search_args(interval, length, sort, key):
    random_list = sample(interval, length)
    if sort:
        random_list.sort()

    if key == KeySelectionType.LAST:
        return random_list, random_list[-1]
    if key == KeySelectionType.NOT_INCLUDED:
        return random_list, max(random_list) + 1
    if key == KeySelectionType.RANDOM:
        return random_list, random.choice(random_list)
    if key == KeySelectionType.MIDDLE:
        return random_list, random_list[len(random_list) // 2]
