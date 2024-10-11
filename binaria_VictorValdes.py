import numpy as np

a=np.random.randint(0,2, size=500)
b=np.arange(100)

def binary_array_search(array,n:int,i=0):
    if array.size > 0:
        if array[0] == n:
            return i
        else:
            array = np.delete(array,0)
            return binary_array_search(array,n,i+1)
    else:
        return False


print(binary_array_search(a,1))
print(binary_array_search(b,45))
print(binary_array_search(b,200))
