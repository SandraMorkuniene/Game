
import streamlit as st
import random
import pandas as pd
#import plotly.express as px

# Initialize session state variables
if "cases_solved" not in st.session_state:
    st.session_state.cases_solved = 0
    st.session_state.suspicion = 0
    st.session_state.case_number = 1
    st.session_state.current_case = None
    st.session_state.history = []

# Generate fake transaction data
def generate_transactions():
    num_transactions = random.randint(5, 15)
    data = {
        "Date": pd.date_range(start="2024-01-01", periods=num_transactions).strftime('%Y-%m-%d').tolist(),
        "Amount": [random.randint(5000, 50000) for _ in range(num_transactions)],
        "Destination": random.choices(["Shell Company", "Offshore Account", "Luxury Goods", "Legitimate Business"], k=num_transactions),
    }
    return pd.DataFrame(data)

# Generate a new case
def generate_case():
    suspects = ["John Doe", "Maria Lopez", "Igor Petrov", "Chen Wei", "Carlos Mendes"]
    schemes = ["Shell Companies", "Casinos", "Real Estate", "Trade-Based Laundering", "Offshore Accounts"]
    locations = ["New York", "London", "Dubai", "Hong Kong", "Panama"]
    
    case = {
        "suspect": random.choice(suspects),
        "scheme": random.choice(schemes),
        "location": random.choice(locations),
        "transactions": generate_transactions(),
        "risk_score": random.randint(20, 90),
        "is_guilty": random.choice([True, False]),  # Some cases are false alarms!
    }
    return case

# Start a new case if none exists
if not st.session_state.current_case:
    st.session_state.current_case = generate_case()

# Display case details
case = st.session_state.current_case
st.title("🕵️ Financial Crimes Unit: Money Laundering Investigation")
st.subheader(f"📂 Case #{st.session_state.case_number}")
st.write(f"**Suspect:** {case['suspect']}")
st.write(f"**Suspicious Scheme:** {case['scheme']}")
st.write(f"**Location:** {case['location']}")
st.write(f"**Risk Score:** {case['risk_score']}%")

# Show transaction data
st.subheader("📊 Transaction Analysis")
st.dataframe(case["transactions"])

# Plot transaction amounts
#fig = px.bar(case["transactions"], x="Date", y="Amount", color="Destination", title="Transaction Flow")
#t.plotly_chart(fig)

# Player decisions
st.subheader("What action will you take?")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Analyze Transactions"):
        if case['risk_score'] > 50:
            st.success("Red flags detected! High-risk transactions found.")
        else:
            st.warning("Transactions appear normal. Need more evidence.")

with col2:
    if st.button("🔎 Conduct Surveillance"):
        if case['is_guilty']:
            st.success("Surveillance confirms illegal activities!")
            case['risk_score'] += 20
        else:
            st.warning("Nothing suspicious found.")

with col3:
    if st.button("🚔 Freeze Accounts & Arrest"):
        if case["is_guilty"] and case["risk_score"] > 50:
            st.success(f"🚨 {case['suspect']} was arrested! Case closed.")
            st.session_state.cases_solved += 1
            st.session_state.history.append(f"Case #{st.session_state.case_number}: {case['suspect']} caught")
        elif not case["is_guilty"]:
            st.error("❌ Wrongful arrest! Your reputation suffers.")
            st.session_state.suspicion += 15
            st.session_state.history.append(f"Case #{st.session_state.case_number}: Wrongful arrest")
        else:
            st.error("❌ Not enough evidence! The suspect escaped.")
            st.session_state.suspicion += 10
            st.session_state.history.append(f"Case #{st.session_state.case_number}: Suspect escaped")

        # Move to next case
        st.session_state.case_number += 1
        st.session_state.current_case = generate_case()

# Sidebar with stats
st.sidebar.header("📊 Investigator Stats")
st.sidebar.write(f"✅ Cases Solved: {st.session_state.cases_solved}")
st.sidebar.write(f"⚠️ Suspicion Level: {st.session_state.suspicion}%")

# Show history
st.sidebar.subheader("📜 Case History")
for entry in st.session_state.history:
    st.sidebar.write(entry)

# Endgame scenarios
if st.session_state.suspicion >= 50:
    st.error("❌ Your division has been shut down due to too many failed investigations! Game Over.")
    if st.button("🔄 Restart Game"):
        st.session_state.cases_solved = 0
        st.session_state.suspicion = 0
        st.session_state.case_number = 1
        st.session_state.current_case = None
        st.session_state.history = []
        st.experimental_rerun()
