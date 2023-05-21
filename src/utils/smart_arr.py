from typing import Tuple, Type, Union, List

Array = Union[Tuple[float, float], List[float]]

def arr_plus(a1: Array, a2: Array):
    return (a1[0]+a2[0], a1[1]+a2[1])

def arr_sub(a1: Array, a2: Array):
    return (a1[0]-a2[0], a1[1]-a2[1])

def arr_multi(a1: Array, a2: Array):
    return (a1[0]*a2[0], a1[1]*a2[1])

def arr_divide(a1: Array, a2: Array):
    return (a1[0]/a2[0], a1[1]/a2[1])