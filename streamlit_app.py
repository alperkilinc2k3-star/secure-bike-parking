import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ==================== TITLE ====================
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
student_id = st.text_input("Enter student ID")

col1, col2 = st.columns(2)

with col1:
    if st.button("Park Bike", type="primary"):
        if not student_id.strip():
            st.error("Please enter a student ID.")
        else:
            empty = [s for s, u in st.session_state.slots.items() if u is None]
            if not empty:
                st.error("❌ No free slots available!")
            else:
                slot = empty[0]
                st.session_state.slots[slot] = student_id
                st.session_state.logs.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                             "slot": slot, "customer": student_id, "action": "Enter"})
                st.success(f"Bike parked at slot **{slot}**")
                st.rerun()

with col2:
    if st.button("Remove Bike"):
        if not student_id.strip():
            st.error("Please enter a student ID.")
        else:
            taken = [s for s, u in st.session_state.slots.items() if u == student_id]
            if not taken:
                st.warning("No bike found for this ID.")
            else:
                slot = taken[0]
                st.session_state.slots[slot] = None
                st.session_state.logs.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                             "slot": slot, "customer": student_id, "action": "Exit"})
                st.success(f"Bike removed from slot **{slot}**")
                st.rerun()

# ==================== CURRENT STATUS ====================
st.markdown("### 📋 Current Parking Status")
data = {"Slot": list(st.session_state.slots.keys()),
        "Status": ["Free" if v is None else f"Taken by {v}" for v in st.session_state.slots.values()]}
st.dataframe(pd.DataFrame(data), use_container_width=True)

free = sum(1 for v in st.session_state.slots.values() if v is None)
taken = TOTAL_SLOTS - free
c1, c2 = st.columns(2)
c1.metric("Free Slots", free)
c2.metric("Occupied Slots", taken)

# ==================== GRAFIEK 1 ====================
st.markdown("### 📊 Parking Slot Overview")
fig, ax = plt.subplots()
ax.bar(["Free Slots", "Occupied Slots"], [free, taken], color=["#4CAF50", "#F44336"])
ax.set_ylabel("Number of Slots")
st.pyplot(fig)

# ==================== EVENT LOG & GRAFIEK 2 ====================
st.markdown("## 📄 Event Log")
if st.session_state.logs:
    log_df = pd.DataFrame(st.session_state.logs)
    st.dataframe(log_df, use_container_width=True)

    st.markdown("## 📈 Entries vs Exits per Hour")
    log_df["hour"] = pd.to_datetime(log_df["time"]).dt.hour
    hourly = log_df.groupby(["hour", "action"]).size().unstack(fill_value=0)
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    hourly.plot(kind="bar", stacked=True, ax=ax2, color={"Enter": "#4CAF50", "Exit": "#F44336"})
    ax2.set_xlabel("Hour")
    ax2.set_ylabel("Events")
    st.pyplot(fig2)
else:
    st.info("No events recorded yet.")
