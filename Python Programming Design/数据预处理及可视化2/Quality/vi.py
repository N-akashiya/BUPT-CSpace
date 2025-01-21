import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("processed_BeijingPM.csv")

# 0-1归一化
data['DEWP_01'] = (data['DEWP'] - data['DEWP'].min()) / (data['DEWP'].max() - data['DEWP'].min())
data['TEMP_01'] = (data['TEMP'] - data['TEMP'].min()) / (data['TEMP'].max() - data['TEMP'].min())

# Z-Score归一化
data['DEWP_Z'] = (data['DEWP'] - data['DEWP'].mean()) / data['DEWP'].std()
data['TEMP_Z'] = (data['TEMP'] - data['TEMP'].mean()) / data['TEMP'].std()

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.scatter(data['DEWP_01'], data['TEMP_01'], alpha=0.5)
plt.title('0-1 Normalization')
plt.xlabel('DEWP')
plt.ylabel('TEMP')

plt.subplot(1, 2, 2)
plt.scatter(data['DEWP_Z'], data['TEMP_Z'], alpha=0.5)
plt.title('Z-Score Normalization')
plt.xlabel('DEWP')
plt.ylabel('TEMP')

plt.tight_layout()
plt.savefig('Normalization.png')
plt.show()