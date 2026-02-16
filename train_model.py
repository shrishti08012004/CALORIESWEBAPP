import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# -----------------------------
# STEP A — Create Dummy Dataset
# -----------------------------

data = {
    "age": [20, 25, 30, 35, 40],
    "height": [160, 165, 170, 175, 180],
    "weight": [55, 65, 70, 75, 85],
    "duration": [30, 45, 60, 40, 50],
    "heart_rate": [90, 110, 130, 100, 120],
    "body_temp": [36.5, 37.0, 37.5, 36.8, 37.2],
    "calories": [120, 250, 400, 220, 330]
}

df = pd.DataFrame(data)

# -----------------------------
# STEP B — Split Data
# -----------------------------

X = df.drop("calories", axis=1)
y = df["calories"]

# -----------------------------
# STEP C — Train Model
# -----------------------------

model = LinearRegression()
model.fit(X, y)

# -----------------------------
# STEP D — Save Model
# -----------------------------

pickle.dump(model, open("model.pkl", "wb"))

print("✅ Model trained and saved successfully!")
