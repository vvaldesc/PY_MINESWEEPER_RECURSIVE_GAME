import numpy as np

table=np.random.randint(-1, 1, size=(8, 8))

def count_cell_mines(table,i=0,j=0):
    print(table[i][j])
    if i < table.shape[0] - 1:
        i = i + 1
        return count_cell_mines(table,i,j)
    else:
        if j < table.shape[1] - 1:
            i = 0
            j = j + 1
            return count_cell_mines(table,i,j)
        else:
            return table



print(count_cell_mines(table))