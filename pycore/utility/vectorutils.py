from collections import deque
from fractions import Fraction
from typing import Any, List, Dict, Tuple

from pycore.core_funcs import stdio


def shift_items(items: List[Any], start_index: int) -> List[Any]:
    """Generic function to shift any list based on the indicated start offset.

    Args:
        items (List[Any]): List of any item.
        start_index (int): The index to start the list from.

    Returns:
        List[Any]: List of any item which ordering has been shifted.
    """
    shift_items = deque(items)
    shift = -start_index
    # stdio.message(f"SHIFT {shift}")
    shift_items.rotate(shift)
    items = list(shift_items)
    return items


def group_list_by_values(list) -> Dict[float, List[Any]]:
    grouped_items: Dict[List] = {}
    for index, i in enumerate(list):
        if type(i) is Fraction:
            i = float(i)
        if not i in grouped_items:
            grouped_items[i] = [index]
        else:
            grouped_items[i].append(index)
    return grouped_items


def group_list_by_values_sequentially(list) -> List[Tuple[float, List[Any]]]:
    grouped_items: List[Tuple[float, List[Any]]] = []
    latest_item = None
    for index, i in enumerate(list):
        if len(grouped_items) == 0:
            grouped_items.append((i, [index]))
        elif latest_item == i:
            grouped_items[-1][1].append(index)
        else:
            grouped_items.append((i, [index]))
        latest_item = i
    return grouped_items
