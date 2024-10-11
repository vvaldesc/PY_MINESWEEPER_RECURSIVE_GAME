import numpy as np

searching_vectors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
table = np.random.randint(-1, 1, size=(8, 8))

def how_many_mines(table,i,j,searching_vectors,c=0):
    if not searching_vectors:
        return c
    else:
        ni, nj = i + searching_vectors[0][0], j + searching_vectors[0][1]
        if 0 <= ni < table.shape[0] and 0 <= nj < table.shape[1]:
            if table[ni,nj] == -1:
                c += 1
        return how_many_mines(table,i,j,searching_vectors[1:],c)


def count_cell_mines(table,i=0,j=0):
    if table[i][j] != -1:
        table[i][j] = how_many_mines(table,i,j,searching_vectors)
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


print(table)
print(count_cell_mines(table))