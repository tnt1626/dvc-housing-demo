import pandas as pd

print('Running data_prep...')
df = pd.read_csv('data/raw/dataset.csv')
df['LotArea'] = df['LotArea'] / 1000 
df.to_csv('data/processed/train.csv', index=False)