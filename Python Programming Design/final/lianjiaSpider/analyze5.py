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
city_gdp_person = {
    'bj': 20.03,
    'sh': 19.08,
    'gz': 16.2,
    'sz': 19.59,
    'su': 19.09
} # 人均GDP（万元）

input_dir = 'cleandata'
output_dir = '5'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

city_avg_rentals = {}
for city in city_names:
    input_file = os.path.join(input_dir, f'{city}-data.json')
    unit_rentals = []
    with jsonlines.open(input_file, mode='r') as reader:
        for item in reader:
            rental = item.get('rental')
            area = item.get('area')
            if rental and area:
                unit_rental = rental / area
                unit_rentals.append(unit_rental)
    city_avg_rentals[city] = np.mean(unit_rentals)

# 租房性价比
rental_affordability = {}
for city in city_names:
    rental_affordability[city] = city_avg_rentals[city] / (city_gdp_person[city] * 10000 / 12)

# 创建双Y轴图表
fig, ax1 = plt.subplots(figsize=(12, 6), dpi=300)
ax2 = ax1.twinx()

# 绘制柱状图（租房性价比）
x = np.arange(len(city_names))
width = 0.3
rental_affordability_scaled = [rental_affordability[city] * 10000 for city in city_names] # 调整柱子的高度
rects = ax1.bar(x, rental_affordability_scaled, width, label='租房性价比', alpha=0.8, color='lightblue')

# 单位面积租金的折线图
ax1.plot(x, [city_avg_rentals[city] for city in city_names], 'bo-', label='单位面积租金', linewidth=2)

# 人均GDP的折线图
ax2.plot(x, [city_gdp_person[city] for city in city_names], 'g^-', label='人均GDP', linewidth=2)

# 设置x轴标签
ax1.set_xticks(x)
ax1.set_xticklabels([city_labels[city] for city in city_names])

# 设置y轴范围
ax1.set_ylim(0, max(city_avg_rentals.values()) * 1.1)
ax2.set_ylim(0, max(city_gdp_person.values()) * 1.1)

# 设置标题和标签
ax1.set_ylabel('单位面积租金（元/平米/月）')
ax2.set_ylabel('人均GDP（万元/年）')
plt.title('各城市单位面积租金与人均GDP关系')

# 图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower right')

# 在柱状图上添加数值标签
for i, rect in enumerate(rects):
    height = rect.get_height()
    original_value = rental_affordability[city_names[i]]
    ax1.text(rect.get_x() + rect.get_width() / 2., height,
             f'{original_value:.4f}',
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'gdp_analysis.png'), dpi=300)

print("各城市租房性价比排名：")
sorted_cities = sorted(rental_affordability.items(), key=lambda x: x[1])
for city, value in sorted_cities:
    print(f"{city_labels[city]}: {value:.4f}")