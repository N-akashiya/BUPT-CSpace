import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("processed_BeijingPM.csv")

data['PM'] = data[['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan']].mean(axis=1)

def standard_pm(pm):
    if 0 <= pm <= 50:
        return 1
    elif 51 <= pm < 100:
        return 2
    elif 101 <= pm <= 150:
        return 3
    elif 151 <= pm <= 200:
        return 4
    elif 201 <= pm <= 300:
        return 5
    else:
        return 0

data['level'] = data['PM'].apply(standard_pm)
filtered_data = data[data['level'] != 0]
level_count = filtered_data['level'].value_counts().sort_index()
lcdf = pd.DataFrame(level_count).reset_index()
lcdf.columns = ['Level', 'Days']
lcdf.to_csv('level_count.csv', index=False)

# 可视化
level_count.plot(kind='bar', color=['green', 'yellow', 'orange', 'red', 'purple', 'brown'])
plt.title('Level Distribution')
plt.xlabel('Level')
plt.ylabel('days')
plt.savefig('Level.png')
plt.show()