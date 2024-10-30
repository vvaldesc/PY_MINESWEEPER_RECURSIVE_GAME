import numpy as np

array = np.arange(11)

def binary_array_average(array: list):
    if len(array)>0:
        return array[0] + binary_array_average(array[1:])
    else:
        return 0


print(array)
print(binary_array_average(array))