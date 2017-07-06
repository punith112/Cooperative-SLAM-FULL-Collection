'''
Created on Mar 13, 2017

@author: rjw0028
'''
import xlwt

good_vals = [[0, 0, 5.5, 164], [0, 0, 2.3, 157], [0, 0, 0.9, 188], [0, 0, 55.2, 159], [0, 0, 0.001, 176]]
new_list = sorted(good_vals, key=lambda x: x[2])
print good_vals
print new_list

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
    ws.write(p+1, 0, new_agv[i][0])
    ws.write(p+1, 1, new_agv[i][1])
    ws.write(p+1, 2, new_agv[i][2])
    ws.write(p+1, 3, new_agv[i][3])  
    
wb.save("Data1Rob.xls")