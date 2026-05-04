import pandas as pd, numpy as np

np.random.seed(42)
n = 2000

df = pd.DataFrame({
    'LotArea': np.random.randint(500, 15000, n),
    'YearBuilt': np.random.randint(1950, 2023, n),
    'Rooms': np.random.randint(1, 6, n),
    'Price': np.random.randint(100000, 500000, n)
})

df.to_csv('data/raw/dataset.csv', index=False)