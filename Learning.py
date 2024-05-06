from TicTacToe import *
import copy
import pickle
import random
import numpy as np
from collections import defaultdict
import time


def constant_schedule(value):
    def get_schedule(i):
        return value
    
    return get_schedule



def temporal_difference_learning(number_of_games,alpha=lambda i: 0.01,exploration=lambda i : 0.1,construct=True):
    if construct:
        print("Constructing initial value table...")
        value_table = construct_initial_value_table()
        print('Initial value table constructed')
    else:
        print("Loading value table...")
        with open("value","rb") as f:
            value_table = pickle.load(f)
        print("Value table loaded...")

    for i in range(number_of_games):
        print(f"{i/number_of_games * 100} %.....")
        actual = get_initial_grid()
        next = None
        prec_1 = None
        prec_2 = None
        player = 1
        moves = 0
        while check_win_from_perspective(actual,player) == 0 and moves < 9:
            available = [(i,j) for i in range(3) for j in range(3) if actual.grid[i][j] == 0]
            if random.random() < exploration(i/number_of_games):
                m = random.choice(available)
                prec_1 = None
                prec_2 = None
                play_at(actual,m[0],m[1],player)
            else:
                copies = [copy.deepcopy(actual) for _ in range(len(available))]
                for j in range(len(copies)):
                    play_at(copies[j],available[j][0],available[j][1],player)
                best_index = 0
                for k in range(1,len(copies)):
                    if copies[k] not in value_table.keys():
                        print_grid(copies[k])
                        print(copies[k].__hash__())
                    if player == 1:
                        if value_table[copies[best_index]] < value_table[copies[k]]:
                            best_index = k
                    else:
                        if value_table[copies[best_index]] > value_table[copies[k]]:
                            best_index = k
                
                prec_2 = prec_1
                prec_1 = copy.deepcopy(actual)
                if prec_2 is not None:
                    value_table[prec_2] = np.clip(value_table[prec_2] + alpha(i/number_of_games)*(value_table[copies[best_index]] - value_table[prec_2]),0,1)
                actual = copies[best_index]
            player = player % 2 + 1
            moves += 1


    print("Training over")
    with open("value","wb") as f:
        pickle.dump(dict(value_table),f)
    print("Saved in value")

def construct_initial_value_table():
    
    def construct_initial_value_table_from(grid,player,line,column,move_count):
        play_at(grid,line,column,player)
        move_count += 1
        
        if grid not in value_table.keys():
            if check_win_from_perspective(grid,player) != 0:
                value_table[grid] = 1 if player == 1 else 0
            else:
                if move_count == 9:
                    value_table[grid] = 0
                else:
                    value_table[grid] = 0.5
                    available_pos = [(i,j) for i in range(3) for j in range(3) if grid.grid[i][j] == 0]
                    for pos in available_pos:
                        construct_initial_value_table_from(copy.deepcopy(grid),player % 2 + 1, pos[0],pos[1],move_count)

    grid = get_initial_grid()

    value_table = {}
    value_table[grid] = 0.5

    available_pos = [(i,j) for i in range(3) for j in range(3) if grid.grid[i][j] == 0]
    for pos in available_pos:
        construct_initial_value_table_from(copy.deepcopy(grid),1, pos[0],pos[1],0)


    return value_table

"""  
if __name__ == '__main__':

    temporal_difference_learning(1000,construct=True)
    value_table = {}
    with open("value","rb") as f:
        value_table = pickle.load(f)

   

    for k,v in list(value_table.items()):
        if (v > 0.5  or v < 0.5) and v != 0 and v != 1:
            print_grid(k)
            print(k.grid)
            print(k.__hash__())
            print(v)

    print(len(value_table.items()))

"""
if __name__ == "__main__":

    temporal_difference_learning(1000000,alpha=constant_schedule(0.001),exploration=constant_schedule(0.5),construct=True)
    
    