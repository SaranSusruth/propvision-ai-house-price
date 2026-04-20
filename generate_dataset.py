import pandas as pd
import numpy as np
import random

rows = []

zones = ["rural", "suburban", "urban", "luxury"]

for _ in range(600):   # creates 600 rows
    zone = random.choice(zones)

    if zone == "rural":
        area = random.randint(700, 1500)
        loc = random.randint(3, 6)
        base_price = area * 30

    elif zone == "suburban":
        area = random.randint(1000, 2000)
        loc = random.randint(5, 8)
        base_price = area * 40

    elif zone == "urban":
        area = random.randint(1500, 3000)
        loc = random.randint(7, 10)
        base_price = area * 55

    else:  # luxury
        area = random.randint(2500, 4500)
        loc = random.randint(8, 10)
        base_price = area * 75

    bedrooms = max(1, area // 500)
    bathrooms = max(1, bedrooms - 1)
    age = random.randint(0, 25)
    garage = random.randint(0, 3)
    pool = 1 if zone == "luxury" and random.random() > 0.4 else 0

    noise = random.uniform(0.9, 1.1)

    price = int(base_price * (loc / 10) * noise)

    rows.append([
        area, bedrooms, bathrooms, loc,
        age, garage, pool, zone, price
    ])

df = pd.DataFrame(rows, columns=[
    "area","bedrooms","bathrooms","location_rating",
    "age","garage","pool","zone","price"
])

df.to_csv("dataset_v2.csv", index=False)

print("✅ dataset_v2.csv created!")