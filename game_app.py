
import streamlit as st
import random

# Initialize session state
if "cases_solved" not in st.session_state:
    st.session_state.cases_solved = 0
    st.session_state.suspicion = 0
    st.session_state.case_number = 1
    st.session_state.current_case = None
    st.session_state.history = []

# Generate a new case
def generate_case():
    criminals = ["John Doe", "Maria Lopez", "Igor Petrov", "Chen Wei", "Carlos Mendes"]
    schemes = ["Shell Companies", "Casinos", "Real Estate", "Trade-Based Laundering", "Offshore Accounts"]
    locations = ["New York", "London", "Dubai", "Hong Kong", "Panama"]
    
    case = {
        "criminal": random.choice(criminals),
        "scheme": random.choice(schemes),
        "location": random.choice(locations),
        "transactions": random.randint(100, 500),
        "amount": random.randint(50000, 500000),
        "risk_level": random.randint(20, 80),
    }
    return case

# Start a new case if none exists
if not st.session_state.current_case:
    st.session_state.current_case = generate_case()

# Display case details
case = st.session_state.current_case
st.title("🕵️ Financial Crimes Unit: Money Laundering Investigation")
st.subheader(f"📂 Case #{st.session_state.case_number}")
st.write(f"**Suspect:** {case['criminal']}")
st.write(f"**Suspicious Scheme:** {case['scheme']}")
st.write(f"**Location:** {case['location']}")
st.write(f"**Number of Transactions:** {case['transactions']}")
st.write(f"**Total Amount:** ${case['amount']:,}")
st.write(f"**Risk Level:** {case['risk_level']}%")

# Player decisions
st.subheader("What action will you take?")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Analyze Transactions"):
        case['risk_level'] += 10
        st.success("You've found suspicious patterns in the transactions!")

with col2:
    if st.button("🔎 Conduct Surveillance"):
        if random.randint(1, 100) < case['risk_level']:
            st.success("Surveillance revealed key evidence against the suspect!")
            case['risk_level'] += 20
        else:
            st.warning("The suspect noticed the surveillance and changed tactics!")

with col3:
    if st.button("🚔 Freeze Accounts"):
        if case['risk_level'] > 50:
            st.success(f"🚨 {case['criminal']} was arrested! Case closed.")
            st.session_state.cases_solved += 1
            st.session_state.history.append(f"Case #{st.session_state.case_number}: {case['criminal']} caught")
        else:
            st.error("❌ Not enough evidence! The suspect escaped, and your reputation suffered.")
            st.session_state.suspicion += 10
            st.session_state.history.append(f"Case #{st.session_state.case_number}: {case['criminal']} escaped")

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
