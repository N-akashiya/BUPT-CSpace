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

input_dir = 'cleandata' 
output_dir = '1'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

statistics = {}

for city in city_names:
    input_file = os.path.join(input_dir, f'{city}-data.json')
    data = []

    with jsonlines.open(input_file, mode='r') as reader:
        for obj in reader:
            data.append(obj)
    
    rental = [item['rental'] for item in data]
    area = [item['area'] for item in data]

    # 计算总体租金的统计数据
    rental_mean = np.mean(rental)
    rental_max = np.max(rental)
    rental_min = np.min(rental)
    rental_median = np.median(rental)

    # 计算单位面积租金
    rental_per_area = [r / a for r, a in zip(rental, area) if a > 0]
    rental_per_area_mean = np.mean(rental_per_area)
    rental_per_area_max = np.max(rental_per_area)
    rental_per_area_min = np.min(rental_per_area)
    rental_per_area_median = np.median(rental_per_area)

    # 存储每个城市的统计数据
    statistics[city] = {
        'rental_mean': rental_mean,
        'rental_max': rental_max,
        'rental_min': rental_min,
        'rental_median': rental_median,
        'rental_per_area_mean': rental_per_area_mean,
        'rental_per_area_max': rental_per_area_max,
        'rental_per_area_min': rental_per_area_min,
        'rental_per_area_median': rental_per_area_median
    }

    # 绘制直方图
    plt.figure(figsize=(12, 6), dpi=300)

    # 总体租金直方图
    plt.subplot(1, 2, 1)
    plt.hist(rental, bins=30, color='skyblue', alpha=0.7, density=True)
    plt.title(f'{city_labels[city]}租金频率分布直方图')
    plt.xlabel('租金（元/月）')
    plt.ylabel('频率')

    # 单位面积租金直方图
    plt.subplot(1, 2, 2)
    plt.hist(rental_per_area, bins=30, color='salmon', alpha=0.7, density=True)
    plt.title(f'{city_labels[city]}单位面积租金频率分布直方图')
    plt.xlabel('单位面积租金（元/平方米）')
    plt.ylabel('频率')

    # 保存
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{city}_1.png'))

# 统计信息
for city, stats in statistics.items():
    print(f"{city_labels[city]}:")
    print(f"租金均价：{stats['rental_mean']:.2f}，最高价：{stats['rental_max']:.2f}，最低价：{stats['rental_min']:.2f}，中位数：{stats['rental_median']:.2f}")
    print(f"单位面积租金均价：{stats['rental_per_area_mean']:.2f}，最高价：{stats['rental_per_area_max']:.2f}，最低价：{stats['rental_per_area_min']:.2f}，中位数：{stats['rental_per_area_median']:.2f}")
    