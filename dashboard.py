import streamlit as st
import pandas as pd

from modules.database import create_tables, add_sample_data
from modules.simulation import EvacuationSimulator

st.set_page_config(
    page_title="SafeSchool Emergency Dashboard",
    page_icon="🚨",
    layout="wide"
)

create_tables()
add_sample_data()

if "simulator" not in st.session_state:
    st.session_state.simulator = EvacuationSimulator()

if "simulation_started" not in st.session_state:
    st.session_state.simulation_started = False

simulator = st.session_state.simulator


st.title(" SafeSchool Emergency Dashboard")

st.caption(
    "Disaster Preparedness and Student Safety Monitoring System"
)

st.divider()
st.subheader(" Select Disaster Scenario")

col1, col2 = st.columns(2)

with col1:

    disaster_type = st.selectbox(
        "Select Disaster Type",
        [
            "Fire",
            "Earthquake",
            "Flood"
        ]
    )


with col2:

    affected_building = st.selectbox(
        "Select Affected Building",
        [
            "Block A",
            "Block B",
            "Block C"
        ]
    )

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        " Start Disaster",
        width="stretch"
    ):

        simulator.start_disaster(
            disaster_type,
            affected_building
        )

        st.session_state.simulation_started = True

        st.rerun()


with col2:

    if st.button(
        "⏱️ Advance 5 Seconds",
        width="stretch"
    ):

        if st.session_state.simulation_started:

            simulator.advance(5)

            st.rerun()

        else:

            st.warning(
                "Please start a disaster first."
            )


with col3:

    if st.button(
        "🔄 Reset Simulation",
        width="stretch"
    ):

        st.session_state.simulator = EvacuationSimulator()

        st.session_state.simulation_started = False

        st.rerun()


if st.session_state.simulation_started:

    st.divider()

    st.error(
        f" {simulator.disaster_type.upper()} DETECTED"
    )

    st.write(
        f"**Affected Building:** "
        f"{simulator.affected_building}"
    )

    st.write(
        f"**Elapsed Time:** "
        f"{simulator.elapsed_seconds} seconds"
    )


counts = simulator.get_counts()

total = counts["total"]
safe = counts["safe"]
moving = counts["moving"]
missing = counts["missing"]


st.divider()

st.subheader("👨‍🎓 Student Safety Status")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Students",
        total
    )


with col2:

    st.metric(
        "🟢 Safe",
        safe
    )


with col3:

    st.metric(
        "🟡 Moving",
        moving
    )


with col4:

    st.metric(
        "🔴 Missing",
        missing
    )

if total > 0:

    evacuation_percentage = (
        safe / total
    ) * 100

else:

    evacuation_percentage = 0


st.subheader("📊 Evacuation Progress")

st.progress(
    evacuation_percentage / 100
)

st.write(
    f"Evacuation Progress: "
    f"**{evacuation_percentage:.1f}%**"
)


st.divider()

st.subheader("👥 Student Status")


students = simulator.get_students()


df = pd.DataFrame(students)


if not df.empty:

    display_df = df[
        [
            "student_id",
            "student_name",
            "class_name",
            "building",
            "status"
        ]
    ]

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )


st.divider()

st.subheader("📌 Status Summary")


col1, col2, col3 = st.columns(3)


with col1:

    st.success(
        f"🟢 Safe Students: {safe}"
    )


with col2:

    st.warning(
        f"🟡 Students Moving: {moving}"
    )


with col3:

    if missing > 0:

        st.error(
            f"🔴 Missing Students: {missing}"
        )

    else:

        st.success(
            "🔴 Missing Students: 0"
        )