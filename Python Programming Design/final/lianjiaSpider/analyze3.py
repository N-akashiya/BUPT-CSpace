import os
import jsonlines
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

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
output_dir = '3'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for city in city_names:
    input_file = os.path.join(input_dir, f'{city}-data.json')
    data = []

    with jsonlines.open(input_file, mode='r') as reader:
        for obj in reader:
            data.append(obj)

    # 计算每个板块的均价
    plate_rentals = {}
    for item in data:
        plate = item.get('plate')
        rental = item.get('rental')
        if plate and rental:
            if plate not in plate_rentals:
                plate_rentals[plate] = []
            plate_rentals[plate].append(rental)

    plate_avg_rentals = {plate: np.mean(rentals) for plate, rentals in plate_rentals.items()}
    sorted_plates = sorted(plate_avg_rentals.items(), key=lambda x: x[1], reverse=True)

    # 绘制板块均价柱状图
    fig, ax = plt.subplots(figsize=(12, 12), dpi=300)
    plates, avg_rentals = zip(*sorted_plates)

    # 创建渐变色
    norm = Normalize(vmin=min(avg_rentals), vmax=max(avg_rentals))
    sm = ScalarMappable(cmap='Blues', norm=norm)
    sm.set_array([])
    colors = [sm.to_rgba(value) for value in avg_rentals]

    bars = ax.barh(plates, avg_rentals, color=colors, height=0.7)
    for bar, avg_rental in zip(bars, avg_rentals):
        ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height() / 2, f'{avg_rental:.2f}', va='center')
    ax.set_xlabel('均价（元/月）')
    ax.set_title(f'{city_labels[city]}各板块租金均价')
    ax.invert_yaxis() # 反转Y轴，使均价最高的板块在最上面
    # 颜色条
    cbar = fig.colorbar(sm, ax=ax)

    # 保存
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{city}_3.png'), dpi=300)
    plt.close()