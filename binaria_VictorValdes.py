def binary_array_search(array,n:int,i=0):
    if array.size > 0:
        if array[0] == n:
            return i
        else:
            return binary_array_search(array[1:],n,i+1)
    else:
        return False