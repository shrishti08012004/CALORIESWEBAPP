import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Calories Predictor", page_icon="🔥", layout="centered")

model = pickle.load(open("model.pkl", "rb"))

st.markdown("<h1 style='text-align: center; color: orange;'>🔥 Smart Calories Burnt Predictor</h1>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🏃 Enter Your Fitness Details")

# ✅ NEW — Dropdowns
gender = st.selectbox("🧑 Gender", ["Select Gender", "Male", "Female"])

activity = st.selectbox(
    "🏋 Activity Level",
    ["Select Activity Level", "Low", "Moderate", "High"]
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("🎂 Age", min_value=1)
    height = st.number_input("📏 Height (cm)", min_value=50)
    weight = st.number_input("⚖ Weight (kg)", min_value=10)

with col2:
    duration = st.number_input("⏱ Duration (minutes)", min_value=1)
    heart_rate = st.number_input("💓 Heart Rate", min_value=40)
    body_temp = st.number_input("🌡 Body Temperature", min_value=30.0)

st.markdown("---")

if st.button("🔥 Predict Calories Burnt"):

    # ✅ VALIDATION (Very Important)
    if gender == "Select Gender":
        st.warning("⚠ Please select your gender")
    
    elif activity == "Select Activity Level":
        st.warning("⚠ Please select your activity level")

    else:
        input_data = np.array([[age, height, weight, duration, heart_rate, body_temp]])
        prediction = model.predict(input_data)

        # ✅ Optional adjustment (makes app smarter)
        if activity == "High":
            prediction = prediction * 1.1
        elif activity == "Low":
            prediction = prediction * 0.9

        st.success(f"🔥 Estimated Calories Burnt: {prediction[0]:.2f}")
        st.balloons()
