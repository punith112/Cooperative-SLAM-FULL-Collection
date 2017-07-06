'''
Created on Mar 13, 2017

@author: Rajish
'''

global occ
occ = 0
from copy import deepcopy
#comp_var = 4    #or any other user defined value to determine the comparable window size
#user_match_perc = 80.00 #get this from user. This decides the allowable percentage for matching

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



def compare(a,b):       #function to compare two square matrices of the same size. The length is found out and then the for loops are run accordingly
    good = 0
    no_match = 0
    c = len(a)
    for i in range(c):
        for j in range(c):
            if no_match == 1:
                break
            if (((a[i][j] == b[i][j]) and (a[i][j] != 'C')) and ((a[i][j] == b[i][j]) and (a[i][j] !='B'))):
                good += 1
            elif ((a[i][j] == b[i][j]) and ((a[i][j] == 'C') or (a[i][j] =='B'))):
                continue
            else :
                if (a[i][j] == 'C') or (b[i][j] == 'C'):
                    continue
                elif (((b[i][j] == 'A') and (a[i][j] != 'C')) or ((a[i][j] == 'A') and (b[i][j] != 'C'))):
                    no_match = 1
                elif (a[i][j] == 'B')  or (b[i][j] == 'B'):
                    continue
                else:
                    no_match = 1
    if no_match == 1:
        match_perc = -1.0
    else:
        match_perc = (100*good)/(float(c**2))
    return match_perc

#a = [['C','B','C','C','C'],['A','0','A','A','A'],['2','0','0','0','4'],['C','B','A','A','0'],['C','C','0','0','7']]
#b = [['B','C','C','C','C'],['A','0','A','A','C'],['2','0','0','0','4'],['B','2','A','A','0'],['C','A','0','0','7']]
#compare(a,b)

def matching (mat1, mat2, comp_var, user_match_perc) :   #finds percentage of matching and stores in a 4D matrix. 
    a = len(mat1)       #Number of rows in mat1
    b = len(mat1[0])    #Number of cols in mat1
    c = len(mat2)       #Number of rows in mat2
    d = len(mat2[0])    #Number of cols in mat2
    #match_perc = 0
    count = 0
    mas = [0,[mat1, mat2, [0,0,0,0]]]
    high = 0.0
    
    lst = [a,b,c,d]
    mini = min(lst)
    #print 'mini = ', mini
    if mini<comp_var :
        #print 'These maps are not comparable yet...'
        return [0, mas]   # This function returns the result and updated/non-updated versions of the two maps compared...
    else:
        a1 = a - comp_var - 1
        b1 = b - comp_var - 1
        c1 = c - comp_var - 1
        d1 = d - comp_var - 1
        #print a1
        #print b1
        #print c1
        #print d1
        match_perc = [[[[0.0 for x in range(d1)] for y in range(c1)]for w in range(b1)]for z in range(a1)]
        ##print match_perc
        
        for i in range(a1):
            ##print 'a1'
            for j in range(b1):
                ##print 'b1'
                for k in range(c1):
                    ##print 'c1'
                    for l in range(d1):
                        ##print 'high = ', high
                        m1 = create_matrix(i, j, mat1, comp_var)
                        m2 = create_matrix(k, l, mat2, comp_var)
                        ##print m1
                        ##print m2
                        match_perc[i][j][k][l] = compare(m1, m2)
                        ##print 'match_perc = ', match_perc[i][j][k][l]
                        if match_perc[i][j][k][l] == 100.0:
                            ##print '100.00 percent match'
                            count = count + 1
                            high = 100.0
                            s = i
                            t = j
                            u = k
                            v = l
                        elif match_perc[i][j][k][l] > high:
                            ##print 'ELif loop for match_perc = ', match_perc[i][j][k][l]
                            high = match_perc[i][j][k][l]
                            ##print 'high just after update = ', high
                            s = i
                            t = j
                            u = k
                            v = l
                            major1 = m1
                            major2 = m2
                            
    if high > user_match_perc :       #user_match_perc is a user defined value that defines the acceptable number
        #print 's', s
        #print 't', t
        #print 'u', u
        #print 'v', v
        #print 'm1', major1
        #print 'm2', major2
        mas = map_merge(s, t, u, v, mat1, mat2, comp_var)
    else:
        return [0, mas[1]]
    
    if mas[0] == 0:
        return [0, mas[1]]
    else:
        return [1, mas[1]] 
        
        
def map_merge(a, b, c, d, mat1, mat2, comp_var):
    # orient = 0          #orientation of the robot towards north
    deal = 1
    m1_row_high = len(mat1)
    m1_col_high = len(mat1[0])
    m2_row_high = len(mat2)
    m2_col_high = len(mat2[0])
        
    mat1_rontop = a
    mat1_ronbot = m1_row_high - a - comp_var       #// These variables will be needed further_ For mat1, Rows below our 4x4 matching part_
    mat1_conlef = b                          # // These variables will be needed further_ For mat1, Columns to the left of out 4x4 matching part_
    mat1_conrig = m1_col_high - b - comp_var    
    
    mat2_rontop = c
    mat2_ronbot = m2_row_high - c - comp_var       #// These variables will be needed further_ For mat1, Rows below our 4x4 matching part_
    mat2_conlef = d                         #  // These variables will be needed further_ For mat1, Columns to the left of out 4x4 matching part_
    mat2_conrig = m2_col_high - d - comp_var   
    
    mat1_rtoaddontop = mat2_rontop - mat1_rontop    #// As the name suggests, number of rows to be added on top of mat1    
    mat1_rtoaddonbot = mat2_ronbot - mat1_ronbot    #// As the name suggests, number of rows to be added at bottom of mat1
    mat1_ctoaddonlef = mat2_conlef - mat1_conlef    #// As the name suggests, ____
    mat1_ctoaddonrig = mat2_conrig - mat1_conrig    #// As the name suggests, 
                                                 
    mat2_rtoaddontop = mat1_rontop - mat2_rontop    #// As the name suggests, number of rows to be added on top of mat2
    mat2_rtoaddonbot = mat1_ronbot - mat2_ronbot    #// As the name suggests, number of rows to be added at bottom of mat2
    mat2_ctoaddonlef = mat1_conlef - mat2_conlef    #// As the name suggests, 
    mat2_ctoaddonrig = mat1_conrig - mat2_conrig    #// As the name suggests,
    
    if mat1_rtoaddontop < 0:
        mat1_rtoaddontop = 0
    if mat1_rtoaddonbot < 0:
        mat1_rtoaddonbot = 0
    if mat1_ctoaddonlef < 0:
        mat1_ctoaddonlef = 0
    if mat1_ctoaddonrig < 0:
        mat1_ctoaddonrig = 0
        
    if mat2_rtoaddontop < 0:
        mat2_rtoaddontop = 0
    if mat2_rtoaddonbot < 0:
        mat2_rtoaddonbot = 0
    if mat2_ctoaddonlef < 0:
        mat2_ctoaddonlef = 0
    if mat2_ctoaddonrig < 0:
        mat2_ctoaddonrig = 0
    
    new_a = a + mat1_rtoaddontop       #//new_a, new_b are the index of our 4x4 matching part's 1st element in the new matrix we will make next_
    new_b = b + mat1_ctoaddonlef
    new_c = c + mat2_rtoaddontop
    new_d = d + mat2_ctoaddonlef
    
    n = new_a - a
    m = new_b - b
    v = new_c - c
    w = new_d - d
    
    if (new_a != new_c) or (new_b != new_d):
        print 'a and c, and, b and d, are not equal_ Something went wrong___'
    
          
    p = m1_row_high + mat1_rtoaddontop + mat1_rtoaddonbot     #//calculating rows and columns for the new matrices_
    q = m1_col_high + mat1_ctoaddonlef + mat1_ctoaddonrig
    r = m2_row_high + mat2_rtoaddontop + mat2_rtoaddonbot
    s = m2_col_high + mat2_ctoaddonlef + mat2_ctoaddonrig
    
    if (p > 18) or (q > 18) or (r > 18) or (s > 18):
        deal = 0
        return [deal, [[], [], [], new_a, new_b]]
    
    #xmat1 = [[0,0],[0,0]]
    #xmat2 = [[0,0],[0,0]]
    xmat1 = [['D' for x in range(q)] for y in range(p)]
    xmat2 = [['D' for x in range(s)] for y in range(r)]
            
    for i in range(m1_row_high):
        for j in range(m1_col_high):
            xmat1[n+i][m+j] = mat1[i][j]
    
    for i in range(m2_row_high):
        for j in range(m2_col_high):
            xmat2[v+i][w+j] = mat2[i][j]
            
    try:   
        for i in range(len(xmat1)):
            for j in range(len(xmat1[0])):
                if xmat1[i][j] == 'D' or xmat1[i][j] == 'C':  #or xmat1[i][j] == 'B':
                    xmat1[i][j] = xmat2[i][j]
                elif xmat2[i][j] == 'D' or xmat2[i][j] == 'C': # or xmat2[i][j] == 'B':
                    xmat2[i][j] = xmat1[i][j]
                elif xmat1[i][j] == 'B':
                    xmat1[i][j] = xmat2[i][j]
                elif xmat2[i][j] == 'B':
                    xmat2[i][j] = xmat1[i][j]
                elif xmat1[i][j] != xmat2[i][j]:
                    deal = 0
                    print "Some value doesn't match. Error!!!!!!!!!!!!!"
                    print "Wrong value is xmat1: ", xmat1[i][j]
                    print "Wrong value is xmat2: ", xmat2[i][j]
                    print i, " , " , j
                    raise StopIteration
    except StopIteration: pass
            
    
    print xmat1
    print xmat2
    
    for i in range(r):
        for j in range(s):
            if xmat1[i][j] == 'D':
                xmat1[i][j] = 'C'
            if xmat2[i][j] == 'D':
                xmat2[i][j] = 'C'
    print "Deal = ", deal
    added_rows_and_cols = [mat1_rtoaddontop, mat1_ctoaddonlef, mat2_rtoaddontop, mat2_ctoaddonlef]
#     if xmat1 != xmat2:
#         print 'They are not equal after map_merge. Something wrong'
    
    return [deal, [xmat1, xmat2, added_rows_and_cols, new_a, new_b]]

def create_matrix(r, c, m, comp_var):
    matrix = [[0 for x in range(comp_var)] for y in range(comp_var)]
    #matrix = [[0,0],[0,0]]      # This needs to be defined in the new way learnt....
    for raj in range(comp_var):
        for wag in range(comp_var):
            matrix[raj][wag] = m[r+raj][c+wag]
    return matrix


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

# End on first_map_update - function...

# def adj_field_value(row_cp_map, col_cp_map, real_map):  # Change the attributes where we call this function.
#     afv = [0,0,0,0]
#     if real_map[row_cp_map - 1][col_cp_map] == 1:
#         afv[0] = 1
#     if real_map[row_cp_map][col_cp_map + 1] == 1:
#         afv[1] = 1
#     if real_map[row_cp_map + 1][col_cp_map] == 1:
#         afv[2] = 1
#     if real_map[row_cp_map][col_cp_map - 1] == 1:
#         afv[3] = 1
#     return afv
# 
# tup = mat1, row_cp_local1, col_cp_local1, mat2, row_cp_local2, col_cp_local2, p3, row_cp_local3, col_cp_local3
def get_level(mat1, r1, c1, mat2, r2, c2, mat3, r3, c3, mat4, r4, c4, mat5, r5, c5):
    
    emms1 = deepcopy(mat1)
    emms2 = deepcopy(mat2)
    emms3 = deepcopy(mat3)
    emms4 = deepcopy(mat4)
    emms5 = deepcopy(mat5)
    
    emms1[r1][c1] = 'R1'
    emms2[r2][c2] = 'R2'
    emms3[r3][c3] = 'R3'
    emms4[r4][c4] = 'R4'
    emms5[r5][c5] = 'R5'
    
    return [emms1, emms2, emms3, emms4, emms5]
    
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

afv = [1,1,0,0]

    
b_spot = 0

# # Testingwork
#         if (mat1[rl-1][cl] == 'B') and (mat1[rl][cl+1] == 'B') and (mat1[rl+1][cl] == 'B') and (mat1[rl][cl-1] == 'B'):
#             for i in range(4):
#                 if orient == i:
#                     answer = minus_1(i)
#         elif (mat1[rl-1][cl] == 'B') and (mat1[rl][cl+1] == 'B') and (mat1[rl+1][cl] == 'B'):
#             answer = 0
#         elif (mat1[rl-1][cl] == 'B') and (mat1[rl][cl+1] == 'B') and (mat1[rl][cl-1] == 'B'):
#             answer = 3
#         elif (mat1[rl-1][cl] == 'B') and (mat1[rl+1][cl] == 'B') and (mat1[rl][cl-1] == 'B'):
#             answer = 2
#         elif (mat1[rl][cl+1] == 'B') and (mat1[rl+1][cl] == 'B') and (mat1[rl][cl-1] == 'B'):
#             answer = 1
#         elif (mat1[rl-1][cl] == 'B') and (mat1[rl][cl+1] == 'B'):
#             answer = 0
#         elif (mat1[rl-1][cl] == 'B') and (mat1[rl+1][cl] == 'B'):
#             if (orient == 1) or (orient == 0):
#                 answer = 0
#             else:
#                 answer = 2
#         elif (mat1[rl-1][cl] == 'B') and (mat1[rl][cl-1] == 'B'):
#             answer = 3
#         elif (mat1[rl][cl+1] == 'B') and (mat1[rl+1][cl] == 'B'):
#             answer = 1
#         elif (mat1[rl][cl+1] == 'B') and (mat1[rl][cl-1] == 'B'):
#             if (orient == 2) or (orient == 1):
#                 answer = 1
#             else:
#                 answer = 3
#         elif (mat1[rl+1][cl] == 'B') and (mat1[rl][cl-1] == 'B'):
#             answer = 2
#         elif (mat1[rl-1][cl] == 'B'):
#             answer = 0
#         elif (mat1[rl+1][cl] == 'B'):
#             answer = 2
#         elif (mat1[rl][cl-1] == 'B'):
#             answer = 3
#         elif (mat1[rl][cl+1] == 'B'):
#             answer = 1
#     
# 
# 
# #
def motion_deciding_function(mat1, orient, rl, cl, afv ):
    if (mat1[rl-1][cl] == 'B') or (mat1[rl+1][cl] == 'B') or (mat1[rl][cl - 1] == 'B') or (mat1[rl][cl+1] == 'B'):
        if (mat1[rl-1][cl] == 'B') and (mat1[rl][cl+1] == 'B') and (mat1[rl+1][cl] == 'B') and (mat1[rl][cl-1] == 'B'):
            for i in range(4):
                if orient == i:
                    answer = minus_1(i)
        elif (mat1[rl-1][cl] == 'B') and (mat1[rl][cl+1] == 'B') and (mat1[rl+1][cl] == 'B'):
            answer = 0
        elif (mat1[rl-1][cl] == 'B') and (mat1[rl][cl+1] == 'B') and (mat1[rl][cl-1] == 'B'):
            answer = 3
        elif (mat1[rl-1][cl] == 'B') and (mat1[rl+1][cl] == 'B') and (mat1[rl][cl-1] == 'B'):
            answer = 2
        elif (mat1[rl][cl+1] == 'B') and (mat1[rl+1][cl] == 'B') and (mat1[rl][cl-1] == 'B'):
            answer = 1
        elif (mat1[rl-1][cl] == 'B') and (mat1[rl][cl+1] == 'B'):
            answer = 0
        elif (mat1[rl-1][cl] == 'B') and (mat1[rl+1][cl] == 'B'):
            if (orient == 1) or (orient == 0):
                answer = 0
            else:
                answer = 2
        elif (mat1[rl-1][cl] == 'B') and (mat1[rl][cl-1] == 'B'):
            answer = 3
        elif (mat1[rl][cl+1] == 'B') and (mat1[rl+1][cl] == 'B'):
            answer = 1
        elif (mat1[rl][cl+1] == 'B') and (mat1[rl][cl-1] == 'B'):
            if (orient == 2) or (orient == 1):
                answer = 1
            else:
                answer = 3
        elif (mat1[rl+1][cl] == 'B') and (mat1[rl][cl-1] == 'B'):
            answer = 2
        elif (mat1[rl-1][cl] == 'B'):
            answer = 0
        elif (mat1[rl+1][cl] == 'B'):
            answer = 2
        elif (mat1[rl][cl-1] == 'B'):
            answer = 3
        elif (mat1[rl][cl+1] == 'B'):
            answer = 1
        return answer
    else:
        # Now this is a dead-end situation...
        imagine = function_to_start_imaginary(mat1, rl, cl, afv)
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
            
            #print 'paths = ', paths
            #print 'rows = ', rows
            #print 'cols = ', cols
            #raw_input("This is while loop to find distant B")
    #Old function for reference
    #if (mat1[row_cp_local-1][col_cp_local] == 'B') or (mat1[row_cp_local+1][col_cp_local] == 'B') or (mat1[row_cp_local][col_cp_local - 1] == 'B') or (mat1[row_cp_local][col_cp_local+1] == 'B'):
    #    for i in range(4):
    #        if orient == i:
    #            answer = minus_1(i)
    #            if afv[answer] != 1:    # afv is a variable in main, that stores the values of adjacent fields of the current position
    #                answer = i
    #                if afv[answer] != 1:
    #                    answer = plus_1(i)
    #                    if afv[answer] != 1:
    #                        answer = plus_1(answer)
    #    return answer
    #else:
    #    # Now this is a dead-end situation...
    #    if ((b_spot == 1) and step!=(path_cols-1)):
    #        answer = route[step]
    #        step = step + 1
    #        return answer
    #    no_b = 0
    #    # mat1, row_cp_local, col_cp_local, afv
    #    imagine = function_to_start_imaginary(mat1, row_cp_local, col_cp_local, afv)
    #    # imagine has [paths, rows, cols]
    #    paths = imagine[0]
    #    rows = imagine[1]
    #    cols = imagine[2]
    #    path_rows = len(rows)
    #    path_cols = len(paths[0])
    #    
    #            
    #    for i in range(path_rows):
    #        if mat1[rows[i]][cols[i]] == 'B':
    #            # Go to this B
    #            route = [9 for x in range(path_cols)]
    #            for t in range(path_cols):
    #                route[t] = paths[i][t]
    #            b_spot = 1      # to remember that b has been spotted. But doesn't look like its useful.
    #            answer = route[0]
    #            return answer
    #        else:
    #            no_b = 111
    #    if no_b == 111:
    #        u = func_to_add_one_step()
    #        paths = u[0]
    #        rows = u[1]
    #        cols = u[2]
    #        new_paths_added = u[3]
    #        #print 'New paths added this time = %d', new_paths_added
    #        path_rows = len(paths)
    #        path_cols = len(paths[0])


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

#Function to add one step ends here...

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



def var_update(mat, row_next_pos, col_next_pos, row_cp_map, col_cp_map, row_cp_local, col_cp_local, orient, fv, afv):
    #global row_cp_map, col_cp_map, row_cp_local, col_cp_local, orient    # Remove these variables from the parameters list of this function after testing is done
    mat_row_low = 0
    mat_col_low = 0
    mat_row_high = len(mat)
    mat_col_high = len(mat[0])
    incor = ' '
    
    ##print 'mat[row_cp_local][col_cp_local+1] = ', mat[row_cp_local][col_cp_local+1]
    if row_next_pos == mat_row_low:     # This part is when the robot has reached the edge of the current map
        mat_new = make_new_array('N', mat)    # after this there will be virtual movement by the robot_ That is we change it's variables___
        ##row_cp_local = row_cp_local;       we can convert such lines which do not change the variable into comments___
        ##col_cp_local = col_cp_local;
        #row_cp_map = row_cp_map - 1
        ##col_cp_map = col_cp_map;
        orient = 0
        incor = 'N'
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
        incor = 'W'
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
                
    
    return [mat_new, row_next_pos, col_next_pos, row_cp_map, col_cp_map, row_cp_local, col_cp_local, orient, incor]

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
                
    i = 0
    good_vals = [[0 for x in range(2)] for y in range(c)]
    for x in range(16):
        for y in range(16):
            if map[x][y] == 1:
                good_vals[i][0] = x
                good_vals[i][1] = y
                i = i + 1
    return good_vals


