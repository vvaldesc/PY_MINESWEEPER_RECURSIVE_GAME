'''
import numpy as np

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



def binary_array_search(array,n:int,i=0):
    if len(array) > 0:
        mid = len(array) // 2
        if array[mid] == n:
            return i + mid
        else:
            if array[mid] > n:
                #izquierda
                return binary_array_search(array[:mid],n,i)
            else:
                #derecha
                return binary_array_search(array[mid+1:],n,i+mid+1)
    else:
        return -1

import numpy as np
array = np.array([10,15,17,24,25,76,129,222])

print(array)
print(binary_array_search(array,76))

x=array[2:5]
x[0]=99
print(x)


