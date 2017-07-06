'''
Created on Mar 13, 2017

@author: rjw0028
'''
import xlwt
import random
import copy
import time
from Funcs1robot import *

style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')

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
                 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],]

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
                 [0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
                 [1,1,1,1,1,1,0,0,0,0,1,0,0,0,0,1],
                 [1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],
                 [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
                 [1,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1],
                 [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
                 [1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],
                 [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],
                 [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],
                 [1,1,1,1,1,1,0,0,0,0,1,0,0,0,1,0],
                 [1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0],
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


choice = input("Please enter the map_choice: 0 through 4:")
real_map = map_choice[choice]

complete = 0

agv = all_good_values(real_map) # List of all Good Values
new_agv = copy.deepcopy(agv)

iter = 0
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
            loggg = open("logg.txt", "a")
#             print "Name of the file: ", loggg.name
#             print "Closed or not : ", loggg.closed
#             print "Opening mode : ", loggg.mode
            st = str(steps)
            rowncol = str(rnc)
            loggg.write("\nStart Position and Distance: ")
            loggg.write(rowncol)
            loggg.write("\nNo. of Steps: ")
            loggg.write(st)
            loggg.close() 
            
            
            
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
    
        wb.save("Data1Rob.xls")
        complete = 100
    else:
        complete = 0
        
print "And we should be done..."