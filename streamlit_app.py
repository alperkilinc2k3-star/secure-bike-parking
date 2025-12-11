import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ==================== TITEL ====================
st.title("🚲 Secure Bike Parking System")
st.write("A prototype that tracks user IDs and available parking slots.")

TOTAL_SLOTS = 30

# ==================== SESSION STATE ====================
if "slots" not in st.session_state:
    st.session_state.slots = {i: None for i in range(1, TOTAL_SLOTS + 1)}
if "logs" not in st.session_state:
    st.session_state.logs = []

# ==================== STUDENT ENTRY ====================
st.markdown("### 🔐 Student Entry")
student_id = st.text_input("Enter student ID", key="id_input")

col1, col2 = st.columns(2)

with col1:
    if st.button("Park Bike", type="primary"):
        if not student_id.strip():
            st.error("Enter a student ID first!")
        else:
            empty = [s for s, u in st.session_state.slots.items() if u is None]
            if not empty:
                st.error("No free slots!")
            else:
                slot = empty[0]
                st.session_state.slots[slot] = student_id
                st.session_state.logs.append({"time": datetime.now().strftime("%H:%M:%S"),
                                            "slot": slot, "id": student_id, "action": "Park"})
                st.success(f"Parked at slot {slot}")
                st.rerun()

with col2:
    if st.button("Remove Bike"):
        if not student_id.strip():
            st.error("Enter a student ID first!")
        else:
            taken = [s for s, u in st.session_state.slots.items() if u == student_id]
            if not taken:
                st.warning("No bike found for this ID")
            else:
                slot = taken[0]
                st.session_state.slots[slot] = None
                st.session_state.logs.append({"time": datetime.now().strftime("%H:%M:%S"),
                                            "slot": slot, "id": student_id, "action": "Remove"})
                st.success(f"Removed from slot {slot}")
                st.rerun()

# ==================== STATUS ====================
st.markdown("### 📋 Current Parking Status")
df_status = pd.DataFrame({
    "Slot": list(st.session_state.slots.keys()),
    "Status": ["Free" if v is None else f"Taken ({v})" for v in st.session_state.slots.values()]
})
st.dataframe(df_status, use_container_width=True)

free = sum(1 for v in st.session_state.slots.values() if v is None)
taken = TOTAL_SLOTS - free
c1, c2 = st.columns(2)
c1.metric("Free Slots", free)
c2.metric("Occupied Slots", taken)

# ==================== GRAFIEK 1 ====================
st.markdown("### 📊 Slot Usage")
fig, ax = plt.subplots()
ax.bar(["Free", "Occupied"], [free, taken], color=["#66bb6a", "#ef5350"])
ax.set_ylabel("Slots")
st.pyplot(fig)

# ==================== LOG & GRAFIEK 2 ====================
st.markdown("## 📄 Event Log")
if st.session_state.logs:
    df_log = pd.DataFrame(st.session_state.logs)
    st.dataframe(df_log, use_container_width=True)

    st.markdown("## 📈 Activity per Hour")
    df_log["hour"] = pd.to_datetime(df_log["time"], format="%H:%M:%S").dt.hour
    hourly = df_log.groupby(["hour", "action"]).size().unstack(fill_value=0)
    fig2, ax2 = plt.subplots()
    hourly.plot(kind="bar", stacked=True, ax=ax2, color={"Park": "#66bb6a", "Remove": "#ef5350"})
    ax2.set_xlabel("Hour")
    ax2.set_ylabel("Actions")
    st.pyplot(fig2)
else:
    st.info("No activity yet.")
