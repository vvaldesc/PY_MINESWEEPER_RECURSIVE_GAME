from logging import exception
from time import sleep
import numpy as np
import pygame

CELL_SIDE_SIZE = 32 #cell size in TAD
SOURCE_SIDE_SIZE = 32 #cell size in source

i_offset = 150
j_offset = 200

WINDOW_SIZE = 550

def rect(i: int, j: int):
    return i * CELL_SIDE_SIZE + i_offset, j * CELL_SIDE_SIZE + j_offset,CELL_SIDE_SIZE, CELL_SIDE_SIZE

BOMB_SOURCE = (SOURCE_SIDE_SIZE * 2, SOURCE_SIDE_SIZE * 2, SOURCE_SIDE_SIZE, SOURCE_SIDE_SIZE)
FLAG_SOURCE = (SOURCE_SIDE_SIZE * 3, SOURCE_SIDE_SIZE * 2, SOURCE_SIDE_SIZE, SOURCE_SIDE_SIZE)
WALL_SOURCE = (SOURCE_SIDE_SIZE * 1, SOURCE_SIDE_SIZE * 2, SOURCE_SIDE_SIZE, SOURCE_SIDE_SIZE)
FLOOR_SOURCE = (SOURCE_SIDE_SIZE * 0, SOURCE_SIDE_SIZE * 2, SOURCE_SIDE_SIZE, SOURCE_SIDE_SIZE)

font_path = 'assets/font/PressStart2P-vaV7.ttf'

image = None

def number_source(n: int):
    n = n - 1
    i = n % 4
    j = n // 4
    return SOURCE_SIDE_SIZE * i, SOURCE_SIDE_SIZE * j, SOURCE_SIDE_SIZE * (i + 1), SOURCE_SIDE_SIZE * (j + 1)

searching_vectors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
# MAX limits the size of the board because it is specified in the 'descubre' exercise section
# The rest of the functions treat the matrix as a dynamic matrix
MAX = 8
game_table = np.zeros((MAX, MAX), dtype=int)

def init_gui():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

    global image
    try:
        image = pygame.image.load("assets/img/minesweeper.png").convert_alpha()
        image = pygame.transform.scale(image, (128, 96))
    except pygame.error as e:
        print(f"Error al cargar la imagen: {e}")
        image = None
        finish_gui()
        return -1

    screen.fill((255, 255, 255))
    font = pygame.font.Font(font_path, 42)
    text = font.render('Minesweeper', True, (0, 0, 0))
    TextRect = text.get_rect()
    TextRect.center = (WINDOW_SIZE // 2, 85)
    screen.blit(text, TextRect)
    pygame.display.set_caption('Minesweeper')
    pygame.display.set_icon(image)

    return screen

def finish_gui():
    pygame.quit()

def draw_table(table,display):

    for j, row in enumerate(table):
        for i, cell in enumerate(row):
            if cell == -1:
                draw_bomb(i, j, display)
            elif cell == (-2):
                draw_flag(i, j, display)
            elif cell == 0:
                draw_wall(i, j, display)
            elif cell == -3:
                draw_floor(i, j, display)
            else:
                if cell > 0:
                    draw_number(i, j, number_source(cell),display)

    pygame.display.update()


def draw_flag(i: int, j: int, display):
    display.blit(image, rect(i,j), FLAG_SOURCE)

def draw_bomb(i: int, j: int, display):
    display.blit(image, rect(i, j), BOMB_SOURCE)

def draw_number(i: int, j: int, source, display):
    display.blit(image, rect(i,j), source)

def draw_wall(i: int, j: int, display):
    display.blit(image, rect(i,j), WALL_SOURCE)

def draw_floor(i: int, j: int, display):
    display.blit(image, rect(i,j), FLOOR_SOURCE)


#This function counts the number of mines near the selected cell recursively using 'searching_vectors' vectors
def how_many_mines(table, i, j, search_vectors, c=0):
    if not search_vectors:
        return c
    else:
        ni, nj = i + search_vectors[0][0], j + search_vectors[0][1]
        if 0 <= ni < table.shape[0] and 0 <= nj < table.shape[1]:
            if table[ni,nj] == -1:
                c += 1
        return how_many_mines(table, i, j, search_vectors[1:], c)

#This function edits the minesweeper table to create the table that shows where are the bombs to the client.
def count_cell_mines(table, i=0, j=0):
    if table[i][j] != -1:
        table[i][j] = how_many_mines(table,i,j,searching_vectors)
    if i < table.shape[0] - 1:
        return count_cell_mines(table,i+1,j)
    else:
        if j < table.shape[1] - 1:
            return count_cell_mines(table,0,j+1)
        else:
            return table

#This function shows the bombs in the main table
def discover_bombs(bombs_table, game_table):
    rows, cols = bombs_table.shape
    for i in range(rows):
        for j in range(cols):
            if bombs_table[i, j] == -1:
                game_table[i, j] = -1

    return np.where(game_table == 0, -3, game_table)

#This function replace the values of the selected depending on the value of the cell
def discover(table,i,j):
    def discover_near(x=i, y=j):
        region = minesweeper_table[max(0, x - 1):min(x + 2, 8), max(0, y - 1):min(y + 2, 8)]
        table[max(0, x - 1):min(x + 2, 8), max(0, y - 1):min(y + 2, 8)] = region
        # No entiendo bien el warning del segundo parámetro
        region = np.where(region == -1, -4, region)
        region = np.where(region == 0, -3, region)
        region = np.where(region == -4, 0, region)
        game_table[max(0, x - 1):min(x + 2, 8), max(0, y - 1):min(y + 2, 8)] = region

    if table.shape != (8, 8):
        exception('Table dimensions are incorrect')
        return True, table
    else:
        table_aux = table.copy()
        minesweeper_table =  count_cell_mines(table_aux)
        print('Bombs near table:')
        print(minesweeper_table)
        del table_aux

        def mine_near():
            game_table[i][j] = -2
            return False, table

        def no_mines():
            # Discovers the zeros island
            def discover_zeros_island(x=i, y=j):
                # Return the island's vectors
                def zeros_island(x_aux, y_aux, table_island, visited=np.zeros((8, 8), dtype=bool)):
                    if x_aux < 0 or x_aux >= table_island.shape[0] or y_aux < 0 or y_aux >= table_island.shape[1]:
                        return []
                    if table_island[x_aux][y_aux] != 0 or visited[x_aux, y_aux]:
                        return []

                    # Switch cell to visited
                    visited[x_aux, y_aux] = True
                    island = [(x_aux, y_aux)]

                    # Recursive adjacent cells search
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    for dx, dy in directions:
                        island += zeros_island(x_aux + dx, y_aux + dy, table_island, visited)

                    return island

                # Discovering process
                island = zeros_island(x, y, minesweeper_table.copy())
                for x, y in island:
                    discover_near(x, y)

            discover_zeros_island()
            return False, table

        def mine():
            return True, table

        # This function chooses what to do in each case
        def evaluate_cases(value):
            if value == -1:
                return mine()
            elif value == 0:
                return no_mines()
            elif value > 0:
                return mine_near()

        return evaluate_cases(minesweeper_table[i][j])

#This function checks winning
def win(table, bombs_table):
    # Copy of original table
    table_aux = table.copy()

    # Refresh table with the bombs
    rows, cols = bombs_table.shape
    for i in range(rows):
        for j in range(cols):
            if bombs_table[i, j] == -1:
                table_aux[i, j] = -1

    # Verifica cada celda en table_aux
    for row in table_aux:
        for cell in row:
            if cell == 0:
                return False
    return True

#This function is the mail function of the game
def minesweeper():

    # Low probability of bomb
    values = np.array([-1, 0])
    probabilities = np.array([0.1, 0.9])
    table = np.random.choice(values, size=(MAX, MAX), p=probabilities)

    # Testing table

    # table = np.zeros((MAX, MAX), dtype=int)
    # table[1,0]=-1


    screen=init_gui()
    draw_table(game_table,screen)



    finish = False
    print('WELCOME TO MINESWEEPER\n\n')
    sleep(1)
    print('\nTHESE ARE THE MINES')
    print(table)
    sleep(1)
    print('\nTHIS IS YOUR GAME')
    print(game_table)
    sleep(1)

    while not finish:
        try:
            while True:
                try:
                    i = int(input('\nIntruduce row :'))
                    j = int(input('Intruduce column :'))
                    if i < MAX and j < MAX:
                        break
                    else:
                        print(f"Out of bounds!\n")
                except ValueError as e:
                    print(f"Error: {e}. Please input a valid number.")

            if i >= MAX or j >= MAX:
                raise ValueError
            finish, table = discover(table, i, j)
            print("\n")

            if win(game_table, table):
                print("YOU WIN!")
                draw_table(game_table,screen)
                sleep(2)
                finish_gui()
                break

            if finish:
                print(table)
                print("BOOOOOOOOOOOMMM YOU LOST")
                draw_table(discover_bombs(table,game_table),screen)
                sleep(2)
                finish_gui()
            else:
                print("CONTINUE!\n")
                print(game_table)
                draw_table(game_table,screen)


        except ValueError as e:
            print(f"Error: {e}. Please input a valid number.")

minesweeper()