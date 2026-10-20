import os
import time

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
if not os.environ.get("OPENROUTER_API_KEY"):
    raise EnvironmentError("OPENROUTER_API_KEY not found in environment variables.")

from llm import create_llm, invoke_with_retry

st.set_page_config(page_title="Diet Plan Generator", layout="wide")

ACTIVITY_LEVELS = [
    "Sedentary (office job, no exercise)",
    "Light (light exercise 1-3 days/week)",
    "Moderate (exercise 3-5 days/week)",
    "Active (hard exercise 6-7 days/week)",
    "Very Active (physical job + exercise)",
    "Extra Active (athlete/very intense training)",
]

DEFAULT_GOAL = "Maintain healthy weight and improve energy levels"
PLACEHOLDER_PLAN = "*Your diet plan will appear here after generation...*"


@st.cache_resource
def get_llm():
    return create_llm()


def generate_plan(weight, height, activity, age, goal, sleep_hours, progress, status):
    status.markdown("📋 Validating input parameters...")
    progress.progress(10)
    time.sleep(0.3)

    if not all([weight > 0, height > 0, age > 0, sleep_hours >= 0]):
        progress.progress(100)
        status.markdown("❌ Invalid input parameters")
        return "**Error:** Please ensure all numeric values are valid and positive."

    status.markdown("📊 Calculating BMI and metabolic data...")
    progress.progress(20)
    time.sleep(0.3)

    bmi = weight / ((height / 100) ** 2)

    status.markdown("🤖 Preparing AI prompt...")
    progress.progress(40)
    time.sleep(0.2)

    messages = [
        (
            "system",
            """You are a veteran nutritionist who always responds in formatted **Markdown**. 
        Provide a comprehensive diet plan with:
        - Daily calorie targets
        - Meal timings and portion sizes
        - Macro/micronutrient breakdowns
        - Food recommendations (no whey protein)
        - Hydration guidelines
        - Any relevant health considerations
        
        Format your response with clear headers, bullet points, and tables where appropriate.""",
        ),
        (
            "human",
            f"""
        Please create a personalized diet plan for:
        - Weight: {weight} kg
        - Height: {height} cm (BMI: {bmi:.1f})
        - Activity Level: {activity}
        - Age: {age} years
        - Fitness Goal: {goal}
        - Sleep Duration: {sleep_hours} hours/day
        
        Provide a detailed diet plan with specific recommendations.
        """,
        ),
    ]

    status.markdown("🔄 Sending request to AI model...")
    progress.progress(60)

    try:
        response = invoke_with_retry(get_llm(), messages)
        status.markdown("📝 Processing AI response...")
        progress.progress(80)
        time.sleep(0.2)

        content = response.content

        status.markdown("✨ Finalizing diet plan...")
        progress.progress(95)
        time.sleep(0.2)

        progress.progress(100)
        status.markdown("✅ Diet plan generated successfully!")
        return content
    except Exception as e:
        progress.progress(100)
        status.markdown("❌ Error occurred")
        message = str(e)
        if "429" in message or "rate-limited" in message.lower():
            return (
                "**Error:** The Gemma model is temporarily rate-limited on OpenRouter. "
                "Wait a minute and try again, or add a Google AI Studio key under "
                "[OpenRouter integrations](https://openrouter.ai/settings/integrations) "
                "to raise the limit."
            )
        return f"**Error:** Failed to generate diet plan. Please try again.\n\n*Error details: {message}*"


if "diet_plan" not in st.session_state:
    st.session_state.diet_plan = PLACEHOLDER_PLAN

st.title("Personalized Diet Plan Generator")
st.markdown(
    """
Enter your personal information below to receive a **comprehensive, AI-generated diet plan**
tailored to your specific needs and goals.

*All plans are formatted in Markdown with detailed macro/micronutrient breakdowns.*
"""
)

stats_col, lifestyle_col = st.columns(2)

with stats_col:
    st.subheader("📊 Physical Stats")
    weight = st.slider("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
    height = st.slider("Height (cm)", min_value=100.0, max_value=280.0, value=170.0, step=0.5)
    age = st.slider("Age (years)", min_value=16, max_value=80, value=30, step=1)

with lifestyle_col:
    st.subheader("🏃‍♂️ Lifestyle")
    activity = st.selectbox(
        "Activity Level",
        ACTIVITY_LEVELS,
        index=ACTIVITY_LEVELS.index("Moderate (exercise 3-5 days/week)"),
    )
    sleep_hours = st.slider(
        "Sleep Hours per Day", min_value=4.0, max_value=12.0, value=8.0, step=0.5
    )
    goal = st.text_area(
        "Fitness/Health Goal",
        value=DEFAULT_GOAL,
        height=100,
        placeholder="e.g., Lose 10kg in 3 months, Build muscle mass, Maintain current weight, Improve energy levels...",
    )

generate_col, clear_col = st.columns(2)
with generate_col:
    generate_clicked = st.button("🎯 Generate My Diet Plan", type="primary", use_container_width=True)
with clear_col:
    clear_clicked = st.button("Clear", use_container_width=True)

if clear_clicked:
    st.session_state.diet_plan = PLACEHOLDER_PLAN
    st.rerun()

if generate_clicked:
    progress = st.progress(0)
    status = st.empty()
    st.session_state.diet_plan = generate_plan(
        weight, height, activity, age, goal, sleep_hours, progress, status
    )

st.subheader("Your Personalized Diet Plan")
st.markdown(st.session_state.diet_plan)
