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
house_type_labels = {
    '1b': '一居',
    '2b': '二居',
    '3b': '三居'
}

input_dir = 'cleandata'
output_dir = '2'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

statistics = {}

for city in city_names:
    input_file = os.path.join(input_dir, f'{city}-data.json')
    data = []

    with jsonlines.open(input_file, mode='r') as reader:
        for obj in reader:
            data.append(obj)

    # 筛选一居、二居、三居数据
    rental_1b = [] 
    rental_2b = [] 
    rental_3b = []

    for item in data:
        if item.get('house_type'):
            house_type = item['house_type']
            rental = item['rental']
            if '1室' in house_type:
                rental_1b.append(rental)
            elif '2室' in house_type:
                rental_2b.append(rental)
            elif '3室' in house_type:
                rental_3b.append(rental)

    # 计算租金统计数据
    def calculate_stats(rental_data):
        mean = np.mean(rental_data)
        max_value = np.max(rental_data)
        min_value = np.min(rental_data)
        median = np.median(rental_data)
        return mean, max_value, min_value, median

    stats_1b = calculate_stats(rental_1b)
    stats_2b = calculate_stats(rental_2b)
    stats_3b = calculate_stats(rental_3b)

    statistics[city] = {
        '1b': stats_1b,
        '2b': stats_2b,
        '3b': stats_3b
    }

    # 绘制直方图
    plt.figure(figsize=(12, 6), dpi=300)

    # 租金直方图
    plt.hist(rental_1b, bins=30, color='skyblue', alpha=0.5, label='一居', density=True)
    plt.hist(rental_2b, bins=30, color='salmon', alpha=0.5, label='二居', density=True)
    plt.hist(rental_3b, bins=30, color='green', alpha=0.5, label='三居', density=True)

    # 图表设置
    plt.title(f'{city_labels[city]}租金分布')
    plt.xlabel('租金（元/月）')
    plt.ylabel('频率')
    plt.legend()

    # 保存
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{city}_2.png'), dpi=300)

# 统计信息
for city, stats in statistics.items():
    print(f"{city_labels[city]}:")
    for house_type, stat in stats.items():
        print(f"{house_type_labels[house_type]}")
        print(f"均价：{stat[0]:.2f}，最高价：{stat[1]:.2f}，最低价：{stat[2]:.2f}，中位数：{stat[3]:.2f}")
