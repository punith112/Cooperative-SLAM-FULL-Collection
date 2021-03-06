'''
Created on Mar 18, 2017

@author: rjw0028
'''
from Three_robot_functions import cp_field_value, first_map_update, matching, get_level, all_good_values, make_agv
from Three_robot_functions import motion_deciding_function, var_update, adj_field_value, get_ref, khoka
from ExtraFunctions import var_update5, map_merge5, matching5, motion_deciding_function5,\
    sel_random

import pygame, sys, copy, random
from pygame import *
from random import randint
import time, xlwt


def robot1(agv, rm, mapno):
    robots = 1
    complete = 0
    iter = 0
    new_agv = copy.deepcopy(agv)
    real_map = copy.deepcopy(rm)

    while complete == 0:
        #print "AGV: ", agv
        
        print "/nIteration No: ", iter+1
        rnc = agv.pop(0)                 # Row and Column of the Random Entry while being popped out...
        #print "RNC: ", rnc
        
        orient = 0
        
        row_cp_map = copy.deepcopy(rnc[0])
        col_cp_map = copy.deepcopy(rnc[1])
        #print "Row_cp_map: ", row_cp_map
        #print "Col_cp_map: ", col_cp_map
        row_cp_local = 1    # These values will be 1 at the start
        col_cp_local = 1
        afv = adj_field_value(row_cp_map, col_cp_map, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position
        
        #print "AFV: ", afv
        fv = cp_field_value(afv)
        #print "FV: ", fv
        mat1 = first_map_update(fv, afv)
        #print "MAT1: ", mat1
        
        steps = 0
        
        done = 0
        while done == 0:
            answer = motion_deciding_function(mat1, orient, row_cp_local, col_cp_local, afv)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            
            #print "Answer = ", answer
            
            steps += 1 
            #print "answer = ", answer
            if answer == 0:
                row_next_pos = row_cp_local - 1
                col_next_pos = col_cp_local
                row_cp_map = row_cp_map - 1
            elif answer == 1:
                row_next_pos = row_cp_local
                col_next_pos = col_cp_local + 1
                col_cp_map = col_cp_map + 1
            elif answer == 2:
                row_next_pos = row_cp_local + 1
                col_next_pos = col_cp_local
                row_cp_map = row_cp_map + 1
            elif answer == 3:
                row_next_pos = row_cp_local
                col_next_pos = col_cp_local - 1
                col_cp_map = col_cp_map - 1
            #print mat1
            
            #print 'row_cp_local = ',row_cp_local
            #print 'col_cp_local = ', col_cp_local
            #print 'row_next_pos = ', row_next_pos
            #print 'col_next_pos = ', col_next_pos
            #print 'row_cp_map = ', row_cp_map
            #print 'col_cp_map = ', col_cp_map
            #raw_input("Press Enter to continue...")
                
            afv = adj_field_value(row_cp_map, col_cp_map, real_map)
            #print afv
            fv = cp_field_value(afv)
            #print fv
            #raw_input("Press Enter to continue...")
            
            # Updating variables for robot 1    
            var_list = var_update(mat1, row_next_pos, col_next_pos, row_cp_map, col_cp_map, row_cp_local, col_cp_local, orient, fv, afv)
            mat1 = var_list[0]
            row_next_pos = var_list[1]
            col_next_pos = var_list[2]
            row_cp_map = var_list[3]
            col_cp_map = var_list[4]
            row_cp_local = var_list[5]
            col_cp_local = var_list[6]
            orient = var_list[7]
            #print mat1
            #print 'row_cp_local = ',row_cp_local
            #print 'col_cp_local = ', col_cp_local
            #print 'row_next_pos = ', row_next_pos
            #print 'col_next_pos = ', col_next_pos
            #print 'row_cp_map = ', row_cp_map
            #print 'col_cp_map = ', col_cp_map
            #print 'orient = ',orient
            #raw_input("Press Enter to continue...")
            
            # You can add a display function here...
            
            #display_map(mat1)
            
            
            no_of_B_left = 0    # Checking if the map is finished.
            for r in range(len(mat1)):
                for c in range(len(mat1[0])):
                    if mat1[r][c] == 'B':
                        no_of_B_left = no_of_B_left + 1
            
            if no_of_B_left != 0:
                done = 0
                #print "The map is still not finished. B's left = ", no_of_B_left
                #raw_input("Press Enter to continue...")
                
            else:
    #             print "Steps: ", steps
    #             print "no_of_B_left: ", no_of_B_left
    #             raw_input("Press Enter to continue...")
                new_agv[iter][3] = steps
                #loggg = open("logg.txt", "a")
    #             print "Name of the file: ", loggg.name
    #             print "Closed or not : ", loggg.closed
    #             print "Opening mode : ", loggg.mode
                #st = str(steps)
                #rowncol = str(rnc)
                #loggg.write("\nStart Position and Distance: ")
                #loggg.write(rowncol)
                #loggg.write("\nNo. of Steps: ")
                #loggg.write(st)
                #loggg.close() 
                
                
                
                done = 1    
        iter = iter + 1
        if len(agv) == 0:
            wb = xlwt.Workbook()
            ws = wb.add_sheet('Data1Robot')
            col0_name = 'Start Row No.'
            col1_name = 'Start Col No.'
            col2_name = 'Distance'
            col3_name = 'Steps Reqd.'
            ws.write(0, 0, col0_name)
            ws.write(0, 1, col1_name)
            ws.write(0, 2, col2_name)
            ws.write(0, 3, col3_name)
            for p in range(len(new_agv)):
                ws.write(p+1, 0, new_agv[p][0])
                ws.write(p+1, 1, new_agv[p][1])
                ws.write(p+1, 2, new_agv[p][2])
                ws.write(p+1, 3, new_agv[p][3])  
            bookname = 'Map-' + str(mapno) + '--1Robot.xls'
            wb.save(bookname)
            complete = 100
        else:
            complete = 0
            
    print "And we should be done..."

def robot2(agv, list, rm, comp_var, user_match_perc, cyc, mapno):
    complete = 0
    robots = 2
    iter = 0
    real_map = copy.deepcopy(rm)
    new_agv = copy.deepcopy(agv)
    #the_agv = make_agv(agv) # Format of each row:    Perc%    Steps    R1    C1    R2    C2    R3    C3    R4    C4    R5    C5
    
    #ref = get_ref(list, 3)
    #kho = khoka(the_agv, list)
    
    lststep = [[0 for y in range(13)] for x in range(cyc)]
         
    for i in range(cyc):
#         v1 = ref[i][0] # = 1
#         v2 = ref[i][1] # = 2
#         v3 = ref[i][2] # = 5
        
        no_of_B_left1 = 0
        no_of_B_left2 = 0
        
        cont1 = 0            # Checking if the map is finished.
        cont2 = 0            # Checking if the map is finished.
        
        tagv = sel_random(new_agv, 2)
        print tagv
#         random.shuffle(kho[v1])
#         rnc1 = kho[v1][0]
#         random.shuffle(kho[v2])
#         rnc2 = kho[v2][0]
#         random.shuffle(kho[v3])
#         rnc3 = kho[v3][0]
        
        lststep[i][1] = copy.deepcopy(tagv[0][0])
        lststep[i][2] = copy.deepcopy(tagv[0][1])
        lststep[i][3] = copy.deepcopy(tagv[1][0])
        lststep[i][4] = copy.deepcopy(tagv[1][1])    
        lststep[i][11] = copy.deepcopy(comp_var)
        lststep[i][12] = copy.deepcopy(user_match_perc)

        print "/nIteration No: ", iter+1
        
        row_cp_map1 = copy.deepcopy(tagv[0][0])
        col_cp_map1 = copy.deepcopy(tagv[0][1])
        row_cp_map2 = copy.deepcopy(tagv[1][0])
        col_cp_map2 = copy.deepcopy(tagv[1][1])
        
        print row_cp_map1, ", ", col_cp_map1, ", ", row_cp_map2, ", ", col_cp_map2
       
        one_two_done = 0
        
        orient1 = 0      #always oriented towards the north at the beginning...
        orient2 = 0      #always oriented towards the north at the beginning...
                
        r12_a = 0
        r12_b = 0
        r12_c = 0
        r12_d = 0
        
        
        row_cp_local1 = 1    # These values will be 1 at the start
        col_cp_local1 = 1
        row_cp_local2 = 1    # These values will be 1 at the start
        col_cp_local2 = 1
        
        afv1 = adj_field_value(row_cp_map1, col_cp_map1, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position
        afv2 = adj_field_value(row_cp_map2, col_cp_map2, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position
        
        fv1 = cp_field_value(afv1)
        fv2 = cp_field_value(afv2)
        
        mat1 = first_map_update(fv1, afv1)
        mat2 = first_map_update(fv2, afv2)
        
        steps = 0
        
        done = 0
        
        while done == 0:
            if one_two_done == 1:
                nmap12 = map_merge5(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
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
                    #print "Merge 12"     
            
            answer1 = motion_deciding_function5(mat1, orient1, row_cp_local1, col_cp_local1, afv1)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            answer2 = motion_deciding_function5(mat2, orient2, row_cp_local2, col_cp_local2, afv2)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            
            steps += 1
        
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
                
            afv1 = adj_field_value(row_cp_map1, col_cp_map1, real_map)
            afv2 = adj_field_value(row_cp_map2, col_cp_map2, real_map)
    #         print afv1
    #         print afv2
    #         print afv3
            fv1 = cp_field_value(afv1)
            #print fv1
            fv2 = cp_field_value(afv2)
            #print fv2
            
            # Updating variables for robot 1    
            var_list1 = var_update5(mat1, row_next_pos1, col_next_pos1, row_cp_map1, col_cp_map1, row_cp_local1, col_cp_local1, orient1, fv1, afv1)
            var_list2 = var_update5(mat2, row_next_pos2, col_next_pos2, row_cp_map2, col_cp_map2, row_cp_local2, col_cp_local2, orient2, fv2, afv2)
            
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
            
            
            if var_list1[8] == 'N':
                r12_a = r12_a + 1
            elif var_list1[8] == 'W':
                r12_b = r12_b + 1
            if var_list2[8] == 'N':
                r12_c = r12_c + 1
            elif var_list2[8] == 'W':
                r12_d = r12_d + 1
            
            if one_two_done == 1:
                nmap12 = map_merge5(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
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
                    #print "Merge 12" 
            else:
                matched12 = matching5(mat1, mat2, comp_var, user_match_perc)
                if matched12[0] == 1:
                    one_two_done = 1
                    mat1 = matched12[1][0]
                    row_cp_local1 = matched12[1][2][0] + row_cp_local1
                    col_cp_local1 = matched12[1][2][1] + col_cp_local1
                    mat2 = matched12[1][1]
                    row_cp_local2 = matched12[1][2][2] + row_cp_local2
                    col_cp_local2 = matched12[1][2][3] + col_cp_local2
    #                 print '----------------------------------------------'
    #                 print 'Mat1 and Mat2 have been merged at step = ', steps
    #                 print '----------------------------------------------'
                    #print mat1
                    #print mat2
                    #raw_input("Press Enter to continue...")
#             if (one_two_done == 1) and (mat1 != mat2):
#                 lststep[i][0] = 0
#                 break
            
            if one_two_done == 1:
                nmap12 = map_merge5(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
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
                    #print "Merge 12"     
                            
            no_of_B_left1 = 0
            no_of_B_left2 = 0
            
            cont1 = 0            # Checking if the map is finished.
            cont2 = 0            # Checking if the map is finished.
            
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
            
            
            if (cont1 == 1) or (cont2 == 1) :
                if (no_of_B_left1 == 0) or (no_of_B_left2 == 0) :
                    done = 1
                    print "Jhala 22"
                    lststep[i][0] = steps
                else:
                    done = 0
                
            else:
                lststep[i][0] = steps
                done = 1
        iter = iter + 1
    wb = xlwt.Workbook()
    sheetname = 'Sheet--' + str(comp_var) + '--' + str(int((user_match_perc)))
    ws = wb.add_sheet(sheetname)         #Sheet
    col0_name = 'No. of Steps.'
    col1_name = 'Row 1'
    col2_name = 'Col 1'
    col3_name = 'Row 2'
    col4_name = 'Col 2'
    
    ws.write(0, 1, "Comparison Window Size: ")
    ws.write(0, 5, "Acceptable Match Perc: ")
    ws.write(0, 4, str(comp_var))
    ws.write(0, 7, str(user_match_perc))
    
    ws.write(1, 0, col0_name)
    ws.write(1, 1, col1_name)
    ws.write(1, 2, col2_name)
    ws.write(1, 3, col3_name)    
    ws.write(1, 4, col4_name)
    for p in range(len(lststep)):
        ws.write(p+2, 0, lststep[p][0])
        ws.write(p+2, 1, lststep[p][1])
        ws.write(p+2, 2, lststep[p][2])
        ws.write(p+2, 3, lststep[p][3]) 
        ws.write(p+2, 4, lststep[p][4])              
    bookname = 'Map-' + str(mapno) + 'Robots2--WS-' + str(comp_var) + '--AP-' + str(int((user_match_perc))) + '.xls'
    wb.save(bookname)

def robot3(agv, list, rm, comp_var, user_match_perc, cyc, mapno):
    complete = 0
    iter = 0
    real_map = copy.deepcopy(rm)
    new_agv = copy.deepcopy(agv)
    #the_agv = make_agv(agv) # Format of each row:    Perc%    Steps    R1    C1    R2    C2    R3    C3    R4    C4    R5    C5
    
    #ref = get_ref(list, 3)
    #kho = khoka(the_agv, list)
    
    lststep = [[0 for y in range(13)] for x in range(cyc)]
         
    for i in range(cyc):
#         v1 = ref[i][0] # = 1
#         v2 = ref[i][1] # = 2
#         v3 = ref[i][2] # = 5
        
        no_of_B_left1 = 0
        no_of_B_left2 = 0
        no_of_B_left3 = 0
        
        cont1 = 0            # Checking if the map is finished.
        cont2 = 0            # Checking if the map is finished.
        cont3 = 0            # Checking if the map is finished.
        
        tagv = sel_random(new_agv, 3)
        print tagv
#         random.shuffle(kho[v1])
#         rnc1 = kho[v1][0]
#         random.shuffle(kho[v2])
#         rnc2 = kho[v2][0]
#         random.shuffle(kho[v3])
#         rnc3 = kho[v3][0]
        
        lststep[i][1] = copy.deepcopy(tagv[0][0])
        lststep[i][2] = copy.deepcopy(tagv[0][1])
        lststep[i][3] = copy.deepcopy(tagv[1][0])
        lststep[i][4] = copy.deepcopy(tagv[1][1])
        lststep[i][5] = copy.deepcopy(tagv[2][0])
        lststep[i][6] = copy.deepcopy(tagv[2][1])    
        lststep[i][11] = copy.deepcopy(comp_var)
        lststep[i][12] = copy.deepcopy(user_match_perc)

        print "/nIteration No: ", iter+1
        
        row_cp_map1 = copy.deepcopy(tagv[0][0])
        col_cp_map1 = copy.deepcopy(tagv[0][1])
        row_cp_map2 = copy.deepcopy(tagv[1][0])
        col_cp_map2 = copy.deepcopy(tagv[1][1])
        row_cp_map3 = copy.deepcopy(tagv[2][0])
        col_cp_map3 = copy.deepcopy(tagv[2][1])
        
        print row_cp_map1, ", ", col_cp_map1, ", ", row_cp_map2, ", ", col_cp_map2
       
        one_two_done = 0
        one_three_done = 0
        two_three_done = 0
        
        orient1 = 0      #always oriented towards the north at the beginning...
        orient2 = 0      #always oriented towards the north at the beginning...
        orient3 = 0      #always oriented towards the north at the beginning...
        
        r12_a = 0
        r12_b = 0
        r12_c = 0
        r12_d = 0
        
        r13_a = 0
        r13_b = 0
        r13_c = 0
        r13_d = 0
        
        r23_a = 0
        r23_b = 0
        r23_c = 0
        r23_d = 0
        
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
            if one_two_done == 1:
                nmap12 = map_merge5(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
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
                    #print "Merge 12"     
            if one_three_done == 1:
                nmap13 = map_merge5(r13_a, r13_b, r13_c, r13_d, mat1, mat3, 1)
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
                    #print "Merge 13"
            if two_three_done == 1:
                nmap23 = map_merge5(r23_a, r23_b, r23_c, r23_d, mat2, mat3, 1)
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
                    #print "Merge 23"
            
            
            answer1 = motion_deciding_function5(mat1, orient1, row_cp_local1, col_cp_local1, afv1)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            answer2 = motion_deciding_function5(mat2, orient2, row_cp_local2, col_cp_local2, afv2)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            answer3 = motion_deciding_function5(mat3, orient3, row_cp_local3, col_cp_local3, afv3)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            
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
            var_list1 = var_update5(mat1, row_next_pos1, col_next_pos1, row_cp_map1, col_cp_map1, row_cp_local1, col_cp_local1, orient1, fv1, afv1)
            var_list2 = var_update5(mat2, row_next_pos2, col_next_pos2, row_cp_map2, col_cp_map2, row_cp_local2, col_cp_local2, orient2, fv2, afv2)
            var_list3 = var_update5(mat3, row_next_pos3, col_next_pos3, row_cp_map3, col_cp_map3, row_cp_local3, col_cp_local3, orient3, fv3, afv3)
            
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
            
            if var_list1[8] == 'N':
                r12_a = r12_a + 1
                r13_a = r13_a + 1
            elif var_list1[8] == 'W':
                r12_b = r12_b + 1
                r13_b = r13_b + 1
            if var_list2[8] == 'N':
                r23_a = r23_a + 1
                r12_c = r12_c + 1
            elif var_list2[8] == 'W':
                r23_b = r23_b + 1
                r12_d = r12_d + 1
            if var_list3[8] == 'N':
                r13_c = r13_c + 1
                r23_c = r23_c + 1
            elif var_list3[8] == 'W':
                r13_d = r13_d + 1
                r23_d = r23_d + 1
            if one_two_done == 1:
                nmap12 = map_merge5(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
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
                    #print "Merge 12" 
            else:
                matched12 = matching5(mat1, mat2, comp_var, user_match_perc)
                if matched12[0] == 1:
                    one_two_done = 1
                    mat1 = matched12[1][0]
                    row_cp_local1 = matched12[1][2][0] + row_cp_local1
                    col_cp_local1 = matched12[1][2][1] + col_cp_local1
                    mat2 = matched12[1][1]
                    row_cp_local2 = matched12[1][2][2] + row_cp_local2
                    col_cp_local2 = matched12[1][2][3] + col_cp_local2
    #                 print '----------------------------------------------'
    #                 print 'Mat1 and Mat2 have been merged at step = ', steps
    #                 print '----------------------------------------------'
                    #print mat1
                    #print mat2
                    #raw_input("Press Enter to continue...")
#             if (one_two_done == 1) and (mat1 != mat2):
#                 lststep[i][0] = 0
#                 break
            if one_three_done == 1:
                nmap13 = map_merge5(r13_a, r13_b, r13_c, r13_d, mat1, mat3, 1)
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
                    #print "Merge 13"
            else:
                matched13 = matching5(mat1, mat3, comp_var, user_match_perc)
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
                    #print 'Mat1 and Mat3 have been merged at step = ', steps
#             if (one_three_done == 1) and (mat1 != mat3):
#                 lststep[i][0] = 0
#                 break
            if two_three_done == 1:
                nmap23 = map_merge5(r23_a, r23_b, r23_c, r23_d, mat2, mat3, 1)
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
                    #print "Merge 23"
            else:      
                matched23 = matching5(mat2, mat3, comp_var, user_match_perc)
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
                    #print 'Mat2 and Mat3 have been merged at step = ', steps
#             if (two_three_done == 1) and (mat2 != mat3):
#                 lststep[i][0] = 0
#                 break
            
            if one_two_done == 1:
                nmap12 = map_merge5(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
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
                    #print "Merge 12"     
            if one_three_done == 1:
                nmap13 = map_merge5(r13_a, r13_b, r13_c, r13_d, mat1, mat3, 1)
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
                    #print "Merge 13"
            if two_three_done == 1:
                nmap23 = map_merge5(r23_a, r23_b, r23_c, r23_d, mat2, mat3, 1)
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
                    #print "Merge 23"
                            
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
                        
#             roger = 10
#             if (steps % roger == 0):
    #             print row_cp_map1
    #             print col_cp_map1
    #             print row_cp_map2
    #             print col_cp_map2
    #             print row_cp_map3
    #             print col_cp_map3
                #time.sleep(0.1)
                #raw_input("Press Enter to continue...")
            
            if (cont1 == 1) or (cont2 == 1) or (cont3 == 1):
                if (no_of_B_left1 == 0) or (no_of_B_left2 == 0) or (no_of_B_left3 == 0):
                    done = 1
                    lststep[i][0] = steps
                    print "Jhala 3"
                else:
                    done = 0
                
            else:
                lststep[i][0] = steps
                done = 1
        iter = iter + 1
    wb = xlwt.Workbook()
    sheetname = 'Sheet--' + str(comp_var) + '--' + str(int((user_match_perc)))
    ws = wb.add_sheet(sheetname)         #Sheet
    col0_name = 'No. of Steps.'
    col1_name = 'Row 1'
    col2_name = 'Col 1'
    col3_name = 'Row 2'
    col4_name = 'Col 2'
    col5_name = 'Row 3'
    col6_name = 'Col 3'
    
    ws.write(0, 1, "Comparison Window Size: ")
    ws.write(0, 5, "Acceptable Match Perc: ")
    ws.write(0, 4, str(comp_var))
    ws.write(0, 7, str(user_match_perc))
    
    ws.write(1, 0, col0_name)
    ws.write(1, 1, col1_name)
    ws.write(1, 2, col2_name)
    ws.write(1, 3, col3_name)    
    ws.write(1, 4, col4_name)
    ws.write(1, 5, col5_name)
    ws.write(1, 6, col6_name)
    for p in range(len(lststep)):
        ws.write(p+2, 0, lststep[p][0])
        ws.write(p+2, 1, lststep[p][1])
        ws.write(p+2, 2, lststep[p][2])
        ws.write(p+2, 3, lststep[p][3]) 
        ws.write(p+2, 4, lststep[p][4])
        ws.write(p+2, 5, lststep[p][5])  
        ws.write(p+2, 6, lststep[p][6])              
    bookname = 'Map-' + str(mapno) + '--Robots3--WS-' + str(comp_var) + '--AP-' + str(int((user_match_perc))) + '.xls'
    wb.save(bookname)

def robot4(agv, list, rm, comp_var, user_match_perc, cyc, mapno):
    iter = 0
    real_map = copy.deepcopy(rm)
    new_agv = copy.deepcopy(agv)
    #the_agv = make_agv(agv) # Format of each row:    Perc%    Steps    R1    C1    R2    C2    R3    C3    R4    C4    R5    C5
    #ref = get_ref(list, 5)
    #kho = khoka(the_agv, list)
    #print kho
    
    lststep = [[0 for y in range(13)] for x in range(cyc)]
    
    for i in range(cyc):            
#         v1 = ref[i][0] # = 1
#         v2 = ref[i][1] # = 2
#         v3 = ref[i][2] # = 5
#         v4 = ref[i][3]
#         v5 = ref[i][4]
#         
        no_of_B_left1 = 0
        no_of_B_left2 = 0
        no_of_B_left3 = 0
        no_of_B_left4 = 0
            
        cont1 = 0            # Checking if the map is finished.
        cont2 = 0            # Checking if the map is finished.
        cont3 = 0            # Checking if the map is finished.
        cont4 = 0            # Checking if the map is finished.
        
        tagv = sel_random(new_agv, 4)
        print tagv
#         random.shuffle(kho[v1])
#         rnc1 = tagv[0][]
#         random.shuffle(kho[v2])
#         rnc2 = kho[v2][0]
#         random.shuffle(kho[v3])
#         rnc3 = kho[v3][0]
#         random.shuffle(kho[v4])
#         rnc4 = kho[v4][0]
#         random.shuffle(kho[v5])
#         rnc5 = kho[v5][0]
#         print rnc1, rnc2, rnc3, rnc4, rnc5
        
        lststep[i][1] = copy.deepcopy(tagv[0][0])
        lststep[i][2] = copy.deepcopy(tagv[0][1])
        lststep[i][3] = copy.deepcopy(tagv[1][0])
        lststep[i][4] = copy.deepcopy(tagv[1][1])
        lststep[i][5] = copy.deepcopy(tagv[2][0])
        lststep[i][6] = copy.deepcopy(tagv[2][1])
        lststep[i][7] = copy.deepcopy(tagv[3][0])
        lststep[i][8] = copy.deepcopy(tagv[3][1])       
        lststep[i][11] = copy.deepcopy(comp_var)
        lststep[i][12] = copy.deepcopy(user_match_perc)
        
        print "/nIteration No: ", iter+1
        
        row_cp_map1 = copy.deepcopy(tagv[0][0])
        col_cp_map1 = copy.deepcopy(tagv[0][1])
        row_cp_map2 = copy.deepcopy(tagv[1][0])
        col_cp_map2 = copy.deepcopy(tagv[1][1])
        row_cp_map3 = copy.deepcopy(tagv[2][0])
        col_cp_map3 = copy.deepcopy(tagv[2][1])
        row_cp_map4 = copy.deepcopy(tagv[3][0])
        col_cp_map4 = copy.deepcopy(tagv[3][1])
        
        print row_cp_map1, ", ", col_cp_map1, ", ", row_cp_map2, ", ", col_cp_map2
        
        one_two_done = 0
        one_three_done = 0
        one_four_done = 0
        two_three_done = 0
        two_four_done = 0
        three_four_done = 0
        
        orient1 = 0      #always oriented towards the north at the beginning...
        orient2 = 0      #always oriented towards the north at the beginning...
        orient3 = 0      #always oriented towards the north at the beginning...
        orient4 = 0
        
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
        
        r23_a = 0
        r23_b = 0
        r23_c = 0
        r23_d = 0
        
        r24_a = 0
        r24_b = 0
        r24_c = 0
        r24_d = 0
        
        r34_a = 0
        r34_b = 0
        r34_c = 0
        r34_d = 0
                
        row_cp_local1 = 1    # These values will be 1 at the start
        col_cp_local1 = 1
        row_cp_local2 = 1    # These values will be 1 at the start
        col_cp_local2 = 1
        row_cp_local3 = 1    # These values will be 1 at the start
        col_cp_local3 = 1
        row_cp_local4 = 1    # These values will be 1 at the start
        col_cp_local4 = 1
        
        
        afv1 = adj_field_value(row_cp_map1, col_cp_map1, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position
        afv2 = adj_field_value(row_cp_map2, col_cp_map2, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position
        afv3 = adj_field_value(row_cp_map3, col_cp_map3, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position
        afv4 = adj_field_value(row_cp_map4, col_cp_map4, real_map)# This is the array returned when we enquire about the 4-neighbors of the current position
        
        fv1 = cp_field_value(afv1)
        fv2 = cp_field_value(afv2)
        fv3 = cp_field_value(afv3)
        fv4 = cp_field_value(afv4)
        
        mat1 = first_map_update(fv1, afv1)
        mat2 = first_map_update(fv2, afv2)
        mat3 = first_map_update(fv3, afv3)
        mat4 = first_map_update(fv4, afv4)
        
        steps = 0
    
        done = 0
        
        
        while done == 0:  
            if one_two_done == 1:
                nmap12 = map_merge5(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
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
                    #print "Merge 12"     
            if one_three_done == 1:
                nmap13 = map_merge5(r13_a, r13_b, r13_c, r13_d, mat1, mat3, 1)
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
                    #print "Merge 13"
            if one_four_done == 1:
                nmap14 = map_merge5(r14_a, r14_b, r14_c, r14_d, mat1, mat4, 1)
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
                    #print "Merge 14"
            if two_three_done == 1:
                nmap23 = map_merge5(r23_a, r23_b, r23_c, r23_d, mat2, mat3, 1)
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
                    #print "Merge 23"
            if two_four_done == 1:
                nmap24 = map_merge5(r24_a, r24_b, r24_c, r24_d, mat2, mat4, 1)
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
                    #print '"Merge 24"'
            
            if three_four_done == 1:
                nmap34 = map_merge5(r34_a, r34_b, r34_c, r34_d, mat3, mat4, 1)
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
                    #print "Merge 34"
                  
            
            answer1 = motion_deciding_function5(mat1, orient1, row_cp_local1, col_cp_local1, afv1)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            answer2 = motion_deciding_function5(mat2, orient2, row_cp_local2, col_cp_local2, afv2)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            answer3 = motion_deciding_function5(mat3, orient3, row_cp_local3, col_cp_local3, afv3)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            answer4 = motion_deciding_function5(mat4, orient4, row_cp_local4, col_cp_local4, afv4)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            
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
            
            
            afv1 = adj_field_value(row_cp_map1, col_cp_map1, real_map)
            afv2 = adj_field_value(row_cp_map2, col_cp_map2, real_map)
            afv3 = adj_field_value(row_cp_map3, col_cp_map3, real_map)
            afv4 = adj_field_value(row_cp_map4, col_cp_map4, real_map)
            
            fv1 = cp_field_value(afv1)
            #print fv1
            fv2 = cp_field_value(afv2)
            #print fv2
            fv3 = cp_field_value(afv3)
            #print fv3
            fv4 = cp_field_value(afv4)
            #print fv4
            
            # Updating variables for robot 1    
            var_list1 = var_update5(mat1, row_next_pos1, col_next_pos1, row_cp_map1, col_cp_map1, row_cp_local1, col_cp_local1, orient1, fv1, afv1)
            var_list2 = var_update5(mat2, row_next_pos2, col_next_pos2, row_cp_map2, col_cp_map2, row_cp_local2, col_cp_local2, orient2, fv2, afv2)
            var_list3 = var_update5(mat3, row_next_pos3, col_next_pos3, row_cp_map3, col_cp_map3, row_cp_local3, col_cp_local3, orient3, fv3, afv3)
            var_list4 = var_update5(mat4, row_next_pos4, col_next_pos4, row_cp_map4, col_cp_map4, row_cp_local4, col_cp_local4, orient4, fv4, afv4)
            
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
                    
            if var_list1[8] == 'N':
                r12_a = r12_a + 1
                r13_a = r13_a + 1
                r14_a = r14_a + 1
                
            elif var_list1[8] == 'W':
                r12_b = r12_b + 1
                r13_b = r13_b + 1
                r14_b = r14_b + 1
                
            if var_list2[8] == 'N':
                r23_a = r23_a + 1
                r24_a = r24_a + 1
                r12_c = r12_c + 1
            elif var_list2[8] == 'W':
                r23_b = r23_b + 1
                r24_b = r24_b + 1
                r12_d = r12_d + 1
            if var_list3[8] == 'N':
                r34_a = r34_a + 1
                r13_c = r13_c + 1
                r23_c = r23_c + 1
            elif var_list3[8] == 'W':
                r34_b = r34_b + 1
                r13_d = r13_d + 1
                r23_d = r23_d + 1
            if var_list4[8] == 'N':
                r14_c = r14_c + 1
                r24_c = r24_c + 1
                r34_c = r34_c + 1
            if var_list4[8] == 'W':
                r14_d = r14_d + 1
                r24_d = r24_d + 1
                r34_d = r34_d + 1
            
            if one_two_done == 1:
                nmap12 = map_merge5(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
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
                    #print "Merge 12"                     
            else:
                matched12 = matching5(mat1, mat2, comp_var, user_match_perc)
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
                    
                    #print 'Mat1 and Mat2 have been merged at step = ', steps
#             if (one_two_done == 1) and (mat1 != mat2):
#                 lststep[i][0] = 0
#                 break
#                 
                    
            if one_three_done == 1:
                nmap13 = map_merge5(r13_a, r13_b, r13_c, r13_d, mat1, mat3, 1)
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
                    #print "Merge 13"
            else:
                matched13 = matching5(mat1, mat3, comp_var, user_match_perc)
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
                    #print 'Mat1 and Mat3 have been merged at step = ', steps
#             if (one_three_done == 1) and (mat1 != mat3):
#                 lststep[i][0] = 0
#                 break
            
            if one_four_done == 1:
                nmap14 = map_merge5(r14_a, r14_b, r14_c, r14_d, mat1, mat4, 1)
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
                    #print "Merge 14"   
            else:
                matched14 = matching5(mat1, mat4, comp_var, user_match_perc)
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
                    #print 'Mat1 and Mat4 have been merged at step = ', steps
#             if (one_four_done == 1) and (mat1 != mat4):
#                 lststep[i][0] = 0
#                 break
#                     
            
                
            
            if two_three_done == 1:
                nmap23 = map_merge5(r23_a, r23_b, r23_c, r23_d, mat2, mat3, 1)
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
                    #print "Merge 23"
            else:      
                matched23 = matching5(mat2, mat3, comp_var, user_match_perc)
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
                    #print 'Mat2 and Mat3 have been merged at step = ', steps
#             if (two_three_done == 1) and (mat2 != mat3):
#                 lststep[i][0] = 0
#                 break
                    
            if two_four_done == 1:
                nmap24 = map_merge5(r24_a, r24_b, r24_c, r24_d, mat2, mat4, 1)
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
                    #print '"Merge 24"'
            else:
                matched24 = matching5(mat2, mat4, comp_var, user_match_perc)
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
                    #print 'Mat2 and Mat4 have been merged at step = ', steps
#             if (two_four_done == 1) and (mat2 != mat4):
#                 lststep[i][0] = 0
#                 break
                
                
            if three_four_done == 1:
                nmap34 = map_merge5(r34_a, r34_b, r34_c, r34_d, mat3, mat4, 1)
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
                    #print "Merge 34"
            else:
                matched34 = matching5(mat3, mat4, comp_var, user_match_perc)
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
                    #print 'Mat3 and Mat4 have been merged at step = ', steps
#             if (three_four_done == 1) and (mat3 != mat4):
#                 lststep[i][0] = 0
#                 break
            
            if one_two_done == 1:
                nmap12 = map_merge5(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
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
                    #print "Merge 12"     
            if one_three_done == 1:
                nmap13 = map_merge5(r13_a, r13_b, r13_c, r13_d, mat1, mat3, 1)
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
                    #print "Merge 13"
            if one_four_done == 1:
                nmap14 = map_merge5(r14_a, r14_b, r14_c, r14_d, mat1, mat4, 1)
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
                    #print "Merge 14"
            
            if two_three_done == 1:
                nmap23 = map_merge5(r23_a, r23_b, r23_c, r23_d, mat2, mat3, 1)
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
                    #print "Merge 23"
            if two_four_done == 1:
                nmap24 = map_merge5(r24_a, r24_b, r24_c, r24_d, mat2, mat4, 1)
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
                    #print '"Merge 24"'
            
            if three_four_done == 1:
                nmap34 = map_merge5(r34_a, r34_b, r34_c, r34_d, mat3, mat4, 1)
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
                    #print "Merge 34"
            
            
            no_of_B_left1 = 0
            no_of_B_left2 = 0
            no_of_B_left3 = 0
            no_of_B_left4 = 0
            
            cont1 = 0            # Checking if the map is finished.
            cont2 = 0            # Checking if the map is finished.
            cont3 = 0            # Checking if the map is finished.
            cont4 = 0            # Checking if the map is finished.
            
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
            
            if ((len(mat1) > 18) or ((len(mat1[0]) > 18))) or ((len(mat2) > 18) or ((len(mat2[0]) > 18))) or ((len(mat3) > 18) or ((len(mat3[0]) > 18))) or ((len(mat4) > 18) or ((len(mat4[0]) > 18))):
                lststep[i][0] = 0
                break
            
            
            if (cont1 == 1) or (cont2 == 1) or (cont3 == 1) or (cont4 == 1) :
                if (no_of_B_left1 == 0) or (no_of_B_left2 == 0) or (no_of_B_left3 == 0) or (no_of_B_left4 == 0) :
                    done = 1
                    print "Jhala 2"
                    lststep[i][0] = steps
                else:
                    done = 0
                #print "The map is still not finished. B's left = ", no_of_B_left1 + no_of_B_left2 + no_of_B_left3 + no_of_B_left4 + no_of_B_left5
                #raw_input("Press Enter to continue...")
            else: 
                lststep[i][0] = steps
                done = 1
        #time.sleep(0.5)
        iter = iter + 1
    wb = xlwt.Workbook()
    sheetname = 'Sheet--' + str(comp_var) + '--' + str(int((user_match_perc)))
    ws = wb.add_sheet(sheetname)         #Sheet
    col0_name = 'No. of Steps.'
    col1_name = 'Row 1'
    col2_name = 'Col 1'
    col3_name = 'Row 2'
    col4_name = 'Col 2'
    col5_name = 'Row 3'
    col6_name = 'Col 3'
    col7_name = 'Row 4'
    col8_name = 'Col 4'
    
    ws.write(0, 1, "Comparison Window Size: ")
    ws.write(0, 4, "Acceptable Match Perc: ")
    ws.write(0, 3, str(comp_var))
    ws.write(0, 6, str(user_match_perc))
    
    ws.write(1, 0, col0_name)
    ws.write(1, 1, col1_name)
    ws.write(1, 2, col2_name)
    ws.write(1, 3, col3_name)    
    ws.write(1, 4, col4_name)
    ws.write(1, 5, col5_name)
    ws.write(1, 6, col6_name)
    ws.write(1, 7, col7_name)
    ws.write(1, 8, col8_name)
    for p in range(len(lststep)):
        ws.write(p+2, 0, lststep[p][0])
        ws.write(p+2, 1, lststep[p][1])
        ws.write(p+2, 2, lststep[p][2])
        ws.write(p+2, 3, lststep[p][3]) 
        ws.write(p+2, 4, lststep[p][4])
        ws.write(p+2, 5, lststep[p][5])  
        ws.write(p+2, 6, lststep[p][6])   
        ws.write(p+2, 7, lststep[p][7]) 
        ws.write(p+2, 8, lststep[p][8])
    bookname = 'Map-' + str(mapno) + '--Robots4--WS-' + str(comp_var) + '--AP-' + str(int((user_match_perc))) + '.xls'
    wb.save(bookname)
      
def robot5(agv, list, rm, comp_var, user_match_perc, cyc, mapno):
    iter = 0
    real_map = copy.deepcopy(rm)
    new_agv = copy.deepcopy(agv)
    #the_agv = make_agv(agv) # Format of each row:    Perc%    Steps    R1    C1    R2    C2    R3    C3    R4    C4    R5    C5
    #ref = get_ref(list, 5)
    #kho = khoka(the_agv, list)
    #print kho
    
    lststep = [[0 for y in range(13)] for x in range(cyc)]
    
    for i in range(cyc):            
#         v1 = ref[i][0] # = 1
#         v2 = ref[i][1] # = 2
#         v3 = ref[i][2] # = 5
#         v4 = ref[i][3]
#         v5 = ref[i][4]
#         
        no_of_B_left1 = 0
        no_of_B_left2 = 0
        no_of_B_left3 = 0
        no_of_B_left4 = 0
        no_of_B_left5 = 0
            
        cont1 = 0            # Checking if the map is finished.
        cont2 = 0            # Checking if the map is finished.
        cont3 = 0            # Checking if the map is finished.
        cont4 = 0            # Checking if the map is finished.
        cont5 = 0
        
        tagv = sel_random(new_agv, 5)
        print tagv
#         random.shuffle(kho[v1])
#         rnc1 = tagv[0][]
#         random.shuffle(kho[v2])
#         rnc2 = kho[v2][0]
#         random.shuffle(kho[v3])
#         rnc3 = kho[v3][0]
#         random.shuffle(kho[v4])
#         rnc4 = kho[v4][0]
#         random.shuffle(kho[v5])
#         rnc5 = kho[v5][0]
#         print rnc1, rnc2, rnc3, rnc4, rnc5
        
        lststep[i][1] = copy.deepcopy(tagv[0][0])
        lststep[i][2] = copy.deepcopy(tagv[0][1])
        lststep[i][3] = copy.deepcopy(tagv[1][0])
        lststep[i][4] = copy.deepcopy(tagv[1][1])
        lststep[i][5] = copy.deepcopy(tagv[2][0])
        lststep[i][6] = copy.deepcopy(tagv[2][1])
        lststep[i][7] = copy.deepcopy(tagv[3][0])
        lststep[i][8] = copy.deepcopy(tagv[3][1])
        lststep[i][9] = copy.deepcopy(tagv[4][0])
        lststep[i][10] = copy.deepcopy(tagv[4][1])       
        lststep[i][11] = copy.deepcopy(comp_var)
        lststep[i][12] = copy.deepcopy(user_match_perc)
        
        print "/nIteration No: ", iter+1
        
        row_cp_map1 = copy.deepcopy(tagv[0][0])
        col_cp_map1 = copy.deepcopy(tagv[0][1])
        row_cp_map2 = copy.deepcopy(tagv[1][0])
        col_cp_map2 = copy.deepcopy(tagv[1][1])
        row_cp_map3 = copy.deepcopy(tagv[2][0])
        col_cp_map3 = copy.deepcopy(tagv[2][1])
        row_cp_map4 = copy.deepcopy(tagv[3][0])
        col_cp_map4 = copy.deepcopy(tagv[3][1])
        row_cp_map5 = copy.deepcopy(tagv[4][0])
        col_cp_map5 = copy.deepcopy(tagv[4][1])
        
        print row_cp_map1, ", ", col_cp_map1, ", ", row_cp_map2, ", ", col_cp_map2
        
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
        
        steps = 0
    
        done = 0
        
        
        while done == 0:  
            if one_two_done == 1:
                nmap12 = map_merge5(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
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
                    #print "Merge 12"     
            if one_three_done == 1:
                nmap13 = map_merge5(r13_a, r13_b, r13_c, r13_d, mat1, mat3, 1)
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
                    #print "Merge 13"
            if one_four_done == 1:
                nmap14 = map_merge5(r14_a, r14_b, r14_c, r14_d, mat1, mat4, 1)
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
                    #print "Merge 14"
            if one_five_done == 1:
                nmap15 = map_merge5(r15_a, r15_b, r15_c, r15_d, mat1, mat5, 1)
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
                    #print "Merge 15"
            if two_three_done == 1:
                nmap23 = map_merge5(r23_a, r23_b, r23_c, r23_d, mat2, mat3, 1)
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
                    #print "Merge 23"
            if two_four_done == 1:
                nmap24 = map_merge5(r24_a, r24_b, r24_c, r24_d, mat2, mat4, 1)
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
                    #print '"Merge 24"'
            if two_five_done == 1:
                nmap25 = map_merge5(r25_a, r25_b, r25_c, r25_d, mat2, mat5, 1)
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
                    #print "Merge 25"
            if three_four_done == 1:
                nmap34 = map_merge5(r34_a, r34_b, r34_c, r34_d, mat3, mat4, 1)
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
                    #print "Merge 34"
            if three_five_done == 1:
                nmap35 = map_merge5(r35_a, r35_b, r35_c, r35_d, mat3, mat5, 1)
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
                    #print "Merge 35"
            if four_five_done == 1:
                nmap45 = map_merge5(r45_a, r45_b, r45_c, r45_d, mat4, mat5, 1)
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
                    #print "Merge 45"
                  
            
            answer1 = motion_deciding_function5(mat1, orient1, row_cp_local1, col_cp_local1, afv1)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            answer2 = motion_deciding_function5(mat2, orient2, row_cp_local2, col_cp_local2, afv2)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            answer3 = motion_deciding_function5(mat3, orient3, row_cp_local3, col_cp_local3, afv3)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            answer4 = motion_deciding_function5(mat4, orient4, row_cp_local4, col_cp_local4, afv4)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            answer5 = motion_deciding_function5(mat5, orient5, row_cp_local5, col_cp_local5, afv5)     #Parameters: mat1, orient, row_cp_local, col_cp_local, afv
            #print "answer1 = ", answer1
            #print "answer2 = ", answer2
            #print "answer3 = ", answer3
            
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
            
            afv1 = adj_field_value(row_cp_map1, col_cp_map1, real_map)
            afv2 = adj_field_value(row_cp_map2, col_cp_map2, real_map)
            afv3 = adj_field_value(row_cp_map3, col_cp_map3, real_map)
            afv4 = adj_field_value(row_cp_map4, col_cp_map4, real_map)
            afv5 = adj_field_value(row_cp_map5, col_cp_map5, real_map)
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
            
            # Updating variables for robot 1    
            var_list1 = var_update5(mat1, row_next_pos1, col_next_pos1, row_cp_map1, col_cp_map1, row_cp_local1, col_cp_local1, orient1, fv1, afv1)
            var_list2 = var_update5(mat2, row_next_pos2, col_next_pos2, row_cp_map2, col_cp_map2, row_cp_local2, col_cp_local2, orient2, fv2, afv2)
            var_list3 = var_update5(mat3, row_next_pos3, col_next_pos3, row_cp_map3, col_cp_map3, row_cp_local3, col_cp_local3, orient3, fv3, afv3)
            var_list4 = var_update5(mat4, row_next_pos4, col_next_pos4, row_cp_map4, col_cp_map4, row_cp_local4, col_cp_local4, orient4, fv4, afv4)
            var_list5 = var_update5(mat5, row_next_pos5, col_next_pos5, row_cp_map5, col_cp_map5, row_cp_local5, col_cp_local5, orient5, fv5, afv5)
            
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
                r23_c = r23_c + 1
            elif var_list3[8] == 'W':
                r34_b = r34_b + 1
                r35_b = r35_b + 1
                r13_d = r13_d + 1
                r23_d = r23_d + 1
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
            
            if one_two_done == 1:
                nmap12 = map_merge5(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
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
                    #print "Merge 12"                     
            else:
                matched12 = matching5(mat1, mat2, comp_var, user_match_perc)
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
                    
                    #print 'Mat1 and Mat2 have been merged at step = ', steps
#             if (one_two_done == 1) and (mat1 != mat2):
#                 lststep[i][0] = 0
#                 break
                
                    
            if one_three_done == 1:
                nmap13 = map_merge5(r13_a, r13_b, r13_c, r13_d, mat1, mat3, 1)
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
                    #print "Merge 13"
            else:
                matched13 = matching5(mat1, mat3, comp_var, user_match_perc)
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
                    #print 'Mat1 and Mat3 have been merged at step = ', steps
#             if (one_three_done == 1) and (mat1 != mat3):
#                 lststep[i][0] = 0
#                 break
            
            if one_four_done == 1:
                nmap14 = map_merge5(r14_a, r14_b, r14_c, r14_d, mat1, mat4, 1)
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
                    #print "Merge 14"   
            else:
                matched14 = matching5(mat1, mat4, comp_var, user_match_perc)
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
                    #print 'Mat1 and Mat4 have been merged at step = ', steps
#             if (one_four_done == 1) and (mat1 != mat4):
#                 lststep[i][0] = 0
#                 break
                    
            if one_five_done == 1:
                nmap15 = map_merge5(r15_a, r15_b, r15_c, r15_d, mat1, mat5, 1)
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
                    #print "Merge 15"
            else:
                matched15 = matching5(mat1, mat5, comp_var, user_match_perc)
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
                    #print 'Mat1 and Mat5 have been merged at step = ', steps
#             if (one_five_done == 1) and (mat1 != mat5):
#                 lststep[i][0] = 0
#                 break        
            
            if two_three_done == 1:
                nmap23 = map_merge5(r23_a, r23_b, r23_c, r23_d, mat2, mat3, 1)
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
                    #print "Merge 23"
            else:      
                matched23 = matching5(mat2, mat3, comp_var, user_match_perc)
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
                    #print 'Mat2 and Mat3 have been merged at step = ', steps
#             if (two_three_done == 1) and (mat2 != mat3):
#                 lststep[i][0] = 0
#                 break
                    
            if two_four_done == 1:
                nmap24 = map_merge5(r24_a, r24_b, r24_c, r24_d, mat2, mat4, 1)
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
                    #print '"Merge 24"'
            else:
                matched24 = matching5(mat2, mat4, comp_var, user_match_perc)
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
                    #print 'Mat2 and Mat4 have been merged at step = ', steps
#             if (two_four_done == 1) and (mat2 != mat4):
#                 lststep[i][0] = 0
#                 break
                
            if two_five_done == 1:
                nmap25 = map_merge5(r25_a, r25_b, r25_c, r25_d, mat2, mat5, 1)
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
                    #print "Merge 25"
            else:
                matched25 = matching5(mat2, mat5, comp_var, user_match_perc)
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
                    #print 'Mat2 and Mat5 have been merged at step = ', steps
#             if (two_five_done == 1) and (mat2 != mat5):
#                 lststep[i][0] = 0
#                 break
                
            if three_four_done == 1:
                nmap34 = map_merge5(r34_a, r34_b, r34_c, r34_d, mat3, mat4, 1)
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
                    #print "Merge 34"
            else:
                matched34 = matching5(mat3, mat4, comp_var, user_match_perc)
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
                    #print 'Mat3 and Mat4 have been merged at step = ', steps
#             if (three_four_done == 1) and (mat3 != mat4):
#                 lststep[i][0] = 0
#                 break
                    
            if three_five_done == 1:
                nmap35 = map_merge5(r35_a, r35_b, r35_c, r35_d, mat3, mat5, 1)
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
                    #print "Merge 35"
            else:
                matched35 = matching5(mat3, mat5, comp_var, user_match_perc)
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
                    #print 'Mat3 and Mat5 have been merged at step = ', steps
#             if (three_five_done == 1) and (mat3 != mat5):
#                 lststep[i][0] = 0
#                 break
                
            if four_five_done == 1:
                nmap45 = map_merge5(r45_a, r45_b, r45_c, r45_d, mat4, mat5, 1)
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
                    #print "Merge 45"
            else:
                matched45 = matching5(mat4, mat5, comp_var, user_match_perc)
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
                    #print 'Mat4 and Mat5 have been merged at step = ', steps
#             if (four_five_done == 1) and (mat4 != mat5):
#                 lststep[i][0] = 0
#                 break

            if one_two_done == 1:
                nmap12 = map_merge5(r12_a, r12_b, r12_c, r12_d, mat1, mat2, 1)
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
                    #print "Merge 12"     
            if one_three_done == 1:
                nmap13 = map_merge5(r13_a, r13_b, r13_c, r13_d, mat1, mat3, 1)
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
                    #print "Merge 13"
            if one_four_done == 1:
                nmap14 = map_merge5(r14_a, r14_b, r14_c, r14_d, mat1, mat4, 1)
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
                    #print "Merge 14"
            if one_five_done == 1:
                nmap15 = map_merge5(r15_a, r15_b, r15_c, r15_d, mat1, mat5, 1)
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
                    #print "Merge 15"
            if two_three_done == 1:
                nmap23 = map_merge5(r23_a, r23_b, r23_c, r23_d, mat2, mat3, 1)
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
                    #print "Merge 23"
            if two_four_done == 1:
                nmap24 = map_merge5(r24_a, r24_b, r24_c, r24_d, mat2, mat4, 1)
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
                    #print '"Merge 24"'
            if two_five_done == 1:
                nmap25 = map_merge5(r25_a, r25_b, r25_c, r25_d, mat2, mat5, 1)
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
                    #print "Merge 25"
            if three_four_done == 1:
                nmap34 = map_merge5(r34_a, r34_b, r34_c, r34_d, mat3, mat4, 1)
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
                    #print "Merge 34"
            if three_five_done == 1:
                nmap35 = map_merge5(r35_a, r35_b, r35_c, r35_d, mat3, mat5, 1)
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
                    #print "Merge 35"
            if four_five_done == 1:
                nmap45 = map_merge5(r45_a, r45_b, r45_c, r45_d, mat4, mat5, 1)
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
                    #print "Merge 45"
            
            
            no_of_B_left1 = 0
            no_of_B_left2 = 0
            no_of_B_left3 = 0
            no_of_B_left4 = 0
            no_of_B_left5 = 0
            
            cont1 = 0            # Checking if the map is finished.
            cont2 = 0            # Checking if the map is finished.
            cont3 = 0            # Checking if the map is finished.
            cont4 = 0            # Checking if the map is finished.
            cont5 = 0
            
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
            
            if ((len(mat1) > 18) or ((len(mat1[0]) > 18))) or ((len(mat2) > 18) or ((len(mat2[0]) > 18))) or ((len(mat3) > 18) or ((len(mat3[0]) > 18))) or ((len(mat4) > 18) or ((len(mat4[0]) > 18))) or ((len(mat5) > 18) or ((len(mat5[0]) > 18))):
                lststep[i][0] = 0
                break
            
            
            if (cont1 == 1) or (cont2 == 1) or (cont3 == 1) or (cont4 == 1) or (cont5 == 1):
                if (no_of_B_left1 == 0) or (no_of_B_left2 == 0) or (no_of_B_left3 == 0) or (no_of_B_left4 == 0) or (no_of_B_left5 == 0):
                    done = 1
                    print "Jhala 2"
                    lststep[i][0] = steps
                else:
                    done = 0
                #print "The map is still not finished. B's left = ", no_of_B_left1 + no_of_B_left2 + no_of_B_left3 + no_of_B_left4 + no_of_B_left5
                #raw_input("Press Enter to continue...")
            else: 
                lststep[i][0] = steps
                done = 1
        #time.sleep(0.5)
        iter = iter + 1
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Data5Robot')
    col0_name = 'No. of Steps.'
    col1_name = 'Row 1'
    col2_name = 'Col 1'
    col3_name = 'Row 2'
    col4_name = 'Col 2'
    col5_name = 'Row 3'
    col6_name = 'Col 3'
    col7_name = 'Row 4'
    col8_name = 'Col 4'
    col9_name = 'Row 5'
    col10_name = 'Col 5'
    
    ws.write(0, 1, "Comparison Window Size: ")
    ws.write(0, 4, "Acceptable Match Perc: ")
    ws.write(0, 3, str(comp_var))
    ws.write(0, 6, str(user_match_perc))
    
    ws.write(1, 0, col0_name)
    ws.write(1, 1, col1_name)
    ws.write(1, 2, col2_name)
    ws.write(1, 3, col3_name)    
    ws.write(1, 4, col4_name)
    ws.write(1, 5, col5_name)
    ws.write(1, 6, col6_name)
    ws.write(1, 7, col7_name)
    ws.write(1, 8, col8_name)
    ws.write(1, 9, col9_name)
    ws.write(1, 10, col10_name)
    for p in range(len(lststep)):
        ws.write(p+2, 0, lststep[p][0])
        ws.write(p+2, 1, lststep[p][1])
        ws.write(p+2, 2, lststep[p][2])
        ws.write(p+2, 3, lststep[p][3]) 
        ws.write(p+2, 4, lststep[p][4])
        ws.write(p+2, 5, lststep[p][5])  
        ws.write(p+2, 6, lststep[p][6])   
        ws.write(p+2, 7, lststep[p][7]) 
        ws.write(p+2, 8, lststep[p][8])
        ws.write(p+2, 9, lststep[p][9])  
        ws.write(p+2, 10, lststep[p][10])   
    bookname = 'Map-' + str(mapno) + '--Robots5--WS-' + str(comp_var) + '--AP-' + str(int((user_match_perc))) + '.xls'
    wb.save(bookname)