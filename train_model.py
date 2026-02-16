import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# ✅ Load datasets
exercise_df = pd.read_csv("exercise.csv")
calories_df = pd.read_csv("calories.csv")

# ✅ Combine datasets (VERY IMPORTANT)
df = pd.concat([exercise_df, calories_df["Calories"]], axis=1)

# ✅ Select features
X = df[["Age", "Height", "Weight", "Duration", "Heart_Rate", "Body_Temp"]]
y = df["Calories"]

# ✅ Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# ✅ Train model
model = LinearRegression()
model.fit(X_train, y_train)

# ✅ Save model
pickle.dump(model, open("model.pkl", "wb"))

print("✅ Real dataset model trained successfully!")
