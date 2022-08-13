from fractions import Fraction
from typing import Any, List, Dict, Tuple


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
