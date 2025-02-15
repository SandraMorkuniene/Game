import streamlit as st
import openai
import pandas as pd
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Generate an AI-driven case using GPT-4 (Inspired by Real-World Money Laundering Cases)
def generate_ai_case():
    prompt = """
    Create a detailed financial crime scenario based on real-world money laundering cases, focusing on the **suspicious activities** rather than **techniques**.
    The scenario should involve multiple parties (companies, individuals, banks) and locations, but avoid directly naming specific financial crime techniques. Instead, describe suspicious behavior and activities that would indicate illicit operations. 
    Focus on unusual patterns in the transactions and business operations, without explicitly naming any of the techniques.

    The case should involve:
    - Multiple entities with complex relationships across different countries.
    - Unusual financial transactions such as large or rapid movements of money, or payments with no apparent business rationale.
    - Inconsistencies in business activities and ownership structures that raise questions.
    - A network of companies and individuals engaged in activities that appear to be legitimate, but are potentially masking illegal behavior.
    - Use of real estate, international payments, and digital assets as part of the financial transactions.

    The description should **not** mention specific techniques like "trade-based laundering" or "shell companies," but provide enough detail for an investigator to **spot** the suspicious activities. Focus on subtle clues such as:
    - Unexplained or overly complex ownership structures.
    - Over-invoicing or under-invoicing of goods or services.
    - Transactions flowing through countries with minimal or opaque financial regulations.
    - Use of third-party companies with no clear business purpose or related activities.

    Provide a detailed scenario, and let the investigator deduce the potential suspicious techniques from the activities described.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=500,
        temperature=0.7,
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content

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

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content

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
