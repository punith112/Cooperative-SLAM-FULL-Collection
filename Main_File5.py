'''
Created on Dec 16, 2016

@author: Rajish
'''
# 0 = North, 1 = East, 2 = South, 3 = West



from Five_robot_functions import cp_field_value, first_map_update, matching, get_level, all_good_values,\
    map_merge
from Five_robot_functions import motion_deciding_function, var_update, adj_field_value
import pygame, copy, sys
from pygame import *
import time

global real_map, occ, one_two_done, one_three_done, one_four_done, one_five_done, two_three_done, two_four_done, two_five_done, three_four_done, three_five_done, four_five_done

# Variables from main algo...



map_choice = [0,0,0,0,0]

map_choice[2] = [[1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0], # Map choices....
                [0,0,0,1,0,0,0,0,1,0,0,0,0,1,1,1],
                [0,1,1,1,1,1,1,1,1,0,0,0,0,1,0,1],
                [0,0,1,0,0,0,0,0,1,1,1,1,1,1,1,1],
                [0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
                [0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
                [0,0,1,0,0,0,1,1,1,1,1,1,1,1,1,1],
                [0,0,1,1,1,1,1,0,0,1,0,0,0,1,0,0],
                [1,1,1,0,0,0,1,0,0,1,0,0,0,1,0,0],
                [1,0,0,0,1,1,1,0,0,1,0,0,0,1,1,1],
                [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
                [1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0],
                [1,1,1,0,0,1,0,0,0,0,0,1,0,0,0,0],
                [0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
                [0,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0]]
map_choice[0] = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                 [1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
                 [1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],
                 [1,0,1,0,1,1,1,1,1,1,1,1,0,1,0,1],
                 [1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,1],
                 [1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,1],
                 [1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1],
                 [1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1],
                 [1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,1],
                 [1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1],
                 [1,0,1,0,1,0,0,0,0,0,0,0,0,1,0,1],
                 [1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
                 [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                 [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

map_choice[1] = [[1,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0],
                 [0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0],
                 [0,1,0,0,0,0,1,1,1,1,1,1,0,0,0,1],
                 [0,1,1,1,0,0,0,0,0,1,0,0,0,0,1,1],
                 [0,0,0,1,0,0,0,0,1,1,0,0,0,1,1,0],
                 [0,0,0,1,1,1,0,0,1,0,0,0,0,1,0,0],
                 [1,1,0,0,0,1,1,1,1,1,1,0,0,1,0,0],
                 [0,1,1,1,0,0,0,0,1,0,1,1,1,1,0,0],
                 [0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0],
                 [0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0],
                 [0,0,0,1,0,0,0,0,1,0,0,1,1,1,0,0],
                 [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
                 [0,0,1,1,0,0,0,1,1,0,0,0,0,1,0,0],
                 [0,1,1,0,0,0,1,1,0,0,0,1,1,1,1,0],
                 [0,1,0,0,0,0,1,0,0,0,1,1,0,0,1,1],
                 [1,1,0,0,0,0,1,0,0,0,1,0,0,0,0,1]]

map_choice[3] = [[1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1],
                 [0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
                 [0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1],
                 [1,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1],
                 [1,1,1,1,1,1,0,0,1,0,1,1,0,0,0,1],
                 [1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],
                 [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
                 [1,0,1,1,1,1,0,0,0,0,1,1,1,1,1,1],
                 [1,0,1,0,0,1,0,0,1,0,1,0,0,0,0,1],
                 [1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,1],
                 [1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0],
                 [1,0,1,0,0,1,0,0,0,0,1,0,1,1,1,0],
                 [1,1,1,1,1,1,0,0,0,0,1,0,0,0,1,1],
                 [1,0,1,0,0,1,0,0,0,0,1,0,0,0,1,0],
                 [1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0],
                 [1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0]]

map_choice[4] = [[0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                 [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                 [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                 [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                 [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                 [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                 [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                 [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                 [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

#Variables for the pygame display part...


WIN_WIDTH = 5*200
WIN_HEIGHT = 300
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#ffffff"
 
PLATFORM_WIDTH = 10
PLATFORM_HEIGHT = 10



#Running the one-time-running program...
def main():     #     The variables are all seperately declared. And oop is not used a lot.  
    mat1 = [[0]]    # My primary objective was to make this thing work before my defense... And hey! IT WORKS!!!
    mat2 = [[0]]
    mat3 = [[0]]
    mat4 = [[0]]
    mat5 = [[0]]
    
    one_two_done = 0
    one_three_done = 0
    one_four_done = 0
    one_five_done = 0
    two_three_done = 0
    two_four_done = 0
    two_five_done = 0
    three_four_done = 0
    three_five_done = 0
    four_five_done = 0
    
    orient1 = 0      #always oriented towards the north at the beginning...
    orient2 = 0      #always oriented towards the north at the beginning...
    orient3 = 0      #always oriented towards the north at the beginning...
    orient4 = 0
    orient5 = 0
    
    r12_a = 0
    r12_b = 0
    r12_c = 0
    r12_d = 0
    
    r13_a = 0
    r13_b = 0
    r13_c = 0
    r13_d = 0
    
    r14_a = 0
    r14_b = 0
    r14_c = 0
    r14_d = 0
    
    r15_a = 0
    r15_b = 0
    r15_c = 0
    r15_d = 0
    
    r23_a = 0
    r23_b = 0
    r23_c = 0
    r23_d = 0
    
    r24_a = 0
    r24_b = 0
    r24_c = 0
    r24_d = 0
    
    r25_a = 0
    r25_b = 0
    r25_c = 0
    r25_d = 0
    
    r34_a = 0
    r34_b = 0
    r34_c = 0
    r34_d = 0
    
    r35_a = 0
    r35_b = 0
    r35_c = 0
    r35_d = 0
    
    r45_a = 0
    r45_b = 0
    r45_c = 0
    r45_d = 0
    
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("5 Robots map")
        
    bg = Surface((WIN_WIDTH,WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))
    
    
    choice = input("Please enter the map_choice: 0 through 4:")
    real_map = map_choice[choice]
    
    rcinput = True
    while rcinput == True:
        row_cp_map1 = input("Enter the row number of the starting position for Robot 1: ")
        col_cp_map1 = input("Enter the col number of the starting position for Robot 1: ")
        row_cp_map2 = input("Enter the row number of the starting position for Robot 2: ")
        col_cp_map2 = input("Enter the col number of the starting position for Robot 2: ")
        row_cp_map3 = input("Enter the row number of the starting position for Robot 3: ")
        col_cp_map3 = input("Enter the col number of the starting position for Robot 3: ")
        row_cp_map4 = input("Enter the row number of the starting position for Robot 4: ")
        col_cp_map4 = input("Enter the col number of the starting position for Robot 4: ")
        row_cp_map5 = input("Enter the row number of the starting position for Robot 5: ")
        col_cp_map5 = input("Enter the col number of the starting position for Robot 5: ")
        comp_var = input("Enter a value between from 3 through 6 to decide the size of the matrices to compare")
        user_match_perc = input("Enter a value from 60 to 90. This value is the acceptable percentage for matrix comparisons")
        
        if real_map[row_cp_map1][col_cp_map1] == 0:
            print "Please enter integers from 0 through 15 which have a '1' in the map for Robot 1"
            rcinput = True
        elif real_map[row_cp_map2][col_cp_map2] == 0:
            print "Please enter integers from 0 through 15 which have a '1' in the map for Robot 2"
            rcinput = True
        elif real_map[row_cp_map3][col_cp_map3] == 0:
            print "Please enter integers from 0 through 15 which have a '1' in the map for Robot 3"
            rcinput = True
        elif real_map[row_cp_map4][col_cp_map4] == 0:
            print "Please enter integers from 0 through 15 which have a '1' in the map for Robot 4"
            rcinput = True
        elif real_map[row_cp_map5][col_cp_map5] == 0:
            print "Please enter integers from 0 through 15 which have a '1' in the map for Robot 5"
            rcinput = True
        else: 
            rcinput = False
    
    row_cp_local1 = 1    # These values will be 1 at the start
    col_cp_local1 = 1
    row_cp_local2 = 1    # These values will be 1 at the start
    col_cp_local2 = 1
    row_cp_local3 = 1    # These values will be 1 at the start
    col_cp_local3 = 1
    row_cp_local4 = 1    # These values will be 1 at the start
    col_cp_local4 = 1
    row_cp_local5 = 1    # These values will be 1 at the start
    col_cp_local5 = 1
    
    
    
    afv1 = adj_field_value(row_cp_map1, col_cp_map1, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position
    afv2 = adj_field_value(row_cp_map2, col_cp_map2, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position
    afv3 = adj_field_value(row_cp_map3, col_cp_map3, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position
    afv4 = adj_field_value(row_cp_map4, col_cp_map4, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position
    afv5 = adj_field_value(row_cp_map5, col_cp_map5, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position

    fv1 = cp_field_value(afv1)
    fv2 = cp_field_value(afv2)
    fv3 = cp_field_value(afv3)
    fv4 = cp_field_value(afv4)
    fv5 = cp_field_value(afv5)
    
    mat1 = first_map_update(fv1, afv1)
    mat2 = first_map_update(fv2, afv2)
    mat3 = first_map_update(fv3, afv3)
    mat4 = first_map_update(fv4, afv4)
    mat5 = first_map_update(fv5, afv5)
#     
#     agv = all_good_values(real_map)
#     

    steps = 0
    
    done = 0
    while done == 0:
        if one_two_done == 1:
            nmap12 = map_merge(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
            if nmap12[0] == 1:
                mat1 = nmap12[1][0]
                row_cp_local1 = nmap12[1][2][0] + row_cp_local1
                col_cp_local1 = nmap12[1][2][1] + col_cp_local1
                mat2 = nmap12[1][1]
                row_cp_local2 = nmap12[1][2][2] + row_cp_local2
                col_cp_local2 = nmap12[1][2][3] + col_cp_local2
                r12_a = nmap12[1][3]
                r12_b = nmap12[1][4]
                r12_c = nmap12[1][3]
                r12_d = nmap12[1][4]
                print "Merge 12"     
        if one_three_done == 1:
            nmap13 = map_merge(r13_a, r13_b, r13_c, r13_d, mat1, mat3, 1)
            if nmap13[0] == 1:
                mat1 = nmap13[1][0]
                row_cp_local1 = nmap13[1][2][0] + row_cp_local1
                col_cp_local1 = nmap13[1][2][1] + col_cp_local1
                mat3 = nmap13[1][1]
                row_cp_local3 = nmap13[1][2][2] + row_cp_local3
                col_cp_local3 = nmap13[1][2][3] + col_cp_local3
                r13_a = nmap13[1][3]
                r13_b = nmap13[1][4]
                r13_c = nmap13[1][3]
                r13_d = nmap13[1][4]
                print "Merge 13"
        if one_four_done == 1:
            nmap14 = map_merge(r14_a, r14_b, r14_c, r14_d, mat1, mat4, 1)
            if nmap14[0] == 1:
                mat1 = nmap14[1][0]
                row_cp_local1 = nmap14[1][2][0] + row_cp_local1
                col_cp_local1 = nmap14[1][2][1] + col_cp_local1
                mat4 = nmap14[1][1]
                row_cp_local4 = nmap14[1][2][2] + row_cp_local4
                col_cp_local4 = nmap14[1][2][3] + col_cp_local4
                r14_a = nmap14[1][3]
                r14_b = nmap14[1][4]
                r14_c = nmap14[1][3]
                r14_d = nmap14[1][4]
                print "Merge 14"
        if one_five_done == 1:
            nmap15 = map_merge(r15_a, r15_b, r15_c, r15_d, mat1, mat5, 1)
            if nmap15[0] == 1:
                mat1 = nmap15[1][0]
                row_cp_local1 = nmap15[1][2][0] + row_cp_local1
                col_cp_local1 = nmap15[1][2][1] + col_cp_local1
                mat5 = nmap15[1][1]
                row_cp_local5 = nmap15[1][2][2] + row_cp_local5
                col_cp_local5 = nmap15[1][2][3] + col_cp_local5
                r15_a = nmap15[1][3]
                r15_b = nmap15[1][4]
                r15_c = nmap15[1][3]
                r15_d = nmap15[1][4]
                print "Merge 15"
        if two_three_done == 1:
            nmap23 = map_merge(r23_a, r23_b, r23_c, r23_d, mat2, mat3, 1)
            if nmap23[0] == 1:
                mat2 = nmap23[1][0]
                row_cp_local2 = nmap23[1][2][0] + row_cp_local2
                col_cp_local2 = nmap23[1][2][1] + col_cp_local2
                mat3 = nmap23[1][1]
                row_cp_local3 = nmap23[1][2][2] + row_cp_local3
                col_cp_local3 = nmap23[1][2][3] + col_cp_local3
                r23_a = nmap23[1][3]
                r23_b = nmap23[1][4]
                r23_c = nmap23[1][3]
                r23_d = nmap23[1][4]  
                print "Merge 23"
        if two_four_done == 1:
            nmap24 = map_merge(r24_a, r24_b, r24_c, r24_d, mat2, mat4, 1)
            if nmap24[0] == 1:
                mat2 = nmap24[1][0]
                row_cp_local2 = nmap24[1][2][0] + row_cp_local2
                col_cp_local2 = nmap24[1][2][1] + col_cp_local2
                mat4 = nmap24[1][1]
                row_cp_local4 = nmap24[1][2][2] + row_cp_local4
                col_cp_local4 = nmap24[1][2][3] + col_cp_local4
                r24_a = nmap24[1][3]
                r24_b = nmap24[1][4]
                r24_c = nmap24[1][3]
                r24_d = nmap24[1][4]
                print '"Merge 24"'
        if two_five_done == 1:
            nmap25 = map_merge(r25_a, r25_b, r25_c, r25_d, mat2, mat5, 1)
            if nmap25[0] == 1:
                mat2 = nmap25[1][0]
                row_cp_local2 = nmap25[1][2][0] + row_cp_local2
                col_cp_local2 = nmap25[1][2][1] + col_cp_local2
                mat5 = nmap25[1][1]
                row_cp_local5 = nmap25[1][2][2] + row_cp_local5
                col_cp_local5 = nmap25[1][2][3] + col_cp_local5
                r25_a = nmap25[1][3]
                r25_b = nmap25[1][4]
                r25_c = nmap25[1][3]
                r25_d = nmap25[1][4]
                print "Merge 25"
        if three_four_done == 1:
            nmap34 = map_merge(r34_a, r34_b, r34_c, r34_d, mat3, mat4, 1)
            if nmap34[0] == 1:
                mat3 = nmap34[1][0]
                row_cp_local3 = nmap34[1][2][0] + row_cp_local3
                col_cp_local3 = nmap34[1][2][1] + col_cp_local3
                mat4 = nmap34[1][1]
                row_cp_local4 = nmap34[1][2][2] + row_cp_local4
                col_cp_local4 = nmap34[1][2][3] + col_cp_local4
                r34_a = nmap34[1][3]
                r34_b = nmap34[1][4]
                r34_c = nmap34[1][3]
                r34_d = nmap34[1][4]
                print "Merge 34"
        if three_five_done == 1:
            nmap35 = map_merge(r35_a, r35_b, r35_c, r35_d, mat3, mat5, 1)
            if nmap35[0] == 1:
                mat3 = nmap35[1][0]
                row_cp_local3 = nmap35[1][2][0] + row_cp_local3
                col_cp_local3 = nmap35[1][2][1] + col_cp_local3
                mat5 = nmap35[1][1]
                row_cp_local5 = nmap35[1][2][2] + row_cp_local5
                col_cp_local5 = nmap35[1][2][3] + col_cp_local5
                r35_a = nmap35[1][3]
                r35_b = nmap35[1][4]
                r35_c = nmap35[1][3]
                r35_d = nmap35[1][4]
                print "Merge 35"
        if four_five_done == 1:
            nmap45 = map_merge(r45_a, r45_b, r45_c, r45_d, mat4, mat5, 1)
            if nmap45[0] == 1:
                mat4 = nmap45[1][0]
                row_cp_local4 = nmap45[1][2][0] + row_cp_local4
                col_cp_local4 = nmap45[1][2][1] + col_cp_local4
                mat5 = nmap45[1][1]
                row_cp_local5 = nmap45[1][2][2] + row_cp_local5
                col_cp_local5 = nmap45[1][2][3] + col_cp_local5
                r45_a = nmap45[1][3]
                r45_b = nmap45[1][4]
                r45_c = nmap45[1][3]
                r45_d = nmap45[1][4]
                print "Merge 45"
        
        
        for eve in pygame.event.get():    #To finish python process when you click the cross button...
            if eve.type == QUIT:
                raise SystemExit("QUIT")
        
        screen.blit(bg, (0,0))
        
        answer1 = motion_deciding_function(mat1, orient1, row_cp_local1, col_cp_local1, afv1)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
        answer2 = motion_deciding_function(mat2, orient2, row_cp_local2, col_cp_local2, afv2)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
        answer3 = motion_deciding_function(mat3, orient3, row_cp_local3, col_cp_local3, afv3)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
        answer4 = motion_deciding_function(mat4, orient4, row_cp_local4, col_cp_local4, afv4)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
        answer5 = motion_deciding_function(mat5, orient5, row_cp_local5, col_cp_local5, afv5)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
        #print "answer1 = ", answer1
        #print "answer2 = ", answer2
        #print "answer3 = ", answer3
        print "MDF"
        steps += 1
        
        if answer3 == 0:
            row_next_pos3 = row_cp_local3 - 1
            col_next_pos3 = col_cp_local3
            row_cp_map3 = row_cp_map3 - 1
        elif answer3 == 1:
            row_next_pos3 = row_cp_local3
            col_next_pos3 = col_cp_local3 + 1
            col_cp_map3 = col_cp_map3 + 1
        elif answer3 == 2:
            row_next_pos3 = row_cp_local3 + 1
            col_next_pos3 = col_cp_local3
            row_cp_map3 = row_cp_map3 + 1
        elif answer3 == 3:
            row_next_pos3 = row_cp_local3
            col_next_pos3 = col_cp_local3 - 1
            col_cp_map3 = col_cp_map3 - 1
        #print 'Mat3 = ', mat3
        
        if answer1 == 0:
            row_next_pos1 = row_cp_local1 - 1
            col_next_pos1 = col_cp_local1
            row_cp_map1 = row_cp_map1 - 1
        elif answer1 == 1:
            row_next_pos1 = row_cp_local1
            col_next_pos1 = col_cp_local1 + 1
            col_cp_map1 = col_cp_map1 + 1
        elif answer1 == 2:
            row_next_pos1 = row_cp_local1 + 1
            col_next_pos1 = col_cp_local1
            row_cp_map1 = row_cp_map1 + 1
        elif answer1 == 3:
            row_next_pos1 = row_cp_local1
            col_next_pos1 = col_cp_local1 - 1
            col_cp_map1 = col_cp_map1 - 1
        #print 'Mat1 = ', mat1
        
        if answer2 == 0:
            row_next_pos2 = row_cp_local2 - 1
            col_next_pos2 = col_cp_local2
            row_cp_map2 = row_cp_map2 - 1
        elif answer2 == 1:
            row_next_pos2 = row_cp_local2
            col_next_pos2 = col_cp_local2 + 1
            col_cp_map2 = col_cp_map2 + 1
        elif answer2 == 2:
            row_next_pos2 = row_cp_local2 + 1
            col_next_pos2 = col_cp_local2
            row_cp_map2 = row_cp_map2 + 1
        elif answer2 == 3:
            row_next_pos2 = row_cp_local2
            col_next_pos2 = col_cp_local2 - 1
            col_cp_map2 = col_cp_map2 - 1
        #print 'Mat2 = ', mat2
        
        if answer4 == 0:
            row_next_pos4 = row_cp_local4 - 1
            col_next_pos4 = col_cp_local4
            row_cp_map4 = row_cp_map4 - 1
        elif answer4 == 1:
            row_next_pos4 = row_cp_local4
            col_next_pos4 = col_cp_local4 + 1
            col_cp_map4 = col_cp_map4 + 1
        elif answer4 == 2:
            row_next_pos4 = row_cp_local4 + 1
            col_next_pos4 = col_cp_local4
            row_cp_map4 = row_cp_map4 + 1
        elif answer4 == 3:
            row_next_pos4 = row_cp_local4
            col_next_pos4 = col_cp_local4 - 1
            col_cp_map4 = col_cp_map4 - 1
        #print 'Mat4 = ', mat4
        
        if answer5 == 0:
            row_next_pos5 = row_cp_local5 - 1
            col_next_pos5 = col_cp_local5
            row_cp_map5 = row_cp_map5 - 1
        elif answer5 == 1:
            row_next_pos5 = row_cp_local5
            col_next_pos5 = col_cp_local5 + 1
            col_cp_map5 = col_cp_map5 + 1
        elif answer5 == 2:
            row_next_pos5 = row_cp_local5 + 1
            col_next_pos5 = col_cp_local5
            row_cp_map5 = row_cp_map5 + 1
        elif answer5 == 3:
            row_next_pos5 = row_cp_local5
            col_next_pos5 = col_cp_local5 - 1
            col_cp_map5 = col_cp_map5 - 1
        #print 'Mat5 = ', mat5
        
        
#         print 'row_next_pos1 = ', row_next_pos1
#         print 'col_next_pos1 = ', col_next_pos1
#         print 'row_cp_map1 = ', row_cp_map1
#         print 'col_cp_map1 = ', col_cp_map1
#         print 'row_next_pos2 = ', row_next_pos2
#         print 'col_next_pos2 = ', col_next_pos2
#         print 'row_cp_map2 = ', row_cp_map2
#         print 'col_cp_map2 = ', col_cp_map2
#         
#         print 'row_next_pos3 = ', row_next_pos3
#         print 'col_next_pos3 = ', col_next_pos3
#         print 'row_cp_map3 = ', row_cp_map3
#         print 'col_cp_map3 = ', col_cp_map3
        #raw_input("Press Enter to continue...")
            
        afv1 = adj_field_value(row_cp_map1, col_cp_map1, real_map)
        afv2 = adj_field_value(row_cp_map2, col_cp_map2, real_map)
        afv3 = adj_field_value(row_cp_map3, col_cp_map3, real_map)
        afv4 = adj_field_value(row_cp_map4, col_cp_map4, real_map)
        afv5 = adj_field_value(row_cp_map5, col_cp_map5, real_map)
        print "AFV obtained"
#         print afv1
#         print afv2
#         print afv3
        fv1 = cp_field_value(afv1)
        #print fv1
        fv2 = cp_field_value(afv2)
        #print fv2
        fv3 = cp_field_value(afv3)
        #print fv3
        fv4 = cp_field_value(afv4)
        #print fv4
        fv5 = cp_field_value(afv5)
        #print fv5
        print "FV obtained"
        # Updating variables for robot 1    
        var_list1 = var_update(mat1, row_next_pos1, col_next_pos1, row_cp_map1, col_cp_map1, row_cp_local1, col_cp_local1, orient1, fv1, afv1)
        var_list2 = var_update(mat2, row_next_pos2, col_next_pos2, row_cp_map2, col_cp_map2, row_cp_local2, col_cp_local2, orient2, fv2, afv2)
        var_list3 = var_update(mat3, row_next_pos3, col_next_pos3, row_cp_map3, col_cp_map3, row_cp_local3, col_cp_local3, orient3, fv3, afv3)
        var_list4 = var_update(mat4, row_next_pos4, col_next_pos4, row_cp_map4, col_cp_map4, row_cp_local4, col_cp_local4, orient4, fv4, afv4)
        var_list5 = var_update(mat5, row_next_pos5, col_next_pos5, row_cp_map5, col_cp_map5, row_cp_local5, col_cp_local5, orient5, fv5, afv5)
        
        print "Variable Updates obtained"
        
        mat1 = var_list1[0]
        row_next_pos1 = var_list1[1]
        col_next_pos1 = var_list1[2]
        row_cp_map1 = var_list1[3]
        col_cp_map1 = var_list1[4]
        row_cp_local1 = var_list1[5]
        col_cp_local1 = var_list1[6]
        orient1 = var_list1[7]
        
        mat2 = var_list2[0]
        row_next_pos2 = var_list2[1]
        col_next_pos2 = var_list2[2]
        row_cp_map2 = var_list2[3]
        col_cp_map2 = var_list2[4]
        row_cp_local2 = var_list2[5]
        col_cp_local2 = var_list2[6]
        orient2 = var_list2[7]
        
        mat3 = var_list3[0]
        row_next_pos3 = var_list3[1]
        col_next_pos3 = var_list3[2]
        row_cp_map3 = var_list3[3]
        col_cp_map3 = var_list3[4]
        row_cp_local3 = var_list3[5]
        col_cp_local3 = var_list3[6]
        orient3 = var_list3[7]
        
        mat4 = var_list4[0]
        row_next_pos4 = var_list4[1]
        col_next_pos4 = var_list4[2]
        row_cp_map4 = var_list4[3]
        col_cp_map4 = var_list4[4]
        row_cp_local4 = var_list4[5]
        col_cp_local4 = var_list4[6]
        orient4 = var_list4[7]
        
        mat5 = var_list5[0]
        row_next_pos5 = var_list5[1]
        col_next_pos5 = var_list5[2]
        row_cp_map5 = var_list5[3]
        col_cp_map5 = var_list5[4]
        row_cp_local5 = var_list5[5]
        col_cp_local5 = var_list5[6]
        orient5 = var_list5[7]
         
        if var_list1[8] == 'N':
            r12_a = r12_a + 1
            r13_a = r13_a + 1
            r14_a = r14_a + 1
            r15_a = r15_a + 1
        elif var_list1[8] == 'W':
            r12_b = r12_b + 1
            r13_b = r13_b + 1
            r14_b = r14_b + 1
            r15_b = r15_b + 1
        if var_list2[8] == 'N':
            r23_a = r23_a + 1
            r24_a = r24_a + 1
            r25_a = r25_a + 1
            r12_c = r12_c + 1
        elif var_list2[8] == 'W':
            r23_b = r23_b + 1
            r24_b = r24_b + 1
            r25_b = r25_b + 1
            r12_d = r12_d + 1
        if var_list3[8] == 'N':
            r34_a = r34_a + 1
            r35_a = r35_a + 1
            r13_c = r13_c + 1
            r12_c = r12_c + 1
        elif var_list3[8] == 'W':
            r34_b = r34_b + 1
            r35_b = r35_b + 1
            r13_d = r13_d + 1
            r12_d = r12_d + 1
        if var_list4[8] == 'N':
            r45_a = r45_a + 1
            r14_c = r14_c + 1
            r24_c = r24_c + 1
            r34_c = r34_c + 1
        if var_list4[8] == 'W':
            r45_b = r45_b + 1
            r14_d = r14_d + 1
            r24_d = r24_d + 1
            r34_d = r34_d + 1
        if var_list5[8] == 'N':
            r15_c = r15_c + 1
            r25_c = r25_c + 1
            r35_c = r35_c + 1
            r45_c = r45_c + 1
        if var_list5[8] == 'W':
            r15_d = r15_d + 1
            r25_d = r25_d + 1
            r35_d = r35_d + 1
            r45_d = r45_d + 1
        
        print 'Mat1 = ', mat1
        print 'Mat2 = ', mat2
        print 'Mat3 = ', mat3
        print 'Mat4 = ', mat4
        print 'Mat5 = ', mat5
#         
#         print 'row_cp_local1 = ',row_cp_local1
#         print 'col_cp_local1 = ', col_cp_local1
#         print 'row_cp_map1 = ', row_cp_map1
#         print 'col_cp_map1 = ', col_cp_map1
#         print 'orient1 = ',orient1
#         
#         print 'row_cp_local2 = ',row_cp_local2
#         print 'col_cp_local2 = ', col_cp_local2
#         print 'row_cp_map2 = ', row_cp_map2
#         print 'col_cp_map2 = ', col_cp_map2
#         print 'orient2 = ',orient2
#     
#         print 'row_cp_local3 = ',row_cp_local3
#         print 'col_cp_local3 = ', col_cp_local3
#         print 'row_cp_map3 = ', row_cp_map3
#         print 'col_cp_map3 = ', col_cp_map3
#         print 'orient3 = ',orient3
    
        #print 'row_next_pos = ', row_next_pos
        #print 'col_next_pos = ', col_next_pos
        #raw_input("Press Enter to continue...")
        '''
        Here you have updated mats. 
        Inside a loop, now, we compare them according to set standards...
        Then if they match, we merge them and update the mats as well as the other variables are updated...
        Then we go out of the loop and continue on the map until we finish the map.
        '''
        if one_two_done == 1:
            nmap12 = map_merge(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
            if nmap12[0] == 1:
                mat1 = nmap12[1][0]
                row_cp_local1 = nmap12[1][2][0] + row_cp_local1
                col_cp_local1 = nmap12[1][2][1] + col_cp_local1
                mat2 = nmap12[1][1]
                row_cp_local2 = nmap12[1][2][2] + row_cp_local2
                col_cp_local2 = nmap12[1][2][3] + col_cp_local2
                r12_a = nmap12[1][3]
                r12_b = nmap12[1][4]
                r12_c = nmap12[1][3]
                r12_d = nmap12[1][4]
                print "Merge 12"                     
        else:
            matched12 = matching(mat1, mat2, comp_var, user_match_perc)
            if matched12[0] == 1:
                one_two_done = 1
                mat1 = matched12[1][0]
                row_cp_local1 = matched12[1][2][0] + row_cp_local1
                col_cp_local1 = matched12[1][2][1] + col_cp_local1
                mat2 = matched12[1][1]
                row_cp_local2 = matched12[1][2][2] + row_cp_local2
                col_cp_local2 = matched12[1][2][3] + col_cp_local2
                r12_a = matched12[1][3]
                r12_b = matched12[1][4]
                r12_c = matched12[1][3]
                r12_d = matched12[1][4]
                
                print 'Mat1 and Mat2 have been merged at step = ', steps
                
        if one_three_done == 1:
            nmap13 = map_merge(r13_a, r13_b, r13_c, r13_d, mat1, mat3, 1)
            if nmap13[0] == 1:
                mat1 = nmap13[1][0]
                row_cp_local1 = nmap13[1][2][0] + row_cp_local1
                col_cp_local1 = nmap13[1][2][1] + col_cp_local1
                mat3 = nmap13[1][1]
                row_cp_local3 = nmap13[1][2][2] + row_cp_local3
                col_cp_local3 = nmap13[1][2][3] + col_cp_local3
                r13_a = nmap13[1][3]
                r13_b = nmap13[1][4]
                r13_c = nmap13[1][3]
                r13_d = nmap13[1][4]
                print "Merge 13"
        else:
            matched13 = matching(mat1, mat3, comp_var, user_match_perc)
            if matched13[0] == 1:
                one_three_done = 1
                mat1 = matched13[1][0]
                row_cp_local1 = matched13[1][2][0] + row_cp_local1
                col_cp_local1 = matched13[1][2][1] + col_cp_local1
                mat3 = matched13[1][1]
                row_cp_local3 = matched13[1][2][2] + row_cp_local3
                col_cp_local3 = matched13[1][2][3] + col_cp_local3
                r13_a = matched13[1][3]
                r13_b = matched13[1][4]
                r13_c = matched13[1][3]
                r13_d = matched13[1][4]
                print 'Mat1 and Mat3 have been merged at step = ', steps
        
        if one_four_done == 1:
            nmap14 = map_merge(r14_a, r14_b, r14_c, r14_d, mat1, mat4, 1)
            if nmap14[0] == 1:
                mat1 = nmap14[1][0]
                row_cp_local1 = nmap14[1][2][0] + row_cp_local1
                col_cp_local1 = nmap14[1][2][1] + col_cp_local1
                mat4 = nmap14[1][1]
                row_cp_local4 = nmap14[1][2][2] + row_cp_local4
                col_cp_local4 = nmap14[1][2][3] + col_cp_local4
                r14_a = nmap14[1][3]
                r14_b = nmap14[1][4]
                r14_c = nmap14[1][3]
                r14_d = nmap14[1][4]
                print "Merge 14"   
        else:
            matched14 = matching(mat1, mat4, comp_var, user_match_perc)
            if matched14[0] == 1:
                one_four_done = 1
                mat1 = matched14[1][0]
                row_cp_local1 = matched14[1][2][0] + row_cp_local1
                col_cp_local1 = matched14[1][2][1] + col_cp_local1
                mat4 = matched14[1][1]
                row_cp_local4 = matched14[1][2][2] + row_cp_local4
                col_cp_local4 = matched14[1][2][3] + col_cp_local4
                r14_a = matched14[1][3]
                r14_b = matched14[1][4]
                r14_c = matched14[1][3]
                r14_d = matched14[1][4]
                print 'Mat1 and Mat4 have been merged at step = ', steps
                
        if one_five_done == 1:
            nmap15 = map_merge(r15_a, r15_b, r15_c, r15_d, mat1, mat5, 1)
            if nmap15[0] == 1:
                mat1 = nmap15[1][0]
                row_cp_local1 = nmap15[1][2][0] + row_cp_local1
                col_cp_local1 = nmap15[1][2][1] + col_cp_local1
                mat5 = nmap15[1][1]
                row_cp_local5 = nmap15[1][2][2] + row_cp_local5
                col_cp_local5 = nmap15[1][2][3] + col_cp_local5
                r15_a = nmap15[1][3]
                r15_b = nmap15[1][4]
                r15_c = nmap15[1][3]
                r15_d = nmap15[1][4]
                print "Merge 15"
        else:
            matched15 = matching(mat1, mat5, comp_var, user_match_perc)
            if matched15[0] == 1:
                one_five_done = 1
                mat1 = matched15[1][0]
                row_cp_local1 = matched15[1][2][0] + row_cp_local1
                col_cp_local1 = matched15[1][2][1] + col_cp_local1
                mat5 = matched15[1][1]
                row_cp_local5 = matched15[1][2][2] + row_cp_local5
                col_cp_local5 = matched15[1][2][3] + col_cp_local5
                r15_a = matched15[1][3]
                r15_b = matched15[1][4]
                r15_c = matched15[1][3]
                r15_d = matched15[1][4]
                print 'Mat1 and Mat5 have been merged at step = ', steps
        if two_three_done == 1:
            nmap23 = map_merge(r23_a, r23_b, r23_c, r23_d, mat2, mat3, 1)
            if nmap23[0] == 1:
                mat2 = nmap23[1][0]
                row_cp_local2 = nmap23[1][2][0] + row_cp_local2
                col_cp_local2 = nmap23[1][2][1] + col_cp_local2
                mat3 = nmap23[1][1]
                row_cp_local3 = nmap23[1][2][2] + row_cp_local3
                col_cp_local3 = nmap23[1][2][3] + col_cp_local3
                r23_a = nmap23[1][3]
                r23_b = nmap23[1][4]
                r23_c = nmap23[1][3]
                r23_d = nmap23[1][4]  
                print "Merge 23"
        else:      
            matched23 = matching(mat2, mat3, comp_var, user_match_perc)
            if matched23[0] == 1:
                two_three_done = 1
                mat2 = matched23[1][0]
                row_cp_local2 = matched23[1][2][0] + row_cp_local2
                col_cp_local2 = matched23[1][2][1] + col_cp_local2
                mat3 = matched23[1][1]
                row_cp_local3 = matched23[1][2][2] + row_cp_local3
                col_cp_local3 = matched23[1][2][3] + col_cp_local3
                r23_a = matched23[1][3]
                r23_b = matched23[1][4]
                r23_c = matched23[1][3]
                r23_d = matched23[1][4]
                print 'Mat2 and Mat3 have been merged at step = ', steps
                
        if two_four_done == 1:
            nmap24 = map_merge(r24_a, r24_b, r24_c, r24_d, mat2, mat4, 1)
            if nmap24[0] == 1:
                mat2 = nmap24[1][0]
                row_cp_local2 = nmap24[1][2][0] + row_cp_local2
                col_cp_local2 = nmap24[1][2][1] + col_cp_local2
                mat4 = nmap24[1][1]
                row_cp_local4 = nmap24[1][2][2] + row_cp_local4
                col_cp_local4 = nmap24[1][2][3] + col_cp_local4
                r24_a = nmap24[1][3]
                r24_b = nmap24[1][4]
                r24_c = nmap24[1][3]
                r24_d = nmap24[1][4]
                print '"Merge 24"'
        else:
            matched24 = matching(mat2, mat4, comp_var, user_match_perc)
            if matched24[0] == 1:
                two_four_done = 1
                mat2 = matched24[1][0]
                row_cp_local2 = matched24[1][2][0] + row_cp_local2
                col_cp_local2 = matched24[1][2][1] + col_cp_local2
                mat4 = matched24[1][1]
                row_cp_local4 = matched24[1][2][2] + row_cp_local4
                col_cp_local4 = matched24[1][2][3] + col_cp_local4
                r24_a = matched24[1][3]
                r24_b = matched24[1][4]
                r24_c = matched24[1][3]
                r24_d = matched24[1][4]
                print 'Mat2 and Mat4 have been merged at step = ', steps
            
        if two_five_done == 1:
            nmap25 = map_merge(r25_a, r25_b, r25_c, r25_d, mat2, mat5, 1)
            if nmap25[0] == 1:
                mat2 = nmap25[1][0]
                row_cp_local2 = nmap25[1][2][0] + row_cp_local2
                col_cp_local2 = nmap25[1][2][1] + col_cp_local2
                mat5 = nmap25[1][1]
                row_cp_local5 = nmap25[1][2][2] + row_cp_local5
                col_cp_local5 = nmap25[1][2][3] + col_cp_local5
                r25_a = nmap25[1][3]
                r25_b = nmap25[1][4]
                r25_c = nmap25[1][3]
                r25_d = nmap25[1][4]
                print "Merge 25"
        else:
            matched25 = matching(mat2, mat5, comp_var, user_match_perc)
            if matched25[0] == 1:
                two_five_done = 1
                mat2 = matched25[1][0]
                row_cp_local2 = matched25[1][2][0] + row_cp_local2
                col_cp_local2 = matched25[1][2][1] + col_cp_local2
                mat5 = matched25[1][1]
                row_cp_local5 = matched25[1][2][2] + row_cp_local5
                col_cp_local5 = matched25[1][2][3] + col_cp_local5
                r25_a = matched25[1][3]
                r25_b = matched25[1][4]
                r25_c = matched25[1][3]
                r25_d = matched25[1][4]
                print 'Mat2 and Mat5 have been merged at step = ', steps
            
        if three_four_done == 1:
            nmap34 = map_merge(r34_a, r34_b, r34_c, r34_d, mat3, mat4, 1)
            if nmap34[0] == 1:
                mat3 = nmap34[1][0]
                row_cp_local3 = nmap34[1][2][0] + row_cp_local3
                col_cp_local3 = nmap34[1][2][1] + col_cp_local3
                mat4 = nmap34[1][1]
                row_cp_local4 = nmap34[1][2][2] + row_cp_local4
                col_cp_local4 = nmap34[1][2][3] + col_cp_local4
                r34_a = nmap34[1][3]
                r34_b = nmap34[1][4]
                r34_c = nmap34[1][3]
                r34_d = nmap34[1][4]
                print "Merge 34"
        else:
            matched34 = matching(mat3, mat4, comp_var, user_match_perc)
            if matched34[0] == 1:
                three_four_done = 1
                mat3 = matched34[1][0]
                row_cp_local3 = matched34[1][2][0] + row_cp_local3
                col_cp_local3 = matched34[1][2][1] + col_cp_local3
                mat4 = matched34[1][1]
                row_cp_local4 = matched34[1][2][2] + row_cp_local4
                col_cp_local4 = matched34[1][2][3] + col_cp_local4
                r34_a = matched34[1][3]
                r34_b = matched34[1][4]
                r34_c = matched34[1][3]
                r34_d = matched34[1][4]
                print 'Mat3 and Mat4 have been merged at step = ', steps
                
        if three_five_done == 1:
            nmap35 = map_merge(r35_a, r35_b, r35_c, r35_d, mat3, mat5, 1)
            if nmap35[0] == 1:
                mat3 = nmap35[1][0]
                row_cp_local3 = nmap35[1][2][0] + row_cp_local3
                col_cp_local3 = nmap35[1][2][1] + col_cp_local3
                mat5 = nmap35[1][1]
                row_cp_local5 = nmap35[1][2][2] + row_cp_local5
                col_cp_local5 = nmap35[1][2][3] + col_cp_local5
                r35_a = nmap35[1][3]
                r35_b = nmap35[1][4]
                r35_c = nmap35[1][3]
                r35_d = nmap35[1][4]
                print "Merge 35"
        else:
            matched35 = matching(mat3, mat5, comp_var, user_match_perc)
            if matched35[0] == 1:
                three_five_done = 1
                mat3 = matched35[1][0]
                row_cp_local3 = matched35[1][2][0] + row_cp_local3
                col_cp_local3 = matched35[1][2][1] + col_cp_local3
                mat5 = matched35[1][1]
                row_cp_local5 = matched35[1][2][2] + row_cp_local5
                col_cp_local5 = matched35[1][2][3] + col_cp_local5
                r35_a = matched35[1][3]
                r35_b = matched35[1][4]
                r35_c = matched35[1][3]
                r35_d = matched35[1][4]
                print 'Mat3 and Mat5 have been merged at step = ', steps
            
        if four_five_done == 1:
            nmap45 = map_merge(r45_a, r45_b, r45_c, r45_d, mat4, mat5, 1)
            if nmap45[0] == 1:
                mat4 = nmap45[1][0]
                row_cp_local4 = nmap45[1][2][0] + row_cp_local4
                col_cp_local4 = nmap45[1][2][1] + col_cp_local4
                mat5 = nmap45[1][1]
                row_cp_local5 = nmap45[1][2][2] + row_cp_local5
                col_cp_local5 = nmap45[1][2][3] + col_cp_local5
                r45_a = nmap45[1][3]
                r45_b = nmap45[1][4]
                r45_c = nmap45[1][3]
                r45_d = nmap45[1][4]
                print "Merge 45"
        else:
            matched45 = matching(mat4, mat5, comp_var, user_match_perc)
            if matched45[0] == 1:
                four_five_done = 1
                mat4 = matched45[1][0]
                row_cp_local4 = matched45[1][2][0] + row_cp_local4
                col_cp_local4 = matched45[1][2][1] + col_cp_local4
                mat5 = matched45[1][1]
                row_cp_local5 = matched45[1][2][2] + row_cp_local5
                col_cp_local5 = matched45[1][2][3] + col_cp_local5
                r45_a = matched45[1][3]
                r45_b = matched45[1][4]
                r45_c = matched45[1][3]
                r45_d = matched45[1][4]
                print 'Mat4 and Mat5 have been merged at step = ', steps
## ===========================            
        if one_two_done == 1:
            nmap12 = map_merge(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
            if nmap12[0] == 1:
                mat1 = nmap12[1][0]
                row_cp_local1 = nmap12[1][2][0] + row_cp_local1
                col_cp_local1 = nmap12[1][2][1] + col_cp_local1
                mat2 = nmap12[1][1]
                row_cp_local2 = nmap12[1][2][2] + row_cp_local2
                col_cp_local2 = nmap12[1][2][3] + col_cp_local2
                r12_a = nmap12[1][3]
                r12_b = nmap12[1][4]
                r12_c = nmap12[1][3]
                r12_d = nmap12[1][4]
                print "Merge 12"     
        if one_three_done == 1:
            nmap13 = map_merge(r13_a, r13_b, r13_c, r13_d, mat1, mat3, 1)
            if nmap13[0] == 1:
                mat1 = nmap13[1][0]
                row_cp_local1 = nmap13[1][2][0] + row_cp_local1
                col_cp_local1 = nmap13[1][2][1] + col_cp_local1
                mat3 = nmap13[1][1]
                row_cp_local3 = nmap13[1][2][2] + row_cp_local3
                col_cp_local3 = nmap13[1][2][3] + col_cp_local3
                r13_a = nmap13[1][3]
                r13_b = nmap13[1][4]
                r13_c = nmap13[1][3]
                r13_d = nmap13[1][4]
                print "Merge 13"
        if one_four_done == 1:
            nmap14 = map_merge(r14_a, r14_b, r14_c, r14_d, mat1, mat4, 1)
            if nmap14[0] == 1:
                mat1 = nmap14[1][0]
                row_cp_local1 = nmap14[1][2][0] + row_cp_local1
                col_cp_local1 = nmap14[1][2][1] + col_cp_local1
                mat4 = nmap14[1][1]
                row_cp_local4 = nmap14[1][2][2] + row_cp_local4
                col_cp_local4 = nmap14[1][2][3] + col_cp_local4
                r14_a = nmap14[1][3]
                r14_b = nmap14[1][4]
                r14_c = nmap14[1][3]
                r14_d = nmap14[1][4]
                print "Merge 14"
        if one_five_done == 1:
            nmap15 = map_merge(r15_a, r15_b, r15_c, r15_d, mat1, mat5, 1)
            if nmap15[0] == 1:
                mat1 = nmap15[1][0]
                row_cp_local1 = nmap15[1][2][0] + row_cp_local1
                col_cp_local1 = nmap15[1][2][1] + col_cp_local1
                mat5 = nmap15[1][1]
                row_cp_local5 = nmap15[1][2][2] + row_cp_local5
                col_cp_local5 = nmap15[1][2][3] + col_cp_local5
                r15_a = nmap15[1][3]
                r15_b = nmap15[1][4]
                r15_c = nmap15[1][3]
                r15_d = nmap15[1][4]
                print "Merge 15"
        if two_three_done == 1:
            nmap23 = map_merge(r23_a, r23_b, r23_c, r23_d, mat2, mat3, 1)
            if nmap23[0] == 1:
                mat2 = nmap23[1][0]
                row_cp_local2 = nmap23[1][2][0] + row_cp_local2
                col_cp_local2 = nmap23[1][2][1] + col_cp_local2
                mat3 = nmap23[1][1]
                row_cp_local3 = nmap23[1][2][2] + row_cp_local3
                col_cp_local3 = nmap23[1][2][3] + col_cp_local3
                r23_a = nmap23[1][3]
                r23_b = nmap23[1][4]
                r23_c = nmap23[1][3]
                r23_d = nmap23[1][4]  
                print "Merge 23"
        if two_four_done == 1:
            nmap24 = map_merge(r24_a, r24_b, r24_c, r24_d, mat2, mat4, 1)
            if nmap24[0] == 1:
                mat2 = nmap24[1][0]
                row_cp_local2 = nmap24[1][2][0] + row_cp_local2
                col_cp_local2 = nmap24[1][2][1] + col_cp_local2
                mat4 = nmap24[1][1]
                row_cp_local4 = nmap24[1][2][2] + row_cp_local4
                col_cp_local4 = nmap24[1][2][3] + col_cp_local4
                r24_a = nmap24[1][3]
                r24_b = nmap24[1][4]
                r24_c = nmap24[1][3]
                r24_d = nmap24[1][4]
                print '"Merge 24"'
        if two_five_done == 1:
            nmap25 = map_merge(r25_a, r25_b, r25_c, r25_d, mat2, mat5, 1)
            if nmap25[0] == 1:
                mat2 = nmap25[1][0]
                row_cp_local2 = nmap25[1][2][0] + row_cp_local2
                col_cp_local2 = nmap25[1][2][1] + col_cp_local2
                mat5 = nmap25[1][1]
                row_cp_local5 = nmap25[1][2][2] + row_cp_local5
                col_cp_local5 = nmap25[1][2][3] + col_cp_local5
                r25_a = nmap25[1][3]
                r25_b = nmap25[1][4]
                r25_c = nmap25[1][3]
                r25_d = nmap25[1][4]
                print "Merge 25"
        if three_four_done == 1:
            nmap34 = map_merge(r34_a, r34_b, r34_c, r34_d, mat3, mat4, 1)
            if nmap34[0] == 1:
                mat3 = nmap34[1][0]
                row_cp_local3 = nmap34[1][2][0] + row_cp_local3
                col_cp_local3 = nmap34[1][2][1] + col_cp_local3
                mat4 = nmap34[1][1]
                row_cp_local4 = nmap34[1][2][2] + row_cp_local4
                col_cp_local4 = nmap34[1][2][3] + col_cp_local4
                r34_a = nmap34[1][3]
                r34_b = nmap34[1][4]
                r34_c = nmap34[1][3]
                r34_d = nmap34[1][4]
                print "Merge 34"
        if three_five_done == 1:
            nmap35 = map_merge(r35_a, r35_b, r35_c, r35_d, mat3, mat5, 1)
            if nmap35[0] == 1:
                mat3 = nmap35[1][0]
                row_cp_local3 = nmap35[1][2][0] + row_cp_local3
                col_cp_local3 = nmap35[1][2][1] + col_cp_local3
                mat5 = nmap35[1][1]
                row_cp_local5 = nmap35[1][2][2] + row_cp_local5
                col_cp_local5 = nmap35[1][2][3] + col_cp_local5
                r35_a = nmap35[1][3]
                r35_b = nmap35[1][4]
                r35_c = nmap35[1][3]
                r35_d = nmap35[1][4]
                print "Merge 35"
        if four_five_done == 1:
            nmap45 = map_merge(r45_a, r45_b, r45_c, r45_d, mat4, mat5, 1)
            if nmap45[0] == 1:
                mat4 = nmap45[1][0]
                row_cp_local4 = nmap45[1][2][0] + row_cp_local4
                col_cp_local4 = nmap45[1][2][1] + col_cp_local4
                mat5 = nmap45[1][1]
                row_cp_local5 = nmap45[1][2][2] + row_cp_local5
                col_cp_local5 = nmap45[1][2][3] + col_cp_local5
                r45_a = nmap45[1][3]
                r45_b = nmap45[1][4]
                r45_c = nmap45[1][3]
                r45_d = nmap45[1][4]
                print "Merge 45"
        
        level = get_level(mat1, row_cp_local1, col_cp_local1, mat2, row_cp_local2, col_cp_local2, mat3, row_cp_local3, col_cp_local3, mat4, row_cp_local4, col_cp_local4, mat5, row_cp_local5, col_cp_local5)
        print "Step No. = ", steps
        x=y=0
        for l in range(len(level)):
            if l == 0:
                z = 0
            elif l == 1:
                z = 200
            elif l == 2:
                z = 400
            elif l == 3:
                z = 600
            elif l == 4:
                z = 800
            for row in range(len(level[l])):
                for col in range(len(level[l][row])):
                    if level[l][row][col] == 'A' or level[l][row][col] == 'C':
                        pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                        pf.fill(Color("#000000"))
                        screen.blit(pf,(x+z+10,y+10))
                    elif level[l][row][col] == 'B':
                        pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                        pf.fill(Color("#ffff00"))       #Yellow
                        screen.blit(pf,(x+z+10,y+10))
                    elif level[l][row][col] == 'R1':
                        pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                        pf.fill(Color("#ff0000"))       #Red
                        screen.blit(pf,(x+z+10,y+10))
                    elif level[l][row][col] == 'R2':
                        pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                        pf.fill(Color("#00ff00"))       #Green
                        screen.blit(pf,(x+z+10,y+10))
                    elif level[l][row][col] == 'R3':
                        pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                        pf.fill(Color("#0000ff"))       #Blue
                        screen.blit(pf,(x+z+10,y+10))
                    elif level[l][row][col] == 'R4':
                        pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                        pf.fill(Color("#800080"))       #Purple
                        screen.blit(pf,(x+z+10,y+10))
                    elif level[l][row][col] == 'R5':
                        pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                        pf.fill(Color("#ffa500"))       #Orange
                        screen.blit(pf,(x+z+10,y+10))
                    else:
                        pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                        pf.fill(Color("#ffffff"))
                        screen.blit(pf,(x+z+10, y+10))
     
                    x += PLATFORM_WIDTH
                y += PLATFORM_HEIGHT
                x = 0
            y = 0 
        pygame.display.update()
        #time.sleep(0.1)
        
        no_of_B_left1 = 0
        no_of_B_left2 = 0
        no_of_B_left3 = 0
        no_of_B_left4 = 0
        no_of_B_left5 = 0
        
        cont1 = 0            # Checking if the map is finished.
        cont2 = 0            # Checking if the map is finished.
        cont3 = 0            # Checking if the map is finished.
        cont4 = 0            # Checking if the map is finished.
        cont5 = 0            # Checking if the map is finished.
        
#         if one_two_done == 1:
#             if mat1 != mat2:
#                 print "Something is very wrong. Stopping the program...12... new problem now"
#                 time.sleep(15)
#                 sys.exit()
#                 
#         if one_three_done == 1:
#             if mat1 != mat3:
#                 print "Something is very wrong. Stopping the program...13... new problem now"
#                 time.sleep(15)
#                 sys.exit()
#                 
#         if two_three_done == 1:
#             if mat2 != mat3:
#                 print "Something is very wrong. Stopping the program...23"
#                 time.sleep(15)
#                 sys.exit()
#         if one_four_done == 1:
#             if mat1 != mat4:
#                 print "Something is very wrong. Stopping the program...14"
#                 time.sleep(15)
#                 sys.exit()
#         if one_five_done == 1:
#             if mat1 != mat5:
#                 print "Something is very wrong. Stopping the program...15"
#                 time.sleep(25)
#                 sys.exit()
#         if two_four_done == 1:
#             if mat2 != mat4:
#                 print "Something is very wrong. Stopping the program...24"
#                 time.sleep(15)
#                 sys.exit()
#         if two_five_done == 1:
#             if mat2 != mat5:
#                 print "Something is very wrong. Stopping the program...25"
#                 time.sleep(15)
#                 sys.exit()
#         if three_four_done == 1:
#             if mat3 != mat4:
#                 print "Something is very wrong. Stopping the program...34"
#                 time.sleep(15)
#                 sys.exit()
#         if three_five_done == 1:
#             if mat3 != mat5:
#                 print "Something is very wrong. Stopping the program...35"
#                 time.sleep(25)
#                 sys.exit()
#         if four_five_done == 1:
#             if mat4 != mat5:
#                 print "Something is very wrong. Stopping the program...45"
#                 time.sleep(15)
#                 sys.exit()
        

        for r in range(len(mat1)):
            for c in range(len(mat1[0])):
                if mat1[r][c] == 'B':
                    no_of_B_left1 += 1
                    cont1 = 1
        for r in range(len(mat2)):
            for c in range(len(mat2[0])):
                if mat2[r][c] == 'B':
                    no_of_B_left2 += 1
                    cont2 = 1
        for r in range(len(mat3)):
            for c in range(len(mat3[0])):
                if mat3[r][c] == 'B':
                    no_of_B_left3 += 1
                    cont3 = 1
        for r in range(len(mat4)):
            for c in range(len(mat4[0])):
                if mat4[r][c] == 'B':
                    no_of_B_left4 += 1
                    cont4 = 1
        for r in range(len(mat5)):
            for c in range(len(mat5[0])):
                if mat5[r][c] == 'B':
                    no_of_B_left5 += 1
                    cont5 = 1
        #if (steps % roger == 0):
#             print row_cp_map1
#             print col_cp_map1
#             print row_cp_map2
#             print col_cp_map2
#             print row_cp_map3
#             print col_cp_map3
            #time.sleep(1)
            #raw_input("Press Enter to continue...")
        
        if (cont1 == 1) or (cont2 == 1) or (cont3 == 1) or (cont4 == 1) or (cont5 == 1):
            if (no_of_B_left1 == 0) or (no_of_B_left2 == 0) or (no_of_B_left3 == 0) or (no_of_B_left4 == 0) or (no_of_B_left5 == 0):
                done = 1
                print "Jhala 2"
            else:
                done = 0
        else: 
            done = 1
            print "Jhala 1"
            time.sleep(30)
    


if __name__ == "__main__":
    main()