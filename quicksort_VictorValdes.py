import numpy as np
'''
def binary_array_sort(array, i=0, sort=True):
    if i < array.size - 1:
        if array[i] > array[i + 1]:
            sort = False
            array[i], array[i + 1] = array[i + 1], array[i]
        return binary_array_sort(array, i + 1, sort)
    else:
        if sort:
            return array
        else:
            return binary_array_sort(array, 0)
'''

def binary_array_sort(array, i=0):
    if i < array.size - 1:
