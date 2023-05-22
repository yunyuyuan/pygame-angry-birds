from typing import Tuple, Type, Union, List

Array = Union[Tuple[float, float], List[float]]
ArrayTarget = Union[Array, float]

def arr_plus(a1: Array, a2: ArrayTarget):
    if isinstance(a2, (float, int)):
        a2 = (a2, a2)
    return (a1[0]+a2[0], a1[1]+a2[1])

def arr_sub(a1: Array, a2: ArrayTarget):
    if isinstance(a2, (float, int)):
        a2 = (a2, a2)
    return (a1[0]-a2[0], a1[1]-a2[1])

def arr_multi(a1: Array, a2: ArrayTarget):
    if isinstance(a2, (float, int)):
        a2 = (a2, a2)
    return (a1[0]*a2[0], a1[1]*a2[1])

def arr_divide(a1: Array, a2: ArrayTarget):
    if isinstance(a2, (float, int)):
        a2 = (a2, a2)
    return (a1[0]/a2[0], a1[1]/a2[1])