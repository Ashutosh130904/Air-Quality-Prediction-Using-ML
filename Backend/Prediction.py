import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV
import joblib

# Load dataset
df = pd.read_csv('2023-24_AQI_Dataset.csv')

# Interpolate and fill missing values
df_interpolated = df.interpolate(method='linear', limit_direction='both')
df_filled = df_interpolated.ffill().bfill()

# Create new targets: AQI for next day and day after next
df_filled['AQI_next_day_1'] = df_filled['AQI'].shift(-1)
df_filled['AQI_next_day_2'] = df_filled['AQI'].shift(-2)

# Drop rows with missing AQI predictions
df_final = df_filled.dropna(subset=['AQI_next_day_1', 'AQI_next_day_2'])

# Define features and targets
features = ['PM2.5 (µg/m³)', 'PM10 (µg/m³)', 'NO2 (µg/m³)', 
            'NH3 (µg/m³)', 'SO2 (µg/m³)', 'CO (mg/m³)', 'Ozone (µg/m³)']

X = df_final[features].values
Y1 = df_final['AQI_next_day_1'].values
Y2 = df_final['AQI_next_day_2'].values

# Train-test split
X_train, X_test, Y1_train, Y1_test = train_test_split(X, Y1, test_size=0.1, random_state=42)
_, _, Y2_train, Y2_test = train_test_split(X, Y2, test_size=0.1, random_state=42)

# (1) Linear Regresson

from sklearn.linear_model import LinearRegression

lr1 = LinearRegression()  # first object for next day AQi

# Fit the model for next day AQI
lr1.fit(X_train, Y1_train)


lr2 = LinearRegression()   # second object for day after next AQI

# Fit the model for day after next's AQI
lr2.fit(X_train, Y2_train)

# (2) Decision Tree

from sklearn.tree import DecisionTreeRegressor

dtr1 = DecisionTreeRegressor(    # first object for next day AQi
    max_depth=50,
    min_samples_split=100,
    min_samples_leaf=5,
    random_state=42
)

dtr1.fit(X_train, Y1_train)

dtr2 = DecisionTreeRegressor(      # second object for day after next AQI
    max_depth=80,
    min_samples_split=150,
    min_samples_leaf=5,
    random_state=42
)

dtr2.fit(X_train, Y2_train)

# (3) SVR (Support Vector Regressor)

from sklearn.svm import SVR

param_grid={
    'C': [0.1, 1, 5, 10],
    'kernel': ['linear', 'rbf', 'poly'],
    'gamma': ['scale', 'auto'],
    'epsilon': [0.01, 0.1, 0.2]
}
              

from sklearn.model_selection import RandomizedSearchCV

svm1 = SVR()

model1 = RandomizedSearchCV(
    estimator= svm1,
    param_distributions= param_grid,
    n_iter= 10,
    cv= 3,
    random_state= 42,
    n_jobs= -1,
    scoring= 'r2',
    verbose= 1
)

model1.fit(X_train, Y1_train)

svm2 = SVR()

model2 = RandomizedSearchCV(
    estimator= svm2,
    param_distributions= param_grid,
    n_iter= 10,
    cv= 3,
    random_state= 42,
    n_jobs= -1,
    scoring= 'r2',
    verbose= 1
)

model2.fit(X_train, Y2_train)

# (4) Random Forest

param_grid = {
    'n_estimators': [100, 200, 300, 500, 700, 1000],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2', None]
}

rf1 = RandomForestRegressor(random_state=42)  # first object for next day AQi

from sklearn.model_selection import RandomizedSearchCV

search1 = RandomizedSearchCV(
    estimator= rf1,
    param_distributions= param_grid,
    n_iter= 30,
    cv= 3,
    scoring= 'r2',
    random_state= 42,
    n_jobs= -1,
    verbose=1
)
    


search1.fit(X_train, Y1_train)


rf2 = RandomForestRegressor(random_state=42)        # second object for day after next AQI

search2 = RandomizedSearchCV(
    estimator= rf2,
    param_distributions= param_grid,
    n_iter= 10,
    cv= 3,
    scoring= 'r2',
    random_state= 42,
    n_jobs= -1,
    verbose= 1
)

search2.fit(X_train, Y2_train)

best_model1 = search1.best_estimator_
joblib.dump(best_model1, 'aqi_predictor_day1.pkl')
print("✅ Tuned model for next day AQI saved as 'aqi_predictor_day1.pkl'.")


best_model2 = search2.best_estimator_
joblib.dump(best_model2, 'aqi_predictor_day1.pkl')
print("✅ Tuned model for next day AQI saved as 'aqi_predictor_day1.pkl'.")
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# valuate models on test data
y1_pred = search1.predict(X_test)
y2_pred = search2.predict(X_test)

# Calculate metrics for next day AQI prediction
print("📊 Accuracy for aqi_predictor_day1:")
print(f"R² Score: {r2_score(Y1_test, y1_pred)}")
print(f"MAE: {mean_absolute_error(Y1_test, y1_pred)}")
print(f"RMSE: {np.sqrt(mean_squared_error(Y1_test, y1_pred))}")

# Calculate metrics for day after next AQI prediction
print("📊 Accuracy for aqi_predictor_day2:")
print(f"R² Score: {r2_score(Y2_test, y2_pred)}")
print(f"MAE: {mean_absolute_error(Y2_test, y2_pred)}")
print(f"RMSE: {np.sqrt(mean_squared_error(Y2_test, y2_pred))}")

