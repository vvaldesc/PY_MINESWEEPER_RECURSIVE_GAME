import numpy as np

array = np.arange(11)

def binary_array_average(array,s=0,i=0):
    if array.size > 1:
        return binary_array_average(array[:1],s+array[i-1],i+1)
    else:
        return (s + array[i-1])/(i + 1)


print(array)
print(binary_array_average(array))