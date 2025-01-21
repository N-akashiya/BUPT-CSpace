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
city_salary = {
    'bj': 218312,
    'sh': 229337,
    'gz': 154475,
    'sz': 171854,
    'su': 138732
} # 平均工资（元/年）

input_dir = 'cleandata'
output_dir = '6'
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

# 租房负担指数
rental_burden = {}
for city in city_names:
    rental_burden[city] = city_avg_rentals[city] / (city_salary[city] / 12)

# 创建双Y轴图表
fig, ax1 = plt.subplots(figsize=(12, 6), dpi=300)
ax2 = ax1.twinx()

# 绘制柱状图（租房负担指数）
x = np.arange(len(city_names))
width = 0.3
rental_burden_scaled = [rental_burden[city] * 10000 for city in city_names] # 调整柱子的高度
rects = ax1.bar(x, rental_burden_scaled, width, label='租房负担指数', color='lightblue')

# 单位面积租金的折线图
line1 = ax1.plot(x, [city_avg_rentals[city] for city in city_names], 'bo-', label='单位面积租金', linewidth=2)

# 平均工资的折线图
line2 = ax2.plot(x, [city_salary[city] / 10000 for city in city_names], 'g^-', label='平均工资', linewidth=2)

# 设置x轴标签
ax1.set_xticks(x)
ax1.set_xticklabels([city_labels[city] for city in city_names])

# 设置标题和标签
ax1.set_ylabel('租房负担指数 & 单位面积租金（元/平米/月）')
ax2.set_ylabel('平均工资（万元/年）')
plt.title('各城市单位面积租金与平均工资关系')

# 图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

# 在柱状图上添加数值标签
for rect in rects:
    height = rect.get_height()
    ax1.text(rect.get_x() + rect.get_width()/2., height,
             f'{height:.4f}',
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'salary_analysis.png'), dpi=300)

print("各城市租房负担排名：")
sorted_cities = sorted(rental_burden.items(), key=lambda x: x[1], reverse=True)
for city, value in sorted_cities:
    avg_rental = city_avg_rentals[city]
    salary = city_salary[city]
    print(f"{city_labels[city]}")
    print(f"租房负担指数: {value:.4f}, 平均工资: {salary} 元/年, 单位面积租金: {avg_rental:.2f} 元/平米/月")