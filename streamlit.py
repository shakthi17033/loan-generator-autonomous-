import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Autonomous Loan Agentic System", layout="wide")

st.title("🏦 Autonomous Loan Origination Agentic System")

# -------------------------------
# AGENT 1: Application Agent
# -------------------------------
def application_agent(form_data):
    if form_data["age"] < 18:
        return False, "Applicant must be 18+"
    if form_data["income"] <= 0:
        return False, "Income must be greater than 0"
    return True, "Application validated"

# -------------------------------
# AGENT 2: Document Verification Agent
# -------------------------------
def document_agent(uploaded_file):
    if uploaded_file is None:
        return False, "No document uploaded"
    return True, "Document verified (Simulated)"

# -------------------------------
# AGENT 3: Credit Evaluation Agent
# -------------------------------
def credit_agent(cibil_score):
    if cibil_score >= 750:
        return "Excellent"
    elif cibil_score >= 650:
        return "Good"
    elif cibil_score >= 550:
        return "Average"
    else:
        return "Poor"

# -------------------------------
# AGENT 4: Risk Assessment Agent
# -------------------------------
def risk_agent(income, emi, loan_amount, cibil_score):
    dti_ratio = emi / income if income > 0 else 1
    risk_score = (loan_amount / income) * 0.4 + dti_ratio * 0.3 + (750 - cibil_score) * 0.3
    return round(risk_score, 2)

# -------------------------------
# AGENT 5: Decision Agent
# -------------------------------
def decision_agent(risk_score, credit_category):
    if risk_score < 5 and credit_category in ["Excellent", "Good"]:
        return "✅ Approved"
    elif risk_score < 8:
        return "⚠️ Conditional Approval"
    else:
        return "❌ Rejected"

# -------------------------------
# STREAMLIT UI
# -------------------------------

st.header("Loan Application Form")

with st.form("loan_form"):
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=18, max_value=100)
    income = st.number_input("Monthly Income")
    existing_emi = st.number_input("Existing EMI")
    loan_amount = st.number_input("Requested Loan Amount")
    tenure = st.number_input("Loan Tenure (Months)")
    cibil_score = st.slider("CIBIL Score", 300, 900, 700)
    uploaded_file = st.file_uploader("Upload Salary Slip (PDF)")
    
    submit = st.form_submit_button("Run Loan Agents")

if submit:

    st.subheader("🔄 Agent Processing Logs")

    form_data = {
        "name": name,
        "age": age,
        "income": income
    }

    # Run Application Agent
    valid, app_msg = application_agent(form_data)
    st.write("Application Agent:", app_msg)

    if not valid:
        st.stop()

    # Run Document Agent
    doc_valid, doc_msg = document_agent(uploaded_file)
    st.write("Document Agent:", doc_msg)

    if not doc_valid:
        st.stop()

    # Run Credit Agent
    credit_category = credit_agent(cibil_score)
    st.write("Credit Agent:", credit_category)

    # Run Risk Agent
    risk_score = risk_agent(income, existing_emi, loan_amount, cibil_score)
    st.write("Risk Agent Score:", risk_score)

    # Run Decision Agent
    decision = decision_agent(risk_score, credit_category)

    st.subheader("🏁 Final Decision")
    st.success(decision)

    st.subheader("📊 Summary")
    summary_df = pd.DataFrame({
        "Metric": ["Credit Category", "Risk Score", "Decision"],
        "Value": [credit_category, risk_score, decision]
    })
    st.table(summary_df)