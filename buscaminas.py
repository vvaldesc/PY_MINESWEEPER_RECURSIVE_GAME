from logging import exception

import numpy as np

searching_vectors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


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

def descubre(table,i,j):
    if table.shape != (8, 8):
        exception('Table dimensions are incorrect')
        return True, table
    else:
        table_aux = table.copy()
        #Me veo obligado a hacer una copia de table ya que por lo visto el parámetro se envía por referencia
        minesweeper_table =  count_cell_mines(table_aux)
        del table_aux
        #print(table)
        #print(minesweeper_table)

        def mine_near():
            table[i][j] = -2
            return False, table
        def no_mines():
            table[max(0, i - 1):min(i + 2, 8), max(0, j - 1):min(j + 2, 8)] = \
                minesweeper_table[max(0, i - 1):min(i + 2, 8),
                max(0, j - 1):min(j + 2, 8)]
            return False, table
        def mine():
            print('BUUUUUMMMMM!!!!')
            return True, table
        switch = [
            (lambda x: x == -1, mine),
            (lambda x: x == 0, no_mines),
            (lambda x: x > 0, mine_near)
        ]
        def evaluate_cases(value):
            for case, action in switch:
                if case(value):
                    return action()
            return True, table

        return evaluate_cases(table[i][j])


def minesweeper():
    table = np.random.randint(-1, 1, size=(8, 8))
    finish = False
    print('Minesweeper')
    #print(table)
    while not finish:
        try:
            i = int(input('Dame la fila'))
            j = int(input('Dame la columna'))
            finish, table = descubre(table, i, j)
            print("NUEVO TABLEROO")
            print(table)
        except ValueError as e:
            print(f"Error: {e}. Por favor, ingresa un número válido.")


minesweeper()
