import pandas as pd, yaml
from catboost import CatBoostRegressor

print('Running train...')
with open('params.yaml', 'r') as f: 
    params = yaml.safe_load(f)['train']

df = pd.read_csv('data/processed/train.csv')
model = CatBoostRegressor(iterations=params['iterations'], learning_rate=params['learning_rate'], depth=params['depth'], verbose=0)
model.fit(df.drop('Price', axis=1), df['Price'])

model.save_model('models/catboost_model.bin')