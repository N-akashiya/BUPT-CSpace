import os
import jsonlines
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

city_names = ['bj', 'sh', 'gz', 'sz', 'su']
city_labels = {
    'bj': '北京',
    'sh': '上海',
    'gz': '广州',
    'sz': '深圳',
    'su': '苏州'
}
orientation_labels = ['东', '南', '西', '北', '东南', '西南', '东北', '西北']

input_dir = 'cleandata'
output_dir = '4'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for city in city_names:
    input_file = os.path.join(input_dir, f'{city}-data.json')
    data = []

    with jsonlines.open(input_file, mode='r') as reader:
        for obj in reader:
            data.append(obj)

    # 计算每个朝向的单位面积租金
    orientation_rentals = {orientation: [] for orientation in orientation_labels}
    for item in data:
        orientation = item.get('orien')
        rental = item.get('rental')
        area = item.get('area')
        if orientation and rental and area:
            unit_rental = rental / area
            if orientation in orientation_rentals:
                orientation_rentals[orientation].append(unit_rental)

    # 绘制箱线图
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    data_to_plot = [orientation_rentals[orientation] for orientation in orientation_labels]
    ax.boxplot(data_to_plot, labels=orientation_labels)
    ax.set_xlabel('朝向')
    ax.set_ylabel('单位面积租金（元/平方米/月）')
    ax.set_title(f'{city_labels[city]}不同朝向的单位面积租金分布')

    # 保存
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{city}_4.png'), dpi=300)

# 分析结果
for city in city_names:
    input_file = os.path.join(input_dir, f'{city}-data.json')
    data = []

    with jsonlines.open(input_file, mode='r') as reader:
        for obj in reader:
            data.append(obj)

    orientation_rentals = {orientation: [] for orientation in orientation_labels}
    for item in data:
        orientation = item.get('orien')
        rental = item.get('rental')
        area = item.get('area')
        if orientation and rental and area:
            unit_rental = rental / area
            if orientation in orientation_rentals:
                orientation_rentals[orientation].append(unit_rental)

    avg_rentals = {orientation: np.mean(rentals) for orientation, rentals in orientation_rentals.items() if rentals}
    sorted_avg_rentals = sorted(avg_rentals.items(), key=lambda x: x[1], reverse=True)
    highest_orientation = sorted_avg_rentals[0]
    lowest_orientation = sorted_avg_rentals[-1]

    print(f'{city_labels[city]}:')
    for orientation, avg_rental in sorted_avg_rentals:
        print(f'{orientation} ', end='')
    print()
    print(f'最高: {highest_orientation[0]}, 平均单位面积租金: {highest_orientation[1]:.2f} 元/平方米/月')
    print(f'最低: {lowest_orientation[0]}, 平均单位面积租金: {lowest_orientation[1]:.2f} 元/平方米/月')
