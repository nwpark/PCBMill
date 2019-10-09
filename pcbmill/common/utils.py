from collections.abc import Hashable
from bitstring import BitArray


def convert_to_iterable(value):
    if hasattr(value, '__iter__'):
        return value
    else:
        return [value]


def convert_to_hashable(value):
    if isinstance(value, Hashable):
        return value
    else:
        return tuple(value)


def convert_to_bit_array(data, length):
    bit_array = BitArray(uint=data, length=length)
    return [int(bit_array[i]) for i in range(bit_array.length)]
