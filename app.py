import streamlit as st
from db import init_db, insert_ticket, get_all_tickets

st.set_page_config(page_title="Help Desk", layout="wide")
st.title("🛠️ Help Desk Ticketing System")

init_db()

with st.form("ticket_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")  # Added email input
    dept = st.selectbox("Department", [
        "Alumni pathway", "Assessments", "Ceo office", "CDU", "DTT", "Audit", "Impact Interventions", "IT", "LLS",
        "Operations", "Research & Knowledge sharing", "Southern Zone", "HR", "Finance", "Brand & Communication",
        "Rabta", "Development Pakistan", "Donor Services", "Evp", "Engineering", "FSPD", "Global Partnership",
        "Supplychain", "Technology for Education", "Others"
    ])
    issue = st.text_area("Describe Issue")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if name and email and issue:
            insert_ticket(name, email, dept, issue)  # Pass as arguments, not a dict
            st.success("🎫 Ticket submitted successfully!")
        else:
            st.error("Please fill all fields.")

st.subheader("📋 Submitted Tickets")
tickets = get_all_tickets()

if tickets:
    st.dataframe(
        tickets,
        use_container_width=True,
        column_config={
            0: "ID",
            1: "Name",
            2: "Email",
            3: "Department",
            4: "Issue",
            5: "Created At"
        }
    )
else:
    st.info("No tickets submitted yet.")
