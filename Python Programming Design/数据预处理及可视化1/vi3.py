import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

df = pd.read_csv('new-house.csv')

house_count = df['position0'].value_counts()

plt.figure(figsize=(10, 8))
plt.pie(house_count, labels=house_count.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(len(house_count))))
plt.title('楼盘行政区分布', y=1.1)
plt.axis('equal')
plt.tight_layout()
plt.savefig('3_DistrictPie.png', dpi=300)
plt.show()