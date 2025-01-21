import os
import jsonlines

city_names = ['bj', 'sh', 'gz', 'sz', 'su']

output_dir = 'cleandata'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for city in city_names:  
    input_file = f'{city}-renthouse.json'
    data = []
    with jsonlines.open(input_file, mode='r') as reader:
        for obj in reader:
            data.append(obj)

    # 过滤板块为 null 的数据
    filtered_data = [item for item in data if item.get('plate') is not None and item.get('area') and item['area'][0].isdigit()]
    
    # 面积和房租转换为数值
    for item in filtered_data:
        item['area'] = float(item['area'].replace('平方米', ''))
        item['rental'] = float(item['rental'].replace('元/月', '').replace(',', ''))

    # 去重
    seen = set()
    cleaned_data = []
    for item in filtered_data:
        unique_key = (item.get('plate'), item.get('orien'), item.get('house_type'), item.get('area'), item.get('rental'))
        if unique_key not in seen:
            seen.add(unique_key)
            cleaned_data.append(item)

    output_file = os.path.join(output_dir, f'{city}-data.json')
    with jsonlines.open(output_file, mode='w') as writer:
        writer.write_all(cleaned_data)