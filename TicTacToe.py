import numpy as np
import pickle
import copy

class Grid:
    def __init__(self,grid=[]):
        self.grid = grid
        self._repr,self._repr_val = self.get_repr()

    def get_repr(self):
        repr = self.grid
        max_eval = valuate_grid(repr)

        for i in range(1,4):
            temp = get_symmetry(self.grid,i)
            eval = valuate_grid(temp)
            if eval > max_eval:
                max_eval = eval
                repr = temp
        
        return repr,max_eval

    def update(self):
        self._repr,self._repr_val = self.get_repr()
    
    def __hash__(self) -> int:
        return self._repr_val
    

    def __eq__(self, value: object) -> bool:
        return self.__hash__() == value.__hash__()


def get_symmetry(grid,axis):
    """
        Return the symmetric equivalent of a 3x3 grid.
        axis:
        - 1 -> y-axis symmetry
        - 2 -> x-axis symmetry
        - 3 -> central symmetry
        - 4 -> up-diag symmetry
        - 5 -> down-diag symmetry
        - 5 -> central symmetry
    """ 
    sym = copy.deepcopy(grid)
    if axis == 1:
        for i in range(3):
            sym[i][0],sym[i][2] = sym[i][2],sym[i][0]
    elif axis == 2:
        for i in range(3):
             sym[0][i],sym[2][i] = sym[2][i],sym[0][i]
    elif axis == 4:
        sym[0][0],sym[2][2] = sym[2][2],sym[0][0]
        sym[0][1],sym[1][2] = sym[1][2],sym[0][1]
        sym[1][0],sym[2][1] = sym[2][1],sym[1][0]
    elif axis == 5:
        for i in range(3):
            for j in range(i):
                sym[i][j],sym[j][i] = sym[j][i],sym[i][j]
    elif axis== 3:
        sym[0][0],sym[2][2] = sym[2][2],sym[0][0]
        sym[0][1],sym[2][1] = sym[2][1],sym[0][1]
        sym[0][2],sym[2][0] = sym[2][0],sym[0][2]
        sym[1][0],sym[1][2] = sym[1][2],sym[1][0]
    return sym

def valuate_grid(grid):
    "Give a numerical representation of a grid"

    num = 0

    for i in range(3):
        num *= 1000
        l = 0
        for j in range(3):
            l *= 10
            l += grid[i][j] + 1
        num += l
    return num

def get_initial_grid():
    """
        Return a 3x3 empty grid 
    """
    return Grid([[0]*3 for _ in range(3)])

def play_at(grid,line,col,player):
    """
        player lets his mark in square (line,col).
        If the move is permited i.e the targeted square 
        is initially empty, this returns True. 
        Else, this returns false
    """
    
    if grid.grid[line][col] == 0:
        grid.grid[line][col] = player
        grid.update()
        return True
    return False


def check_win_from_perspective(grid,player):
    """
        Check if the grid corresponds to a terminal state. 
        Returns 1 if player1 won, -1 if they lost and 0 otherwise
    """

    #Horizontal
    for line in grid.grid:
        if line.count(player) == 3:
            return 1
        elif line.count(player % 2 + 1) == 3:
            return -1
        
    #Vertical 
    transpose = np.array(grid.grid).T
    for line in transpose:

        if list(line).count(player) == 3:
            return 1
        elif list(line).count(player % 2 + 1) == 3:
            return -1
    
    #Diagonal NorthEast-SouthWest
    diagup = [grid.grid[i][i] for i in range(3)]
    if diagup.count(player) == 3:
        return 1
    elif diagup.count(player % 2 + 1) == 3:
        return -1
    
    #Diagonal NorthWest-SouthEast
    diagdown = [grid.grid[i][2-i] for i in range(3)]
    if diagdown.count(player) == 3:
        return 1
    elif diagdown.count(player % 2 + 1) == 3:
        return -1
    
    return 0


def print_grid(grid):
    for line in grid.grid:
        for c in line:
            if c == 1:
                print("X",end="  ")
            elif c == 2:
                print("O",end="  ")
            else:
                print(" ",end="  ")
        print("\n")



if __name__ == "__main__":


    grid = get_initial_grid()
    value_table = {}
    with open("value","rb") as f:
        value_table = pickle.load(f)


    bot_player = 2

    actual_player = 1
    
    stop = False

    count_moves = 0

   
    while not stop and count_moves < 9 :
        if actual_player != bot_player:
            line = int(input("Line : "))
            col = int(input("Column : "))
            while not play_at(grid,line,col,actual_player):
                print("Not Available")
                line = int(input("Line : "))
                col = int(input("Column : "))
        else:
            available = [(i,j) for i in range(3) for j in range(3) if grid.grid[i][j] == 0]
            copies = [copy.deepcopy(grid) for _ in range(len(available))]
            for j in range(len(copies)):
                play_at(copies[j],available[j][0],available[j][1],actual_player)
            best_index = 0
            for k in range(1,len(copies)):
                if bot_player == 1:
                    if value_table[copies[best_index]] < value_table[copies[k]]:
                        best_index = k
                else:
                    if value_table[copies[best_index]] > value_table[copies[k]]:
                        best_index = k

                
            grid = copies[best_index]
        count_moves += 1  
        stop = check_win_from_perspective(grid,actual_player)
        if stop:
            print(f"Victoire de {'X' if actual_player==1 else "O"}")
        actual_player = actual_player % 2 + 1
        print_grid(grid)
    if not stop:
        print("Egalité")
    
    
    