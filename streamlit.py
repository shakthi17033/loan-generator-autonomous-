import streamlit as st
import pandas as pd
import json
from datetime import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Autonomous Loan Agentic System", layout="wide")

# Force white background
st.markdown(
    """
    <style>
        .stApp {
            background-color: white;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏦 Decision-Driven Agentic Loan Origination System")

# -----------------------------
# CONFIGURABLE POLICY RULES
# -----------------------------
policy_rules = {
    "min_cibil": 650,
    "max_dti_ratio": 0.5,
    "max_loan_to_income": 20,
    "max_age": 60
}

# -----------------------------
# AGENT 1: User Interaction Agent
# -----------------------------
def user_interaction_agent():
    st.header("📋 Loan Application Form")
    with st.form("loan_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=18, max_value=100)
        income = st.number_input("Monthly Income")
        existing_emi = st.number_input("Existing EMI")
        loan_amount = st.number_input("Requested Loan Amount")
        tenure = st.number_input("Loan Tenure (Months)")
        cibil_score = st.slider("CIBIL Score", 300, 900, 700)
        uploaded_file = st.file_uploader("Upload Income Proof (PDF)")
        submit = st.form_submit_button("Submit Application")

    return submit, {
        "name": name,
        "age": age,
        "income": income,
        "existing_emi": existing_emi,
        "loan_amount": loan_amount,
        "tenure": tenure,
        "cibil_score": cibil_score,
        "uploaded_file": uploaded_file
    }

# -----------------------------
# AGENT 2: Data Intake Agent
# -----------------------------
def data_intake_agent(data):
    errors = []
    if not data["name"]:
        errors.append("Name missing")
    if data["income"] <= 0:
        errors.append("Income must be greater than 0")
    if data["loan_amount"] <= 0:
        errors.append("Loan amount must be greater than 0")

    return len(errors) == 0, errors

# -----------------------------
# AGENT 3: Document Verification Agent
# -----------------------------
def document_verification_agent(uploaded_file):
    if uploaded_file is None:
        return False, "No document uploaded"
    return True, "Document verified (Simulated)"

# -----------------------------
# AGENT 4: Policy Compliance Agent
# -----------------------------
def policy_compliance_agent(data):
    violations = []

    dti_ratio = data["existing_emi"] / data["income"] if data["income"] > 0 else 1
    loan_income_ratio = data["loan_amount"] / data["income"]

    if data["cibil_score"] < policy_rules["min_cibil"]:
        violations.append("CIBIL score below minimum threshold")

    if dti_ratio > policy_rules["max_dti_ratio"]:
        violations.append("Debt-to-Income ratio exceeds policy limit")

    if loan_income_ratio > policy_rules["max_loan_to_income"]:
        violations.append("Loan-to-Income ratio exceeds policy limit")

    if data["age"] > policy_rules["max_age"]:
        violations.append("Applicant age exceeds maximum allowed")

    return len(violations) == 0, violations, round(dti_ratio, 2)

# -----------------------------
# AGENT 5: Decision & Explanation Agent
# -----------------------------
def decision_agent(is_valid, policy_pass, violations, dti_ratio, data):
    if not is_valid:
        return "Rejected", "Application validation failed."

    if not policy_pass:
        explanation = f"Loan Rejected due to: {', '.join(violations)}."
        return "Rejected", explanation

    explanation = (
        f"Loan Approved. Applicant has CIBIL score of {data['cibil_score']} "
        f"and Debt-to-Income ratio of {dti_ratio}, within acceptable limits."
    )
    return "Approved", explanation

# -----------------------------
# MAIN EXECUTION
# -----------------------------
submit, data = user_interaction_agent()

if submit:
    st.subheader("🔄 Agent Execution Logs")

    # Data Intake
    valid, errors = data_intake_agent(data)
    if valid:
        st.success("Data Intake Agent: Validation Passed")
    else:
        st.error(f"Data Intake Agent Errors: {errors}")

    # Document Agent
    doc_valid, doc_msg = document_verification_agent(data["uploaded_file"])
    if doc_valid:
        st.success(f"Document Agent: {doc_msg}")
    else:
        st.error(f"Document Agent: {doc_msg}")

    # Policy Agent
    policy_pass, violations, dti_ratio = policy_compliance_agent(data)
    if policy_pass:
        st.success("Policy Compliance Agent: All checks passed")
    else:
        st.error(f"Policy Violations: {violations}")

    # Decision Agent
    decision, explanation = decision_agent(valid and doc_valid, policy_pass, violations, dti_ratio, data)

    st.subheader("🏁 Final Decision")
    if decision == "Approved":
        st.success(decision)
    else:
        st.error(decision)

    st.write("📝 Explanation:")
    st.write(explanation)

    # Human-in-loop override
    if decision == "Rejected":
        st.subheader("👤 Human Review Option")
        override = st.checkbox("Override and Approve Loan")
        if override:
            st.success("Loan Approved by Human Credit Manager Override")

    # Decision Log
    log_data = {
        "Name": data["name"],
        "Decision": decision,
        "Explanation": explanation,
        "Timestamp": datetime.now()
    }

    log_df = pd.DataFrame([log_data])
    st.subheader("📊 Decision Log")
    st.table(log_df)
