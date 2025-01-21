import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('new-house.csv')

house_count = df.groupby('position0')['unit_price'].count()
avg_unit_price = df.groupby('position0')['unit_price'].mean()
avg_total_price = df.groupby('position0')['total_price'].mean()

# 对宽度进行归一化处理，代表楼盘数量
normalized_width = (house_count / house_count.max())*0.6+0.4
# 柱子位置
x_positions = np.arange(len(avg_unit_price))

fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(x_positions, avg_unit_price, width=normalized_width, color='#008888')
ax1.set_xticks(x_positions)
ax1.set_xticklabels(avg_unit_price.index, rotation=90)
ax1.set_xlabel('行政区')
ax1.set_ylabel('平均单价（元）')
ax1.set_title('各行政区楼盘平均单价')
plt.tight_layout()
plt.savefig('2_DistrictAvgUnit.png', dpi=300)
plt.show()

fig, ax2 = plt.subplots(figsize=(12, 6))
ax2.bar(x_positions, avg_total_price, width=normalized_width, color='#026399')
ax2.set_xticks(x_positions)
ax2.set_xticklabels(avg_total_price.index, rotation=90)
ax2.set_xlabel('行政区')
ax2.set_ylabel('平均总价（万元）')
ax2.set_title('各行政区楼盘平均总价')
plt.tight_layout()
plt.savefig('2_DistrictAvgTotal.png', dpi=300)
plt.show()