import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

df = pd.read_csv('new-house.csv')

type_colors = {
    '商业': 'red',
    '低密住宅': 'blue',
    '住宅': 'green'
}
colors = df['type'].map(type_colors)
df = df[colors.notna()]
colors = colors[colors.notna()] # 商业类

plt.figure(figsize=(10, 6))

scatter = plt.scatter(df['unit_price'], df['total_price'], c=colors, alpha=0.6)

handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in type_colors.values()]
labels = type_colors.keys()
plt.legend(handles, labels, title='楼盘类型')

plt.title('楼盘价格分布')
plt.ylabel('单价（元/㎡）')
plt.xlabel('总价（万元）')

plt.savefig('1_PriceDistribution.png', dpi=300)
plt.show()