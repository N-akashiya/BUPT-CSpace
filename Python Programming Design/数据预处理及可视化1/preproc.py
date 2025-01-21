import json
import pandas as pd
import re

cleaned_data = []

with open('scrapy-new-house.json', 'r', encoding='utf-8') as f:
    for line in f:
        item = json.loads(line)

        name = item.get("name", "").strip()
        type_ = item.get("type", "").strip()
        position = item.get("position", "").strip()
        position_parts = position.split(" / ")
        district = position_parts[0].strip() if len(position_parts) > 0 else ""
        landmark = position_parts[1].strip() if len(position_parts) > 1 else ""
        address = position_parts[2].strip() if len(position_parts) > 2 else ""
        house_type = item.get("house_type", "").split(" / ")[0].strip()
        area = item.get("area")
        if area:
            area_values = re.findall(r'\d+', area)
            area = min(map(int, area_values)) if area_values else None
        total_price = item.get("total_price", "0").replace("总价", "").replace("(万/套)", "").strip()
        total_price_values = re.findall(r'\d+', total_price)
        total_price = min(map(int, total_price_values)) if total_price_values else 0
        unit_price = item.get("unit_price", "0").replace("元/㎡(均价)", "").strip()
        unit_price = int(unit_price) if unit_price else 0
        
        cleaned_data.append({
            "name": name,
            "type": type_,
            "position0": district,
            "position1": landmark,
            "position2": address,
            "house_type": house_type,
            "area": area,
            "total_price": total_price,
            "unit_price": unit_price,
        })

df = pd.DataFrame(cleaned_data)

df.to_csv('new-house.csv', index=False, encoding='utf-8-sig')