'''
Created on Dec 16, 2016

@author: rjw0028
'''
# 0 = North, 1 = East, 2 = South, 3 = West



from Three_robot_functions import cp_field_value, first_map_update, matching, get_level
from Three_robot_functions import motion_deciding_function, var_update, adj_field_value
import pygame, sys
from pygame import *
from random import randint
import time


global real_map

# Variables from main algo...



map_choice = [0,0,0,0,0,0]

map_choice[2] = [[1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0],
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
map_choice[4] = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
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

map_choice[0] = [[0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
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

map_choice[5] = [[1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
                 [0,1,1,0,0,0,0,0,1,0,0,0,0,0,1,1],
                 [0,0,1,0,0,0,0,1,1,0,0,0,0,1,1,0],
                 [0,0,1,1,1,0,0,1,0,0,0,0,1,1,0,0],
                 [0,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0],
                 [0,1,1,1,1,1,0,1,0,0,1,1,0,0,0,0],
                 [1,1,0,0,0,1,0,1,0,1,1,0,0,0,0,0],
                 [0,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1],
                 [0,1,1,1,1,0,0,1,0,1,1,1,1,1,0,0],
                 [1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0],
                 [0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0],
                 [0,0,0,0,1,1,0,1,1,1,1,1,0,0,0,0],
                 [0,0,0,1,1,0,0,1,0,0,0,1,1,1,0,0],
                 [0,0,0,1,0,0,0,1,0,0,0,0,0,1,1,0],
                 [0,1,1,1,0,0,0,1,0,0,0,0,0,0,1,1],
                 [1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1]]


#Variables for the pygame display part...

WIN_WIDTH = 3*580
WIN_HEIGHT = 600
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#ffffff"
 
PLATFORM_WIDTH = 30
PLATFORM_HEIGHT = 30

#Running the one-time-running program...
def main():
    
    
    one_two_done = 0
    one_three_done = 0
    two_three_done = 0
    
    orient1 = 0      #always oriented towards the north at the beginning...
    orient2 = 0      #always oriented towards the north at the beginning...
    orient3 = 0      #always oriented towards the north at the beginning...

    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Robots map")
        
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
        else: 
            rcinput = False
    
    row_cp_local1 = 1    # These values will be 1 at the start
    col_cp_local1 = 1
    row_cp_local2 = 1    # These values will be 1 at the start
    col_cp_local2 = 1
    row_cp_local3 = 1    # These values will be 1 at the start
    col_cp_local3 = 1
    
    
    
    afv1 = adj_field_value(row_cp_map1, col_cp_map1, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position
    afv2 = adj_field_value(row_cp_map2, col_cp_map2, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position
    afv3 = adj_field_value(row_cp_map3, col_cp_map3, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position
    
    fv1 = cp_field_value(afv1)
    fv2 = cp_field_value(afv2)
    fv3 = cp_field_value(afv3)
    
    mat1 = first_map_update(fv1, afv1)
    mat2 = first_map_update(fv2, afv2)
    mat3 = first_map_update(fv3, afv3)
    steps = 0
    
    done = 0
    while done == 0:
        steps += 1
        for eve in pygame.event.get():    #To finish python process when you click the cross button...
            if eve.type == QUIT:
                raise SystemExit("QUIT")
        
        screen.blit(bg, (0,0))
        
        answer1 = motion_deciding_function(mat1, orient1, row_cp_local1, col_cp_local1, afv1)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
        answer2 = motion_deciding_function(mat2, orient2, row_cp_local2, col_cp_local2, afv2)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
        answer3 = motion_deciding_function(mat3, orient3, row_cp_local3, col_cp_local3, afv3)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
        #print "answer1 = ", answer1
        #print "answer2 = ", answer2
        #print "answer3 = ", answer3
        
        
        print steps
        
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
#         print afv1
#         print afv2
#         print afv3
        fv1 = cp_field_value(afv1)
        #print fv1
        fv2 = cp_field_value(afv2)
        #print fv2
        fv3 = cp_field_value(afv3)
        #print fv3
        
        # Updating variables for robot 1    
        var_list1 = var_update(mat1, row_next_pos1, col_next_pos1, row_cp_map1, col_cp_map1, row_cp_local1, col_cp_local1, orient1, fv1, afv1)
        var_list2 = var_update(mat2, row_next_pos2, col_next_pos2, row_cp_map2, col_cp_map2, row_cp_local2, col_cp_local2, orient2, fv2, afv2)
        var_list3 = var_update(mat3, row_next_pos3, col_next_pos3, row_cp_map3, col_cp_map3, row_cp_local3, col_cp_local3, orient3, fv3, afv3)
        
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
        
#         print 'Mat1 = ', mat1
#         print 'Mat2 = ', mat2
#         print 'Mat3 = ', mat3
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
        
        matched12 = matching(mat1, mat2, comp_var, user_match_perc)
        if matched12[0] == 1:
            one_two_done = 1
            mat1 = matched12[1][0]
            row_cp_local1 = matched12[1][2][0] + row_cp_local1
            col_cp_local1 = matched12[1][2][1] + col_cp_local1
            mat2 = matched12[1][1]
            row_cp_local2 = matched12[1][2][2] + row_cp_local2
            col_cp_local2 = matched12[1][2][3] + col_cp_local2
#             print '----------------------------------------------'
            print 'Mat1 and Mat2 have been merged at step = ', steps
#             print '----------------------------------------------'
#             print mat1
#             print mat2
            #raw_input("Press Enter to continue...")
        matched13 = matching(mat1, mat3, comp_var, user_match_perc)
        if matched13[0] == 1:
            one_three_done = 1
            mat1 = matched13[1][0]
            row_cp_local1 = matched13[1][2][0] + row_cp_local1
            col_cp_local1 = matched13[1][2][1] + col_cp_local1
            mat3 = matched13[1][1]
            row_cp_local3 = matched13[1][2][2] + row_cp_local3
            col_cp_local3 = matched13[1][2][3] + col_cp_local3
#             print '---------------------------------------------'
            print 'Mat1 and Mat3 have been merged at step = ', steps
#             print '---------------------------------------------'
#             print mat1
#             print mat3
            #raw_input("Press Enter to continue...")
        matched23 = matching(mat2, mat3, comp_var, user_match_perc)
        if matched23[0] == 1:
            two_three_done = 1
            mat2 = matched23[1][0]
            row_cp_local2 = matched23[1][2][0] + row_cp_local2
            col_cp_local2 = matched23[1][2][1] + col_cp_local2
            mat3 = matched23[1][1]
            row_cp_local3 = matched23[1][2][2] + row_cp_local3
            col_cp_local3 = matched23[1][2][3] + col_cp_local3
#             print '----------------------------------------------'
            print 'Mat2 and Mat3 have been merged at step = ', steps
#             print '----------------------------------------------'
#             print mat2
#             print mat3
            #raw_input("Press Enter to continue...")
        
        level = get_level(mat1, row_cp_local1, col_cp_local1, mat2, row_cp_local2, col_cp_local2, mat3, row_cp_local3, col_cp_local3)
        
        x=y=0
        for l in range(len(level)):
            if l == 0:
                z = 0
            elif l == 1:
                z = 580
            elif l == 2:
                z = 1160
            for row in range(len(level[l])):
                for col in range(len(level[l][row])):
                    if level[l][row][col] == 'A' or level[l][row][col] == 'C':
                        pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                        pf.fill(Color("#000000"))
                        screen.blit(pf,(x+z+20,y+20))
                    elif level[l][row][col] == 'B':
                        pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                        pf.fill(Color("#ffff00"))       #Yellow
                        screen.blit(pf,(x+z+20,y+20))
                    elif level[l][row][col] == 'R1':
                        pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                        pf.fill(Color("#ff0000"))       #Red
                        screen.blit(pf,(x+z+20,y+20))
                    elif level[l][row][col] == 'R2':
                        pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                        pf.fill(Color("#00ff00"))       #Green
                        screen.blit(pf,(x+z+20,y+20))
                    elif level[l][row][col] == 'R3':
                        pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                        pf.fill(Color("#0000ff"))       #Blue
                        screen.blit(pf,(x+z+20,y+20))
                    else:
                        pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                        pf.fill(Color("#ffffff"))
                        screen.blit(pf,(x+z+20, y+20))
     
                    x += PLATFORM_WIDTH
                y += PLATFORM_HEIGHT
                x = 0
            y = 0 
        pygame.display.update()
        time.sleep(0.3)
        
        no_of_B_left1 = 0
        no_of_B_left2 = 0
        no_of_B_left3 = 0
        cont1 = 0            # Checking if the map is finished.
        cont2 = 0            # Checking if the map is finished.
        cont3 = 0            # Checking if the map is finished.
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
        roger = 10
        
        if (steps == 29) or (steps == 28) or (steps == 70) or (steps == 71):
            time.sleep(5)
        #raw_input("Press Enter to continue...")
        
        if (cont1 == 1) or (cont2 == 1) or (cont3 == 1):
#             print "The map is still not finished. B's left = ", no_of_B_left1 + no_of_B_left2 + no_of_B_left3
            #raw_input("Press Enter to continue...")
            done = 0
        else: 
            done = 1
            time.sleep(30)
    


if __name__ == "__main__":
    main()