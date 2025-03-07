import streamlit as st
import openai
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Generate an AI-driven case
def generate_ai_case():
    prompt = """
    Write a detailed narrative about a complex financial operation involving multiple businesses, individuals, and jurisdictions. 
    The story should describe business activities, financial transactions, and relationships as they would appear to an observer, without explicitly stating what is suspicious. 
    Keep the description concise but informative, under 400 words. Focus on key financial transactions and operational details without excessive background information.

    The case should focus on realistic details about how the operation functions, including:

    - The nature of the businesses involved and how they interact financially.
    - The flow of funds, including major transactions, partnerships, and expansion efforts.
    - Ownership structures, operational decisions, and how different entities justify their financial movements.

    The scenario should be told as a realistic business case, not an analysis. Avoid phrases like "this is suspicious" or bullet-pointed red flags. Instead, provide a complete narrative where an investigator could later identify concerns based on the details provided.

    Example approach:
    - Describe a company's rapid rise and how its financials evolved.
    - Show transactions between multiple parties without explicitly stating they are unusual.
    - Introduce complex relationships between entities without saying they are suspicious.
    - Let the inconsistencies in the business activities become evident only through storytelling rather than direct analysis.
    
    The goal is to create a scenario where the reader must piece together what might be wrong, rather than having the issues directly pointed out.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=800,
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

# Initialize session state for case tracking
if "current_case" not in st.session_state:
    st.session_state.current_case = generate_ai_case()
if "cases_solved" not in st.session_state:
    st.session_state.cases_solved = 0
if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = 0

# Streamlit UI
st.title("🕵️ AI Money Laundering Investigator")
st.subheader("Analyze AI-generated financial crime cases and identify laundering techniques.")

# Display current case
st.header("📄 Case Report")
st.write(st.session_state.current_case)

# Player input (free form)
player_answer = st.text_area("What money laundering techniques do you identify in this case?", "")

# Submit button
if st.button("Submit Analysis"):
    if player_answer:
        feedback = evaluate_response(player_answer, st.session_state.current_case)
        
        # Extract the score from AI feedback
        try:
            score = int([s for s in feedback.split() if s.isdigit()][0])  # Extract first number as score
        except:
            score = 0  # Default to 0 if parsing fails

        # Update game stats
        st.session_state.cases_solved += 1
        if score >= 50:  # Example threshold for a "correct" answer
            st.session_state.correct_answers += 1

        st.subheader("📋 AI Feedback")
        st.write(feedback)

# Button to load a new case
if st.button("Next Case"):
    st.session_state.current_case = generate_ai_case()
    st.rerun()  # Force refresh to show new case

# Sidebar Stats
st.sidebar.header("Game Stats")
st.sidebar.write(f"✅ Cases Solved: {st.session_state.cases_solved}")
st.sidebar.write(f"🏆 Correct Answers: {st.session_state.correct_answers}")
