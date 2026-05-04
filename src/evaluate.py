import pandas as pd, json
from catboost import CatBoostRegressor
from sklearn.metrics import root_mean_squared_error

print('Running evaluate...')
df = pd.read_csv('data/processed/train.csv')
model = CatBoostRegressor(); model.load_model('models/catboost_model.bin')
preds = model.predict(df.drop('Price', axis=1))

rmse = root_mean_squared_error(df['Price'], preds)

with open('metrics.json', 'w') as f: 
    json.dump({'rmse': rmse}, f, indent=4)

print(f'RMSE: {rmse}')