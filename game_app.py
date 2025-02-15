import streamlit as st
import openai
import pandas as pd
import os

# Load OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Generate an AI-driven case using GPT-4 (Inspired by Real-World Money Laundering Cases)
def generate_ai_case():
    prompt = """
    Create a detailed financial crime scenario inspired by real-world money laundering cases.
    The case should include suspicious transactions, involved parties (companies, individuals, banks), 
    and locations. Focus on realistic methods like shell companies, trade-based laundering, real estate purchases, or crypto mixing.
    Provide enough detail for an investigator to analyze the scheme.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

# Analyze player's response for multiple money laundering techniques
def evaluate_response(player_answer, case_description):
    prompt = f"""
    The following is a financial crime case:

    {case_description}

    The player analyzed this case and identified the following money laundering techniques:
    "{player_answer}"

    Your task:
    1. Identify **all possible money laundering techniques** in this case.
    2. Compare the player's answer with these techniques.
    3. Score the player's response from 0-100.
    4. Provide feedback on what they got right, what they missed, and any hints for improvement.
    5. If applicable, relate this case to a **real-world money laundering scandal**.

    Return your response in a structured way: **Score (0-100)** + **Detailed Feedback**.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("🕵️ AI Money Laundering Investigator")
st.subheader("Analyze AI-generated financial crime cases and identify laundering techniques.")

# Load AI-generated case
if "current_case" not in st.session_state:
    st.session_state.current_case = generate_ai_case()

case_description = st.session_state.current_case
st.header("📄 Case Report")
st.write(case_description)

# Player input (free form)
player_answer = st.text_area("What money laundering techniques do you identify in this case?", "")

# Submit button
if st.button("Submit Analysis"):
    if player_answer:
        feedback = evaluate_response(player_answer, case_description)
        st.subheader("📋 AI Feedback")
        st.write(feedback)

        # Button to load a new case
        if st.button("Next Case"):
            st.session_state.current_case = generate_ai_case()
            st.experimental_rerun()
    else:
        st.warning("Please enter your analysis before submitting.")

# Sidebar Stats
st.sidebar.header("Game Stats")
if "cases_solved" not in st.session_state:
    st.session_state.cases_solved = 0
if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = 0

st.sidebar.write(f"✅ Cases Solved: {st.session_state.cases_solved}")
st.sidebar.write(f"🏆 Correct Answers: {st.session_state.correct_answers}")

