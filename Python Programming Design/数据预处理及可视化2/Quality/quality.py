import pandas as pd
import numpy as np

file_path = "BeijingPM20100101_20151231.csv"
data = pd.read_csv(file_path)

columns_to_process = ['HUMI', 'PRES', 'TEMP']

for column in columns_to_process:
    # 对缺失值进行线性插值
    data[column] = data[column].interpolate(method='linear', limit_direction='both')
    mean = data[column].mean()
    std = data[column].std()
    lower_bound = mean - 3 * std
    upper_bound = mean + 3 * std
    # 修改超过3倍标准差的值为3倍标准差
    data[column] = np.where((data[column] > upper_bound) | (data[column] < lower_bound), np.nan, data[column])
    data[column] = data[column].interpolate(method='linear', limit_direction='both')

    # PM异常值处理
    pm_columns = ['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan']
    for column in pm_columns:
        data[column] = np.where(data[column] > 500, 500, data[column])
    
    # cv后项填充
    data['cbwd'] = data['cbwd'].replace('cv', method='bfill')

output_file = "processed_BeijingPM.csv"
data.to_csv(output_file, index=False)