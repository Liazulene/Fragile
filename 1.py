import os
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rcParams
config = {
    "font.family":'Arial',  # 设置字体类型
    "axes.unicode_minus": False  #解决负号无法显示的问题
}
rcParams.update(config)

# 文件目录路径
directory = r'C:\Users\Liazulene\Desktop\ElectrochemicalTest\LA044\044-5'

final_list=[]
Cp_list=[]
Cpdraw_list=[]

txt_files = [file for file in os.listdir(directory) if file.startswith('GCD-') and file.endswith('c.txt') ]

for txt_file in txt_files:
    file_path = os.path.join(directory, txt_file)
    # 解析文件名中的扫描速率
    specific_current = int(txt_file.split('GCD-')[1].split('_')[0])/10  
    cycle_number = int(txt_file.split('_')[1].split('c')[0])
    coordinates = []

    with open(file_path, 'r') as file:
        # 跳过无效行
        line = file.readline().strip()
        while not line.startswith('Time/sec'):
            line = file.readline().strip()
        
        for line in file:
                if line.startswith('Summary:'):
                    break  # 遇到无效数据的开头，跳出循环
            # 移除行末的换行符并使用逗号分隔符分割行
                parts = line.strip().split(',')
            
            # 确保每行包含的数据量正确
                if len(parts) == 10:
                # 将前四个数据转换为浮点数，并创建坐标点
                    try:
                        time = float(parts[0])
                        potential = float(parts[1])
                        step = float(parts[2])
                        cycle = float(parts[3])
                        coordinate = (time, potential, step, cycle)
                        coordinates.append(coordinate)
                    except ValueError:
                        print(f"无法解析行：{line}")

    # 创建一个矩阵用来存储数据，这个矩阵具有5行，
    # 第一行是cycle的值，第二行是这个cycle中time的最小值，
    # 第三行是这个cycle中potential达到最大值时的time值，
    # 第四行是这个cycle中time的最大值，第五行是这个cycle中Potential的最值的差
    # 行数a = 5，列数rows是cycle的数量
    a = 5 
    rows = int(max(coordinate[3] for coordinate in coordinates))
    matrix = [[0 for i in range(rows)] for j in range(a)]
    for i in range(rows):
        matrix[0][i] = i + 1


    # 创建一个字典用于存储每个不同step值对应的最大和最小time值
    cycle_time_data = {}

    # 遍历coordinates列表
    for coordinate in coordinates:
        cycle_value = coordinate[3]
        time_value = coordinate[0]

        if cycle_value not in cycle_time_data:
            # 如果step值不在字典中，添加一个新的条目
            cycle_time_data[cycle_value] = {'max_time': time_value, 'min_time': time_value}
        else:
            # 更新字典中的max_time和min_time值
            cycle_time_data[cycle_value]['max_time'] = max(cycle_time_data[cycle_value]['max_time'], time_value)
            cycle_time_data[cycle_value]['min_time'] = min(cycle_time_data[cycle_value]['min_time'], time_value)

    # 遍历字典并输出结果
    for cycle_value, time_values in cycle_time_data.items():
        max_time = time_values['max_time']
        min_time = time_values['min_time']
        for i in range(rows):
            if cycle_value ==  matrix[0][i]:
                matrix[1][i] = min_time
                matrix[3][i] = max_time

    # 创建一个字典用于存储cycle值对应的time和potential
    cycle_time_potential = {}  

    # 遍历coordinates列表
    for coordinate in coordinates:
        cycle_value = coordinate[3]
        time_value = coordinate[0]
        potential_value = coordinate[1]

        if cycle_value not in cycle_time_potential:
            # 如果cycle值不在字典中，添加一个新的条目
            cycle_time_potential[cycle_value] = {'time': time_value, 'potential': potential_value}
        else:
            # 检查当前potential是否大于字典中的potential
            if potential_value > cycle_time_potential[cycle_value]['potential']:
                cycle_time_potential[cycle_value] = {'time': time_value, 'potential': potential_value}

    # 遍历字典并输出结果
    for cycle_value, values in cycle_time_potential.items():
        max_potential_time = values['time']
        max_potential = values['potential']
        for i in range(rows):
            if cycle_value ==  matrix[0][i]:
                matrix[2][i] = max_potential_time

    # 创建一个字典用于存储cycle值对应的potential的最大值和最小值
    cycle_potential = {}  

    # 遍历coordinates列表
    for coordinate in coordinates:
        cycle_value = coordinate[3]
        potential_value = coordinate[1]

        if cycle_value not in cycle_potential:
            # 如果cycle值不在字典中，添加一个新的条目
            cycle_potential[cycle_value] = {'max_potential': potential_value, 'min_potential': potential_value}
        else:
            # 检查当前potential是否大于字典中的max_potential
            if potential_value > cycle_potential[cycle_value]['max_potential']:
                cycle_potential[cycle_value]['max_potential'] = potential_value
            # 检查当前potential是否小于字典中的min_potential
            if potential_value < cycle_potential[cycle_value]['min_potential']:
                cycle_potential[cycle_value]['min_potential'] = potential_value

    # 计算并输出差值
    cycle_differences = {}  # 存储每个cycle的最大和最小potential差值
    for cycle_value, values in cycle_potential.items():
        max_potential = values['max_potential']
        min_potential = values['min_potential']
        difference = max_potential - min_potential
        cycle_differences[cycle_value] = difference

    # 遍历差值字典并输出结果
    for cycle_value, difference in cycle_differences.items():
        for i in range(rows):
            if cycle_value ==  matrix[0][i]:
                matrix[4][i] = difference

    matrix = [row[1:-1] for row in matrix]
    matrix[0] = [x - 1 for x in matrix[0]]

    # 计算比电容，为矩阵的第六行
    Cp = []

    for col_index in range(len(matrix[0])):
        numerator = matrix[3][col_index] - matrix[2][col_index]
        denominator = matrix[4][col_index]
        
        # 防止除以0错误
        if denominator != 0:
            result = specific_current * numerator / denominator
        else:
            result = None
        
        # 添加结果到新行
        Cp.append(result)
    matrix.append(Cp)


    CE = []

    for col_index in range(len(matrix[0])):
        numerator = matrix[3][col_index] - matrix[2][col_index]
        denominator = matrix[2][col_index] - matrix[1][col_index]
        
        # 防止除以0错误
        if denominator != 0:
            result = specific_current * numerator / denominator
        else:
            result = None
        
        # 添加结果到新行
        CE.append(result)

    # print(CE)
    matrix.append(CE)

    # 计算平均放电比电容
    Cp_average = sum(matrix[5][1:])/len(matrix[5][1:])


    #计算电容保持率，作为第八行，计算最终电容保持率
    row_index = 5
    row_to_modify = matrix[row_index]
    first_element = row_to_modify[0]
    CR = [x / first_element for x in row_to_modify]
    matrix.append(CR)

    CR_final = 100*matrix[7][-1]



    #计算平均库仑效率
    CE_average = 100*sum(matrix[6][1:])/len(matrix[6][1:])


    #计算充电比电容与平均充电比电容
    Cpn = []

    for col_index in range(len(matrix[0])):
        numerator = matrix[2][col_index] - matrix[1][col_index]
        denominator = matrix[4][col_index]
        
        # 防止除以0错误
        if denominator != 0:
            result = specific_current * numerator / denominator
        else:
            result = None
        
        # 添加结果到新行
        Cpn.append(result)

    matrix.append(Cpn)
    Cp_first5 = sum(matrix[5][:5])/len(matrix[5][:5])
    Cp_final5 = sum(matrix[5][-5:])/len(matrix[5][-5:])
    capacitance_retention = Cp_final5/Cp_first5 *100
    k2 = (cycle_number, specific_current, Cp_first5, Cp_final5, capacitance_retention)
    combined_list = [cycle_number, Cp]
    final_list.append(k2)
    Cp_list.append(combined_list)

final_array = np.array(final_list)

sorted_indices = np.argsort(final_array[:, 0])
sorted_scan_list = final_array[sorted_indices]

# 提取排序后的 Sc 和 Cp 值
sorted_number = sorted_scan_list[:, 0]
sorted_sc = sorted_scan_list[:, 1]
sorted_Cpn = sorted_scan_list[:, 2]
sorted_Cp = sorted_scan_list[:, 3]
sorted_CR = sorted_scan_list[:, 4]

for num, k, Cpn, Cp ,CR in zip(sorted_number, sorted_sc, sorted_Cpn, sorted_Cp, sorted_CR):
    print("Cycle number:", num, "Specific Current:", k, "A/g", "\t Cp_first5: {:.2f}".format(Cpn), "F/g", "\t Cp_final5: {:.2f}".format(Cp),"F/g", "\t  Capacitance retention: {:.2f}".format(CR), "%")

Cp_list_sorted = sorted(Cp_list, key=lambda x: x[0])
merged_Cp_list = []
for _, Cp_list in Cp_list_sorted:
    merged_Cp_list.extend(Cp_list)

x = len(merged_Cp_list)
x_values = list(range(1, x + 1))

# 绘制图表
plt.plot(x_values, merged_Cp_list)  # 使用圆圈标记
plt.xlabel('Cycle Number')
plt.ylabel('$\mathrm{C_p (F/g)}$')
plt.title('Plot of Cp_list')
plt.xlim((0, 10000))
plt.ylim((0, 450))
plt.grid(False)  # 添加网格线
plt.show()
