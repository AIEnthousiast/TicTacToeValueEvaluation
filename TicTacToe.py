import numpy as np
def get_initial_grid():
    """
        Return a 3x3 empty grid 
    """
    return [[0]*3 for _ in range(3)]

def play_at(grid,line,col,player):
    """
        player lets his mark in square (line,col).
        If the move is permited i.e the targeted square 
        is initially empty, this returns True. 
        Else, this returns false
    """

    if grid[line][col] == 0:
        grid[line][col] = player
        return True
    return False


def check_win_from_perspective(grid,player):
    """
        Check if the grid corresponds to a terminal state. 
        Returns 1 if player1 won, -1 if they lost and 0 otherwise
    """

    #Horizontal
    for line in grid:
        if line.count(player) == 3:
            return 1
        elif line.count(player % 2 + 1) == 3:
            return -1
        
    #Vertical 
    transpose = np.array(grid).T
    for line in transpose:

        if list(line).count(player) == 3:
            return 1
        elif list(line).count(player % 2 + 1) == 3:
            return -1
    
    #Diagonal NorthEast-SouthWest
    diagup = [grid[i][i] for i in range(3)]
    if diagup.count(player) == 3:
        return 1
    elif diagup.count(player % 2 + 1) == 3:
        return -1
    
    #Diagonal NorthWest-SouthEast
    diagdown = [grid[i][2-i] for i in range(3)]
    if diagdown.count(player) == 3:
        return 1
    elif diagdown.count(player % 2 + 1) == 3:
        return -1
    
    return 0


def print_grid(grid):
    for line in grid:
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

    actual_player = 1
    
    stop = False

    count_moves = 0
    while not stop and count_moves < 9 :
        print_grid(grid)
        line = int(input("Line : "))
        col = int(input("Column : "))
        while not play_at(grid,line,col,actual_player):
            print("Not Available")
            line = int(input("Line : "))
            col = int(input("Column : "))

        count_moves += 1  
        stop = check_win_from_perspective(grid,actual_player)
        if stop:
            print(f"Victoire de {'X' if actual_player==1 else "O"}")
        actual_player = actual_player % 2 + 1
    print_grid(grid)
    if not stop:
        print("Egalité")