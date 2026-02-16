import streamlit as st
import pickle
import numpy as np
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Smart Calories Predictor", page_icon="🔥")

# -------------------------
# LOAD MODEL
# -------------------------
model = pickle.load(open("model.pkl", "rb"))

# -------------------------
# SESSION STATE FOR HISTORY ⭐
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# HEADER
# -------------------------
st.markdown("""
    <div style="
        background: linear-gradient(90deg, #ff9966, #ff5e62);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
    ">
        <h1>🔥 Smart Calories Burnt Predictor</h1>
        <p>AI-powered fitness insights</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("### 🏃 Enter Your Fitness Details")

# -------------------------
# INPUTS
# -------------------------
gender = st.selectbox("🧑 Gender", ["Select Gender", "Male", "Female"])
activity = st.selectbox("🏋 Activity Level", ["Select Activity Level", "Low", "Moderate", "High"])

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("🎂 Age", min_value=1)
    height = st.number_input("📏 Height (cm)", min_value=50)
    weight = st.number_input("⚖ Weight (kg)", min_value=10)

with col2:
    duration = st.number_input("⏱ Duration (minutes)", min_value=1)
    heart_rate = st.number_input("💓 Heart Rate", min_value=40)
    body_temp = st.number_input("🌡 Body Temperature", min_value=30.0)

# -------------------------
# PDF FUNCTION ⭐⭐⭐
# -------------------------
def generate_pdf(data):

    doc = SimpleDocTemplate("report.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Calories Burnt Prediction Report", styles['Title']))
    elements.append(Spacer(1, 20))

    for key, value in data.items():
        elements.append(Paragraph(f"<b>{key}:</b> {value}", styles['BodyText']))
        elements.append(Spacer(1, 10))

    doc.build(elements)

# -------------------------
# PREDICTION BUTTON
# -------------------------
if st.button("🔥 Predict Calories Burnt"):

    if gender == "Select Gender":
        st.warning("⚠ Please select gender")

    elif activity == "Select Activity Level":
        st.warning("⚠ Please select activity level")

    else:
        input_data = np.array([[age, height, weight, duration, heart_rate, body_temp]])
        prediction = model.predict(input_data)

        if activity == "High":
            prediction *= 1.1
        elif activity == "Low":
            prediction *= 0.9

        calories_value = float(prediction[0])

        st.success(f"🔥 Estimated Calories Burnt: {calories_value:.2f}")

        # -------------------------
        # SAVE TO HISTORY ⭐
        # -------------------------
        record = {
            "Age": age,
            "Height": height,
            "Weight": weight,
            "Duration": duration,
            "Heart Rate": heart_rate,
            "Body Temp": body_temp,
            "Calories": round(calories_value, 2)
        }

        st.session_state.history.append(record)

        # -------------------------
        # CHARTS
        # -------------------------
        chart_df = pd.DataFrame({
            "Metrics": ["Age", "Height", "Weight", "Duration", "Heart Rate", "Body Temp"],
            "Values": [age, height, weight, duration, heart_rate, body_temp]
        })

        st.bar_chart(chart_df.set_index("Metrics"))

        # -------------------------
        # PDF GENERATION ⭐⭐⭐
        # -------------------------
        generate_pdf(record)

        with open("report.pdf", "rb") as file:
            st.download_button(
                label="📄 Download Report PDF",
                data=file,
                file_name="Calories_Report.pdf",
                mime="application/pdf"
            )

        st.balloons()

# -------------------------
# DISPLAY HISTORY ⭐⭐⭐
# -------------------------
st.markdown("## 📜 Prediction History")

if len(st.session_state.history) == 0:
    st.write("No predictions yet")

else:
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df)
