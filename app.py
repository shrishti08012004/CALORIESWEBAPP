import streamlit as st
import pickle
import numpy as np
import pandas as pd

# -------------------------
# PAGE CONFIG
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
# CUSTOM HEADER
# -------------------------
st.markdown("""
    <div style="
        background: linear-gradient(90deg, #ff9966, #ff5e62);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    ">
        <h1>🔥 Smart Calories Burnt Predictor</h1>
        <p>AI-powered fitness insights & calorie analytics</p>
    </div>
""", unsafe_allow_html=True)

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
# INPUT SECTION (CARD STYLE)
# -------------------------
st.markdown("### 📋 Personal Metrics")

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
# BUTTON
# -------------------------
if st.button("🔥 Predict Calories Burnt"):

    if gender == "Select Gender":
        st.warning("⚠ Please select your gender")

    elif activity == "Select Activity Level":
        st.warning("⚠ Please select your activity level")

    else:
        input_data = np.array([[age, height, weight, duration, heart_rate, body_temp]])

        prediction = model.predict(input_data)

        if activity == "High":
            prediction *= 1.1
        elif activity == "Low":
            prediction *= 0.9

        calories_value = float(prediction[0])

        # -------------------------
        # RESULT CARD
        # -------------------------
        st.markdown(f"""
            <div style="
                background-color: #1f2933;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                color: white;
                margin-top: 20px;
            ">
                <h2>🔥 Estimated Calories Burnt</h2>
                <h1 style="color: orange;">{calories_value:.2f}</h1>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("## 📊 Detailed Insights")

        # -------------------------
        # METRICS ROW
        # -------------------------
        c1, c2, c3 = st.columns(3)

        c1.metric("⏱ Duration", f"{duration} min")
        c2.metric("💓 Heart Rate", f"{heart_rate} bpm")
        c3.metric("🌡 Temp", f"{body_temp} °C")

        st.markdown("---")

        # -------------------------
        # CHART DATA
        # -------------------------
        chart_df = pd.DataFrame({
            "Metrics": ["Age", "Height", "Weight", "Duration", "Heart Rate", "Body Temp"],
            "Values": [age, height, weight, duration, heart_rate, body_temp]
        })

        st.markdown("### 📊 Input Breakdown")
        st.bar_chart(chart_df.set_index("Metrics"))

        st.markdown("### 📈 Body Metrics Trend")
        st.line_chart(chart_df.set_index("Metrics"))

        st.markdown("### 🔥 Calories Comparison")

        comparison_df = pd.DataFrame({
            "Category": ["Predicted Calories", "Reference Average"],
            "Calories": [calories_value, 250]
        })

        st.bar_chart(comparison_df.set_index("Category"))

        st.balloons()
