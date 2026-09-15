import streamlit as st

st.set_page_config(
    page_title="SafeSchool Emergency Dashboard",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 SafeSchool Emergency Dashboard")
st.subheader("Disaster Preparedness & Student Safety Monitoring")

st.divider()
total = 160
safe = 157
moving = 0
missing = 3

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Students", total)

with col2:
    st.metric("Safe", safe)

with col3:
    st.metric("Moving", moving)

with col4:
    st.metric("Missing", missing)

st.divider()

st.error("🔥 FIRE DETECTED")

st.subheader("Evacuation Status")

evacuation_percentage = (safe / total) * 100

st.progress(evacuation_percentage / 100)

st.write(f"Evacuation Progress: {evacuation_percentage:.1f}%")

st.divider()

st.subheader("Student Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.success(f"🟢 Safe\n\n{safe} students")

with col2:
    st.warning(f"🟡 Moving\n\n{moving} students")

with col3:
    st.error(f"🔴 Missing\n\n{missing} students")

st.divider()

st.info(
    "This dashboard displays the current state of students "
    "during an emergency simulation."
)