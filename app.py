# app.py
import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

# Initialize OpenAI Client
client = OpenAI(api_key=api_key, base_url=base_url)

st.title("🧠 StressEase - AI-Based Stress Predictor")

st.write("Please rate the following from 1 (low) to 5 (high):")

# Define stress factor inputs
factors = {
    "Anxiety": st.slider("Anxiety", 1, 5),
    "Sleep Quality": st.slider("Sleep Quality", 1, 5),
    "Academic Pressure": st.slider("Academic Pressure", 1, 5),
    "Career Concerns": st.slider("Career Concerns", 1, 5),
    "Relationship with Teachers": st.slider("Relationship with Teachers", 1, 5),
    "Peer Pressure": st.slider("Peer Pressure", 1, 5),
    "Headache": st.slider("Headache", 1, 5),
    "Blood Pressure": st.slider("Blood Pressure", 1, 5),
    "Noise at Home": st.slider("Noise at Home", 1, 5),
    "Bullying": st.slider("Bullying", 1, 5),
    "Extracurricular Load": st.slider("Extracurricular Load", 1, 5),
}

if st.button("🧠 Predict Stress & Get Suggestions"):
    with st.spinner("Analyzing your data..."):
        # Compute average stress level
        avg = sum(factors.values()) / len(factors)
        if avg <= 2.5:
            level = "Low"
        elif avg <= 3.5:
            level = "Medium"
        else:
            level = "High"

        # Prompt for GPT
        prompt = "A user submitted these stress ratings:\n"
        for k, v in factors.items():
            prompt += f"{k}: {v}/5\n"
        prompt += "\nGive 3 personalized suggestions to reduce stress and improve well-being."

        # Call A4F/OpenAI API
        response = client.chat.completions.create(
            model="provider-5/gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        suggestions_raw = response.choices[0].message.content.strip()
        suggestions = [s.strip("-•123. ").strip() for s in suggestions_raw.split("\n") if s.strip()]

        # Output result
        st.success(f"Your Stress Level: **{level}**")
        st.subheader("💡 Personalized Suggestions:")
        for s in suggestions:
            st.markdown(f"- {s}")


