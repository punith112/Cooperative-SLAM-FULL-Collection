'''
Created on Mar 13, 2017

@author: rjw0028
'''
import math
global occ
occ = 0

def cp_field_value(all_adj_positions):
    if all_adj_positions[0]==all_adj_positions[1]==all_adj_positions[2]==all_adj_positions[3]==1:
        field_value = 9
    elif all_adj_positions[1]==all_adj_positions[2]==all_adj_positions[3]==1 and all_adj_positions[0]==0:
        field_value = 1
    elif all_adj_positions[1]==all_adj_positions[2]==all_adj_positions[0]==1 and all_adj_positions[3]==0:
        field_value = 4
    elif all_adj_positions[1]==all_adj_positions[3]==all_adj_positions[0]==1 and all_adj_positions[2]==0:
        field_value = 3
    elif (all_adj_positions[3]==all_adj_positions[2]==all_adj_positions[0]==1) and (all_adj_positions[1]==0):
        field_value = 2
    elif (all_adj_positions[0]==all_adj_positions[1]==1) and (all_adj_positions[3]==all_adj_positions[2]==0):
        field_value = 5
    elif (all_adj_positions[2]==all_adj_positions[3]==1) and (all_adj_positions[1]==all_adj_positions[0]==0):
        field_value = 7
    elif (all_adj_positions[1]==all_adj_positions[2]==1) and (all_adj_positions[0]==all_adj_positions[3]==0):
        field_value = 6
    elif (all_adj_positions[0]==all_adj_positions[3]==1) and (all_adj_positions[1]==all_adj_positions[2]==0):
        field_value = 8
    else:
        field_value = 0
    return field_value


def first_map_update(fv, afv):    # called as 'update_map' in the psuedocode...
    mat1 = [['D' for x in range(3)] for y in range(3)]
    mat1[1][1] = fv # fv is the current position field value, its a char type value
    if afv[0] == 1:
        mat1[0][1] = 'B'
    elif afv[0] == 0:
        mat1[0][1] = 'A'
    
    if afv[1] == 1:    # Valid case true for east
        mat1[1][2] = 'B'
    else: 
        mat1[1][2] = 'A'
    
    if afv[2] == 1:    # Valid case true for south
        mat1[2][1] = 'B'
    else:
        mat1[2][1] = 'A'
    
    if afv[3] == 1:    # Valid case true for west
        mat1[1][0] = 'B'
    else:
        mat1[1][0] = 'A'
    
    mat1[0][0] = 'C'
    mat1[0][2] = 'C'
    mat1[2][0] = 'C'
    mat1[2][2] = 'C'
    return mat1

def adj_field_value(row_cp_map, col_cp_map, real_map):
    afv = [0,0,0,0]
    if row_cp_map == 0:
        afv[0] = 0
    elif real_map[row_cp_map - 1][col_cp_map] == 1:   
        afv[0] = 1
    
    if col_cp_map == len(real_map[0]) - 1:
        afv[1] = 0
    elif real_map[row_cp_map][col_cp_map + 1] == 1:
        afv[1] = 1
        
    if row_cp_map == len(real_map) - 1:
        afv[2] = 0
    elif real_map[row_cp_map + 1][col_cp_map] == 1:
        afv[2] = 1
        
    if col_cp_map == 0:
        afv[3] = 0
    elif real_map[row_cp_map][col_cp_map - 1] == 1:
        afv[3] = 1
    return afv
def motion_deciding_function(mat1, orient, row_cp_local, col_cp_local, afv ):
    if (mat1[row_cp_local-1][col_cp_local] == 'B') or (mat1[row_cp_local+1][col_cp_local] == 'B') or (mat1[row_cp_local][col_cp_local - 1] == 'B') or (mat1[row_cp_local][col_cp_local+1] == 'B'):
        for i in range(4):
            if orient == i:
                answer = minus_1(i)
                if afv[answer] != 1:    # afv is a variable in main, that stores the values of adjacent fields of the current position
                    answer = i
                    if afv[answer] != 1:
                        answer = plus_1(i)
                        if afv[answer] != 1:
                            answer = plus_1(answer)
        return answer
    else:
        # Now this is a dead-end situation...
        imagine = function_to_start_imaginary(mat1, row_cp_local, col_cp_local, afv)
        # imagine has [paths, rows, cols]
        paths = imagine[0]
        rows = imagine[1]
        cols = imagine[2]
        #print 'paths = ', paths
        #print 'rows = ', rows
        #print 'cols = ', cols
        
        
        end = 0
        while end == 0:
            row_of_B = 999
            path_rows = len(paths)
            path_cols = len(paths[0])
            
            for i in range(path_rows):
                if mat1[rows[i]][cols[i]] == 'B':
                    row_of_B = i
                    end = 1
                    break
            if row_of_B != 999:
                route = [9 for x in range(path_cols)]
                for t in range(path_cols):
                    route[t] = paths[row_of_B][t]
                    answer = route[0]
                    return answer
            else:
                u = func_to_add_one_step(mat1, paths, rows, cols, afv)
                paths = u[0]
                rows = u[1]
                cols = u[2]
                new_paths_added = u[3]
def minus_1(val):
    if val == 0:
        val = 3
    else:
        val = val - 1
    return val

def plus_1(val):
    if val == 3:
        val = 0
    else:
        val = val + 1
    return val
def var_update(mat, row_next_pos, col_next_pos, row_cp_map, col_cp_map, row_cp_local, col_cp_local, orient, fv, afv):
    #global row_cp_map, col_cp_map, row_cp_local, col_cp_local, orient    # Remove these variables from the parameters list of this function after testing is done
    mat_row_low = 0
    mat_col_low = 0
    mat_row_high = len(mat)
    mat_col_high = len(mat[0])
    
    ##print 'mat[row_cp_local][col_cp_local+1] = ', mat[row_cp_local][col_cp_local+1]
    if row_next_pos == mat_row_low:     # This part is when the robot has reached the edge of the current map
        mat_new = make_new_array('N', mat)    # after this there will be virtual movement by the robot_ That is we change it's variables___
        ##row_cp_local = row_cp_local;       we can convert such lines which do not change the variable into comments___
        ##col_cp_local = col_cp_local;
        #row_cp_map = row_cp_map - 1
        ##col_cp_map = col_cp_map;
        orient = 0
        ##print 'row_next_pos == mat_row_low' 
    elif row_next_pos == mat_row_high - 1:
        mat_new = make_new_array('S', mat)
        row_cp_local = row_cp_local + 1
        #col_cp_local = col_cp_local;
        #row_cp_map = row_cp_map + 1;
        #col_cp_map = col_cp_map;
        orient = 2
        ##print 'row_next_pos == mat_row_high'
    elif col_next_pos == mat_col_low:
        mat_new = make_new_array('W', mat)
        #row_cp_local = row_cp_local;
        #col_cp_local = col_cp_local;
        #row_cp_map = row_cp_map;
        #col_cp_map = col_cp_map - 1
        #mat1_row_low = mat1_row_low;
        orient = 3
        ##print 'col_next_pos == mat_col_low'
    elif col_next_pos == mat_col_high - 1:
        mat_new = make_new_array('E', mat)
        #row_cp_local = row_cp_local;
        col_cp_local = col_cp_local + 1
        #row_cp_map = row_cp_map;
        #col_cp_map = col_cp_map + 1;
        #mat1_row_low = mat1_row_low;
        orient = 1
        ##print 'col_next_pos == mat_col_high'
    else:
        ##print 'We are here'
        mat_new = mat
        #print mat_new[row_cp_local][col_cp_local+1]
        if row_next_pos < row_cp_local:          # Going North but not on any edge
            #row_cp_map = row_cp_map - 1
            row_cp_local = row_cp_local - 1
            orient = 0
        elif row_next_pos > row_cp_local:        # Going South but not on any edge
            #row_cp_map = row_cp_map + 1
            row_cp_local = row_cp_local + 1
            orient = 2
        elif col_next_pos < col_cp_local:        # Going West but not on any edge
            #col_cp_map = col_cp_map - 1
            col_cp_local = col_cp_local - 1
            orient = 3
        elif col_next_pos > col_cp_local:        # Going East but not on any edge
            #col_cp_map = col_cp_map + 1
            col_cp_local = col_cp_local + 1
            orient = 1
    mat_new[row_cp_local][col_cp_local] = fv
        
    if afv[0] == 1 and (mat_new[row_cp_local-1][col_cp_local] == 'C' or mat_new[row_cp_local-1][col_cp_local] == 'B' or mat_new[row_cp_local-1][col_cp_local] == 'D'):
        mat_new[row_cp_local-1][col_cp_local] = 'B'
    elif afv[0] == 0:
        mat_new[row_cp_local-1][col_cp_local] = 'A'
    
    if afv[1] == 1 and (mat_new[row_cp_local][col_cp_local+1] == 'C' or mat_new[row_cp_local][col_cp_local+1] == 'B' or mat_new[row_cp_local][col_cp_local+1] == 'D'):
        mat_new[row_cp_local][col_cp_local+1] = 'B'
    elif afv[1] == 0:
        mat_new[row_cp_local][col_cp_local+1] = 'A'
            
    if afv[2] == 1 and (mat_new[row_cp_local+1][col_cp_local] == 'C' or mat_new[row_cp_local+1][col_cp_local] == 'B' or mat_new[row_cp_local+1][col_cp_local] == 'D'):
        mat_new[row_cp_local+1][col_cp_local] = 'B'
    elif afv[2] == 0:
        mat_new[row_cp_local+1][col_cp_local] = 'A'
        
    if afv[3] == 1 and (mat_new[row_cp_local][col_cp_local-1] == 'C' or mat_new[row_cp_local][col_cp_local-1] == 'B' or mat_new[row_cp_local][col_cp_local-1] == 'D'):
        mat_new[row_cp_local][col_cp_local-1] = 'B'
    elif afv[3] == 0:
        mat_new[row_cp_local][col_cp_local-1] = 'A'
    
    for k in range(len(mat_new)):
        for l in range(len(mat_new[0])):
            if mat_new[k][l] == 'D':
                mat_new[k][l] = 'C'
                
    
    return [mat_new, row_next_pos, col_next_pos, row_cp_map, col_cp_map, row_cp_local, col_cp_local, orient]
def function_to_start_imaginary(mat1, row_cp_local, col_cp_local, afv): # Will happen only once... Whenever we get a deadend...
    #print "Here we enter the function_to_start_imaginary"
    
    e = row_cp_local
    f = col_cp_local
    #print mat1
    #print 'row_cp_local = ', e
    #print 'col_cp_local = ', f
    
    if mat1[e][f] == 0:
        nc = afv.count(1)
        #print 'nc = ', nc
        path_rows = nc
        path_cols = 1
        r = 0
        c = 0
        paths = [[9 for x in range(path_cols)] for y in range(path_rows)]   # Initializing with 9 since it isn't used anywhere else
        rows = [0 for x in range(path_rows)]
        cols = [0 for x in range(path_rows)]
        if nc == 1:
            if mat1[e-1][f] != 'A':
                paths[r][c] = 0
                rows[r] = e - 1
                cols[r] = f
            elif mat1[e+1][f] != 'A':
                paths[r][c] = 2
                rows[r] = e + 1
                cols[r] = f
            elif mat1[e][f-1] != 'A':
                paths[r][c] = 3
                rows[r] = e
                cols[r] = f - 1
            else:
                paths[r][c] = 1
                rows[r] = e
                cols[r] = f + 1
                
        else:
            if mat1[e-1][f] != 'A':
                paths[r][c] = 0
                rows[r] = e - 1
                cols[r] = f
                paths[r+1][c] = 2
                rows[r+1] = e + 1
                cols[r+1] = f 
            elif mat1[e][f-1] != 'A':
                paths[r][c] = 1
                rows[r] = e
                cols[r] = f + 1
                paths[r+1][c] = 3
                rows[r+1] = e
                cols[r+1] = f - 1
                
    elif (mat1[e][f] == 5) or (mat1[e][f] == 6) or (mat1[e][f] == 7) or (mat1[e][f] == 8):
        path_rows = 2
        path_cols = 1
        paths = [[9 for x in range(path_cols)] for y in range(path_rows)]   # Initializing with 9 since it isn't used anywhere else
        rows = [0 for x in range(path_rows)]
        cols = [0 for x in range(path_rows)]
        r = 0
        c = 0
        if mat1[e][f] == 5:
            paths[r][c] = 0
            rows[r] = e - 1
            cols[r] = f
            paths[r+1][c] = 1
            rows[r+1] = e
            cols[r+1] = f + 1
        elif mat1[e][f] == 6:
            paths[r][c] = 1
            rows[r] = e
            cols[r] = f + 1
            paths[r+1][c] = 2
            rows[r+1] = e + 1
            cols[r+1] = f
        elif mat1[e][f] == 7:
            paths[r][c] = 2
            rows[r] = e + 1
            cols[r] = f
            paths[r+1][c] = 3
            rows[r+1] = e
            cols[r+1] = f - 1
        elif mat1[e][f] == 8:
            paths[r][c] = 3
            rows[r] = e
            cols[r] = f - 1
            paths[r+1][c] = 0
            rows[r+1] = e - 1
            cols[r+1] = f
    elif (mat1[e][f] == 1) or (mat1[e][f] == 2) or (mat1[e][f] == 3) or (mat1[e][f] == 4):
        path_rows = 3
        path_cols = 1
        paths = [[9 for x in range(path_cols)] for y in range(path_rows)]   # Initializing with 9 since it isn't used anywhere else
        rows = [0 for x in range(path_rows)]
        cols = [0 for x in range(path_rows)]
        r = 0
        c = 0
        if mat1[e][f] == 1:
            paths[r][c] = 1
            rows[r] = e
            cols[r] = f + 1
            paths[r+1][c] = 2
            rows[r+1] = e + 1
            cols[r+1] = f
            paths[r+2][c] = 3
            rows[r+2] = e
            cols[r+2] = f - 1
        elif mat1[e][f] == 2:
            paths[r][c] = 2
            rows[r] = e + 1
            cols[r] = f
            paths[r+1][c] = 3
            rows[r+1] = e
            cols[r+1] = f - 1
            paths[r+2][c] = 0
            rows[r+2] = e - 1
            cols[r+2] = f
        elif mat1[e][f] == 3:
            paths[r][c] = 3
            rows[r] = e
            cols[r] = f - 1
            paths[r+1][c] = 0
            rows[r+1] = e - 1
            cols[r+1] = f
            paths[r+2][c] = 1
            rows[r+2] = e 
            cols[r+2] = f + 1
        elif mat1[e][f] == 4:
            paths[r][c] = 0
            rows[r] = e - 1
            cols[r] = f
            paths[r+1][c] = 1
            rows[r+1] = e
            cols[r+1] = f + 1
            paths[r+2][c] = 2
            rows[r+2] = e + 1
            cols[r+2] = f
    elif mat1[e][f] == 9:
        path_rows = 4
        path_cols = 1
        paths = [[9 for x in range(path_cols)] for y in range(path_rows)]   # Initializing with 9 since it isn't used anywhere else
        rows = [0 for x in range(path_rows)]
        cols = [0 for x in range(path_rows)]
        r = 0
        c = 0
        paths[r][c] = 0
        rows[r] = e - 1
        cols[r] = f
        paths[r+1][c] = 1
        rows[r+1] = e
        cols[r+1] = f + 1
        paths[r+2][c] = 2
        rows[r+2] = e + 1
        cols[r+2] = f
        paths[r+3][c] = 3
        rows[r+3] = e
        cols[r+3] = f - 1
    return [paths, rows, cols]

# Function_to_start_imaginary   Ends here.....
def func_to_add_one_step(mat1, paths, rows, cols, afv): # before every occurence of this function, it is checked if one of the neighbors is B
    global occ
    occ += 1
    #print 'Here we enter the func_to_add_one_step. Occurence = ', occ
    new_paths_counter = 0
    u = 0
    path_rows = len(paths)
    path_cols = len(paths[0])    # Check this later. What do you fill in the paths row where you have reached a dead-end again?
        
    path_count = total_paths_counter(mat1, paths, rows, cols, afv)
    
    temp_paths = [[9 for x in range(path_cols+1)] for y in range(path_count)]
    temp_cols = [0 for x in range(path_count)]
    temp_rows = [0 for x in range(path_count)]
    
    ##print 'temp_paths = ', temp_paths
    ##print 'temp_rows = ', temp_rows
    ##print 'temp_cols = ', temp_cols
    
    #for i in range(path_rows):
        #for m in range(path_cols):
            #temp_paths[u][m] = paths[i][m]
        #u = u + 1  
    
    for i in range(path_rows):
        if paths[i][path_cols-1] == 5:
            for m in range(path_cols):
                temp_paths[u][m] = paths[i][m]
            temp_paths[u][path_cols] = 5
            temp_rows[u] = rows[i]
            temp_cols[u] = cols[i]
            u += 1
        
        elif mat1[rows[i]][cols[i]] == 0:
            for m in range(path_cols):
                temp_paths[u][m] = paths[i][m]
            afv1 = [0,0,0,0]
            
            if mat1[rows[i]-1][cols[i]] != 'A':
                afv1[0] = 1
            if mat1[rows[i]][cols[i]+1] != 'A':
                afv1[1] = 1
            if mat1[rows[i]+1][cols[i]] != 'A':
                afv1[2] = 1
            if mat1[rows[i]][cols[i]-1] != 'A':
                afv1[3] = 1
                
            nc = afv1.count(1) # afv must be defined again for the current value of 
            if nc == 2:
                temp_paths[u][path_cols] = paths[i][path_cols-1]
                if paths[i][path_cols-1] == 0:
                    temp_rows[u] = rows[i] - 1
                    temp_cols[u] = cols[i]
                
                elif paths[i][path_cols-1] == 1:
                    temp_cols[u] = cols[i] + 1
                    temp_rows[u] = rows[i]
                
                elif paths[i][path_cols-1] == 2:
                    temp_rows[u] = rows[i] + 1
                    temp_cols[u] = cols[i]
                
                elif paths[i][path_cols-1] == 3:
                    temp_cols[u] = cols[i] - 1
                    temp_rows[u] = rows[i]
                u += 1
            elif nc == 1:
                temp_paths[u][path_cols] = 5
                temp_rows[u] = rows[i]
                temp_cols[u] = cols[i]
                u = u + 1
        
        elif mat1[rows[i]][cols[i]] == 5 or mat1[rows[i]][cols[i]] == 6 or mat1[rows[i]][cols[i]] == 7 or mat1[rows[i]][cols[i]] == 8:
            for m in range(path_cols):
                temp_paths[u][m] = paths[i][m]
            if mat1[rows[i]][cols[i]] == 5:
                if paths[i][path_cols - 1] == 2:
                    temp_paths[u][path_cols]=1
                    temp_cols[u] = cols[i] + 1
                    temp_rows[u] = rows[i]
                elif paths[i][path_cols - 1] == 3:
                    temp_paths[u][path_cols]=0
                    temp_cols[u] = cols[i]
                    temp_rows[u] = rows[i] - 1
            elif mat1[rows[i]][cols[i]] == 6:
                if paths[i][path_cols - 1] == 0:
                    temp_paths[u][path_cols]=1
                    temp_cols[u] = cols[i] + 1
                    temp_rows[u] = rows[i]
                elif paths[i][path_cols - 1] == 3:
                    temp_paths[u][path_cols]=2
                    temp_cols[u] = cols[i]
                    temp_rows[u] = rows[i] + 1
            elif mat1[rows[i]][cols[i]] == 7:
                if paths[i][path_cols -1] == 0:
                    temp_paths[u][path_cols]=3
                    temp_cols[u] = cols[i] - 1
                    temp_rows[u] = rows[i]
                elif paths[i][path_cols - 1] == 1:
                    temp_paths[u][path_cols]=2
                    temp_cols[u] = cols[i]
                    temp_rows[u] = rows[i] + 1
            elif mat1[rows[i]][cols[i]] == 8:
                if paths[i][path_cols -1] == 2:
                    temp_paths[u][path_cols]=3
                    temp_cols[u] = cols[i] - 1   
                    temp_rows[u] = rows[i]
                elif paths[i][path_cols - 1] == 1:
                    temp_paths[u][path_cols]=0
                    temp_cols[u] = cols[i]
                    temp_rows[u] = rows[i] - 1
            u = u + 1;
        
        elif mat1[rows[i]][cols[i]] == 1 or mat1[rows[i]][cols[i]] == 2 or mat1[rows[i]][cols[i]] == 3 or mat1[rows[i]][cols[i]] == 4:
            for m in range(path_cols):
                temp_paths[u][m] = paths[i][m]
                temp_paths[u+1][m] = paths[i][m]
            new_paths_counter = new_paths_counter + 1
            if mat1[rows[i]][cols[i]] == 1:
                # row_filler(pc, i, 2, u);
                if paths[i][path_cols-1] == 3:
                    temp_paths[u][path_cols] = 2
                    temp_cols[u] = cols[i]
                    temp_rows[u] = rows[i] + 1
                    temp_paths[u+1][path_cols] = 3
                    temp_cols[u+1] = cols[i] - 1
                    temp_rows[u+1] = rows[i]
                    # u = u + 2
                elif paths[i][path_cols-1] == 1:
                    temp_paths[u][path_cols] = 2
                    temp_cols[u] = cols[i]
                    temp_rows[u] = rows[i] + 1
                    temp_paths[u+1][path_cols] = 1
                    temp_cols[u+1] = cols[i] + 1
                    temp_rows[u+1] = rows[i]
                    # u = u + 2;
                elif paths[i][path_cols-1] == 0:
                    temp_paths[u][path_cols] = 1
                    temp_cols[u] = cols[i] + 1
                    temp_rows[u] = rows[i]
                    temp_paths[u+1][path_cols] = 3
                    temp_cols[u+1] = cols[i] - 1
                    temp_rows[u+1] = rows[i]
                    # u = u + 2
            elif mat1[rows[i]][cols[i]] == 2:
                if paths[i][path_cols-1] == 0:
                    temp_paths[u][path_cols] = 0
                    temp_cols[u] = cols[i]
                    temp_rows[u] = rows[i] - 1
                    temp_paths[u+1][path_cols] = 3
                    temp_cols[u+1] = cols[i] - 1
                    temp_rows[u+1] = rows[i]
                elif paths[i][path_cols-1] == 1:
                    temp_paths[u][path_cols] = 0
                    temp_cols[u] = cols[i]
                    temp_rows[u] = rows[i] - 1
                    temp_paths[u+1][path_cols] = 2
                    temp_cols[u+1] = cols[i]
                    temp_rows[u+1] = rows[i] + 1
                    # u = u + 2
                elif paths[i][path_cols-1] == 2:
                    temp_paths[u][path_cols] = 2
                    temp_cols[u] = cols[i]
                    temp_rows[u] = rows[i] + 1
                    temp_paths[u+1][path_cols] = 3
                    temp_cols[u+1] = cols[i] - 1
                    temp_rows[u+1] = rows[i]
                    # u = u + 2;
            elif mat1[rows[i]][cols[i]] == 3:
                # temp_paths[i] = 30;
                # temp_cols[u] = cols[i]
                # temp_rows[u] = rows[i]
                # row_filler(path_cols, i, 2, u);
                if paths[i][path_cols-1] == 3:
                    temp_paths[u][path_cols] = 0
                    temp_cols[u] = cols[i]
                    temp_rows[u] = rows[i] - 1
                    temp_paths[u+1][path_cols] = 3
                    temp_cols[u+1] = cols[i] - 1
                    temp_rows[u+1] = rows[i]
                elif paths[i][path_cols-1] == 1:
                    temp_paths[u][path_cols] = 0
                    temp_cols[u] = cols[i]
                    temp_rows[u] = rows[i] - 1
                    temp_paths[u+1][path_cols] = 1
                    temp_cols[u+1] = cols[i] + 1
                    temp_rows[u+1] = rows[i]
                    # u = u + 2
                elif paths[i][path_cols-1] == 2:
                    temp_paths[u][path_cols] = 1
                    temp_cols[u] = cols[i] + 1
                    temp_rows[u] = rows[i]
                    temp_paths[u+1][path_cols] = 3
                    temp_cols[u+1] = cols[i] - 1
                    temp_rows[u+1] = rows[i]
                    # u = u + 2
            
            elif mat1[rows[i]][cols[i]] == 4:
                # #new_paths[i] = 40;
                # #row_filler(path_cols, i, 2, u);
                if paths[i][path_cols-1] == 3:
                    temp_paths[u][path_cols] = 0
                    temp_cols[u] = cols[i]
                    temp_rows[u] = rows[i] - 1
                    temp_paths[u+1][path_cols] = 2
                    temp_cols[u+1] = cols[i]
                    temp_rows[u+1] = rows[i] + 1
                    # #u = u + 2
                elif paths[i][path_cols-1] == 0:
                    temp_paths[u][path_cols] = 0
                    temp_cols[u] = cols[i]
                    temp_rows[u] = rows[i] - 1
                    temp_paths[u+1][path_cols] = 1
                    temp_cols[u+1] = cols[i] + 1
                    temp_rows[u+1] = rows[i]
                    # #u = u + 2
                elif paths[i][path_cols-1] == 2:
                    temp_paths[u][path_cols] = 1
                    temp_cols[u] = cols[i] + 1
                    temp_rows[u] = rows[i]
                    temp_paths[u+1][path_cols] = 2
                    temp_cols[u+1] = cols[i]
                    temp_rows[u+1] = rows[i] + 1
                    # #u = u + 2
            u += 2
        elif mat1[rows[i]][cols[i]] == 9:
            for m in range(path_cols):
                temp_paths[u][m] = paths[i][m]
                temp_paths[u+1][m] = paths[i][m]
                temp_paths[u+2][m] = paths[i][m]
            new_paths_counter = new_paths_counter + 2
            if paths[i][path_cols-1] == 0:
                temp_paths[u][path_cols] = 0
                temp_cols[u] = cols[i]
                temp_rows[u] = rows[i] - 1
                temp_paths[u+1][path_cols] = 3
                temp_cols[u+1] = cols[i] - 1
                temp_rows[u+1] = rows[i]
                temp_paths[u+2][path_cols] = 1
                temp_cols[u+2] = cols[i] + 1
                temp_rows[u+2] = rows[i]
                # #u = u + 3
            elif paths[i][path_cols-1] == 1:
                temp_paths[u][path_cols] = 0
                temp_cols[u] = cols[i]
                temp_rows[u] = rows[i] - 1
                temp_paths[u+1][path_cols] = 1
                temp_cols[u+1] = cols[i] + 1
                temp_rows[u+1] = rows[i]
                temp_paths[u+2][path_cols] = 2
                temp_cols[u+2] = cols[i]
                temp_rows[u+2] = rows[i] + 1
                # #u = u + 3
            elif paths[i][path_cols-1] == 2:
                temp_paths[u][path_cols] = 1
                temp_cols[u] = cols[i] + 1
                temp_rows[u] = rows[i]
                temp_paths[u+1][path_cols] = 3
                temp_cols[u+1] = cols[i] - 1
                temp_rows[u+1] = rows[i]
                temp_paths[u+2][path_cols] = 2
                temp_cols[u+2] = cols[i]
                temp_rows[u+2] = rows[i] + 1
                # u = u + 3;
            elif paths[i][path_cols-1] == 3:
                temp_paths[u][path_cols] = 0
                temp_cols[u] = cols[i]
                temp_rows[u] = rows[i] - 1
                temp_paths[u+1][path_cols] = 3
                temp_cols[u+1] = cols[i] - 1
                temp_rows[u+1] = rows[i]
                temp_paths[u+2][path_cols] = 2
                temp_cols[u+2] = cols[i]
                temp_rows[u+2] = rows[i] + 1
                # #u = u + 3                          
            u += 3
    return [temp_paths, temp_rows, temp_cols, new_paths_counter]

def make_new_array(direction, mat1):
    r = len(mat1)
    c = len(mat1[0])
    
    if direction == 'N':
        mat = [['D' for x in range(c)] for y in range(r+1)]
        for i in range(r):
            for j in range(c):
                mat[i+1][j] = mat1[i][j]
                
    elif direction == 'S':
        mat = [['D' for x in range(c)] for y in range(r+1)]
        for i in range(r):
            for j in range(c):
                mat[i][j] = mat1[i][j]
                
    elif direction == 'E':
        mat = [['D' for x in range(c+1)] for y in range(r)]
        for i in range(r):
            for j in range(c):
                mat[i][j] = mat1[i][j]
        ##print mat1
        ##print mat                
               
    elif direction == 'W':
        mat = [['D' for x in range(c+1)] for y in range(r)]
        for i in range(r):
            for j in range(c):
                mat[i][j+1] = mat1[i][j]
                
    return mat
def total_paths_counter(mat1, paths, rows, cols, afv):
    counter = 0
    path_rows = len(paths)
    path_cols = len(paths[0])
    for i in range(path_rows):
        if paths[i][path_cols-1] == 5:
            continue
        elif mat1[rows[i]][cols[i]] == 0 or mat1[rows[i]][cols[i]] == 5 or mat1[rows[i]][cols[i]] == 6 or mat1[rows[i]][cols[i]] == 7 or mat1[rows[i]][cols[i]] == 8:
            continue
        elif mat1[rows[i]][cols[i]] == 1 or mat1[rows[i]][cols[i]] == 2 or mat1[rows[i]][cols[i]] == 3 or mat1[rows[i]][cols[i]] == 4:
            counter = counter + 1
        elif mat1[rows[i]][cols[i]] == 9:
            counter = counter + 2
    
    return counter + len(paths)

def all_good_values(map):
    c = 0
    for l in range(16):
        for m in range(16):
            if map[l][m] == 1:
                c = c + 1
    
    print "Number of iterations to happen: ", c
    i = 0
    good_vals = [[0 for x in range(4)] for y in range(c)]
    print "VAG: ", good_vals
    for x in range(16):
        for y in range(16):
            if map[x][y] == 1:
                good_vals[i][0] = x
                good_vals[i][1] = y
                i = i + 1
    for r in range(len(good_vals)):
        if (good_vals[r][0] == 7) or (good_vals[r][0] == 8):
            row = 7
        if (good_vals[r][0] == 6) or (good_vals[r][0] == 9):
            row = 6
        if (good_vals[r][0] == 5) or (good_vals[r][0] == 10):
            row = 5
        if (good_vals[r][0] == 4) or (good_vals[r][0] == 11):
            row = 4
        if (good_vals[r][0] == 3) or (good_vals[r][0] == 12):
            row = 3
        if (good_vals[r][0] == 2) or (good_vals[r][0] == 13):
            row = 2
        if (good_vals[r][0] == 1) or (good_vals[r][0] == 14):
            row = 1
        if (good_vals[r][0] == 0) or (good_vals[r][0] == 15):
            row = 0
        if (good_vals[r][1] == 7) or (good_vals[r][1] == 8):
            col = 7
        if (good_vals[r][1] == 6) or (good_vals[r][1] == 9):
            col = 6
        if (good_vals[r][1] == 5) or (good_vals[r][1] == 10):
            col = 5
        if (good_vals[r][1] == 4) or (good_vals[r][1] == 11):
            col = 4
        if (good_vals[r][1] == 3) or (good_vals[r][1] == 12):
            col = 3
        if (good_vals[r][1] == 2) or (good_vals[r][1] == 13):
            col = 2
        if (good_vals[r][1] == 1) or (good_vals[r][1] == 14):
            col = 1
        if (good_vals[r][1] == 0) or (good_vals[r][1] == 15):
            col = 0
        perc = math.sqrt(((float(row)**2)+(float(col)**2)))
        good_vals[r][2] = perc
        new_list = sorted(good_vals, key=lambda x: x[2])
    return new_list
                