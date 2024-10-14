'''

If input array not sorted

def binary_array_search(array,n:int,i=0):
    if array.size > 0:
        if array[0] == n:
            return i
        else:
            return binary_array_search(array[1:],n,i+1)
    else:
        return False
'''
import numpy as np


def binary_array_search(array,n:int,i=0):
    if array.size > 0:
        mid = array.size // 2
        if array[mid] == n:
            return i + mid
        else:
            if array[mid] > n:
                return binary_array_search(array[:mid],n,i)
            else:
                #derecha
                return binary_array_search(array[mid+1:],n,i + mid+1)
    else:
        return False


array = np.arange(8)
print(array)
print(binary_array_search(array,7))