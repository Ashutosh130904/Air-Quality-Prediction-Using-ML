import numpy as np
import pandas as pd
import joblib

df = pd.read_csv('2023Dataset.csv')

median_val = df['PM2.5 (µg/m³)'].median()
df['PM2.5 (µg/m³)'] =  df['PM2.5 (µg/m³)'].fillna(median_val)

median_val = df['PM10 (µg/m³)'].median()
df['PM10 (µg/m³)'] =  df['PM10 (µg/m³)'].fillna(median_val)

median_val = df['NO2 (µg/m³)'].median()
df['NO2 (µg/m³)'] =  df['NO2 (µg/m³)'].fillna(median_val)


median_val = df['NH3 (µg/m³)'].median()
df['NH3 (µg/m³)'] =  df['NH3 (µg/m³)'].fillna(median_val)

median_val = df['SO2 (µg/m³)'].median()
df['SO2 (µg/m³)'] =  df['SO2 (µg/m³)'].fillna(median_val)

median_val = df['CO (mg/m³)'].median()
df['CO (mg/m³)'] =  df['CO (mg/m³)'].fillna(median_val)


median_val = df['Ozone (µg/m³)'].median()
df['Ozone (µg/m³)'] =  df['Ozone (µg/m³)'].fillna(median_val)

X = df.iloc[ : , 0:7].values
Y = df.iloc[ : , -1].values


from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


from sklearn.linear_model import LinearRegression

lr = LinearRegression()

lr.fit(X_train, Y_train)

Y_pred = lr.predict(X_test)



joblib.dump(lr, 'air_quality_prediction.pkl')
print("Model trained and saved")
