import streamlit as st
import pickle
import numpy as np
import pandas as pd

# -------------------------
# PAGE SETTINGS
# -------------------------
st.set_page_config(
    page_title="Smart Calories Predictor",
    page_icon="🔥",
    layout="centered"
)

# -------------------------
# LOAD MODEL
# -------------------------
model = pickle.load(open("model.pkl", "rb"))

# -------------------------
# TITLE
# -------------------------
st.markdown(
    "<h1 style='text-align: center; color: orange;'>🔥 Smart Calories Burnt Predictor</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

st.markdown("### 🏃 Enter Your Fitness Details")

# -------------------------
# DROPDOWNS
# -------------------------
gender = st.selectbox("🧑 Gender", ["Select Gender", "Male", "Female"])

activity = st.selectbox(
    "🏋 Activity Level",
    ["Select Activity Level", "Low", "Moderate", "High"]
)

st.markdown("---")

# -------------------------
# INPUT FIELDS
# -------------------------
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

# -------------------------
# PREDICTION BUTTON
# -------------------------
if st.button("🔥 Predict Calories Burnt"):

    if gender == "Select Gender":
        st.warning("⚠ Please select your gender")

    elif activity == "Select Activity Level":
        st.warning("⚠ Please select your activity level")

    else:
        input_data = np.array([[age, height, weight, duration, heart_rate, body_temp]])

        prediction = model.predict(input_data)

        # Activity Adjustment
        if activity == "High":
            prediction = prediction * 1.1
        elif activity == "Low":
            prediction = prediction * 0.9

        calories_value = float(prediction[0])

        st.success(f"🔥 Estimated Calories Burnt: {calories_value:.2f}")

        st.markdown("## 📊 Analytics & Insights")

        # -------------------------
        # METRICS DISPLAY
        # -------------------------
        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("⏱ Duration", f"{duration} min")

        with c2:
            st.metric("💓 Heart Rate", f"{heart_rate} bpm")

        with c3:
            st.metric("🔥 Calories", f"{calories_value:.2f}")

        st.markdown("---")

        # -------------------------
        # DATAFRAME FOR CHARTS
        # -------------------------
        chart_df = pd.DataFrame({
            "Values": [age, height, weight, duration, heart_rate, body_temp],
            "Metrics": ["Age", "Height", "Weight", "Duration", "Heart Rate", "Body Temp"]
        })

        # -------------------------
        # BAR CHART
        # -------------------------
        st.markdown("### 📊 Input Breakdown")
        st.bar_chart(chart_df.set_index("Metrics"))

        # -------------------------
        # LINE CHART (Trend Style)
        # -------------------------
        st.markdown("### 📈 Body Metrics Trend")
        st.line_chart(chart_df.set_index("Metrics"))

        # -------------------------
        # CALORIE COMPARISON
        # -------------------------
        st.markdown("### 🔥 Calories Comparison")

        comparison_df = pd.DataFrame({
            "Type": ["Predicted Calories", "Average Person (Reference)"],
            "Calories": [calories_value, 250]
        })

        st.bar_chart(comparison_df.set_index("Type"))

        st.balloons()
