import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- Titel ---
st.title("🚲 Secure Bike Parking System")
st.write("A prototype that tracks user IDs and available parking slots.")

# --- Basisinstellingen ---
TOTAL_SLOTS = 30

# Session state initialiseren
if "slots" not in st.session_state:
    st.session_state.slots = {i: None for i in range(1, TOTAL_SLOTS + 1)}

if "logs" not in st.session_state:
    st.session_state.logs = []

# --- Student Entry ---
st.write("### 🔐 Student Entry")
student_id = st.text_input("Enter student ID")

col1, col2 = st.columns(2)

with col1:
    if st.button("Park Bike"):
        if not student_id.strip():
            st.error("Please enter a student ID.")
        else:
            empty_slots = [s for s, user in st.session_state.slots.items() if user is None]
            if not empty_slots:
                st.error("❌ No empty slots available!")
            else:
                slot = empty_slots[0]
                st.session_state.slots[slot] = student_id
                st.success(f"Bike parked at slot **{slot}**")
                st.session_state.logs.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "slot": slot,
                    "customer": student_id,
                    "action": "Enter"
                })

with col2:
    if st.button("Remove Bike"):
        if not student_id.strip():
            st.error("Please enter a student ID.")
        else:
            user_slots = [s for s, user in st.session_state.slots.items() if user == student_id]
            if not user_slots:
                st.warning("This student does not have a bike parked.")
            else:
                slot = user_slots[0]
                st.session_state.slots[slot] = None
                st.success(f"Bike removed from slot **{slot}**")
                st.session_state.logs.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "slot": slot,
                    "customer": student_id,
                    "action": "Exit"
                })

# --- Huidige status ---
st.write("### 📋 Current Parking Status")
data = {"Slot": list(st.session_state.slots.keys()),
        "Status": ["Free" if v is None else f"Taken by {v}" for v in st.session_state.slots.values()]}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# --- Samenvatting ---
free = sum(1 for v in st.session_state.slots.values() if v is None)
taken = TOTAL_SLOTS - free
col1, col2 = st.columns(2)
col1.metric("Free Slots", free)
col2.metric("Occupied Slots", taken)

# --- Grafiek 1: Free vs Occupied ---
st.write("### 📊 Slot Usage Overview")
fig, ax = plt.subplots()
ax.bar(["Free Slots", "Occupied Slots"], [free, taken], color=["#90EE90", "#FF6347"])
ax.set_ylabel("Number of Slots")
st.pyplot(fig)

# --- Event Log ---
st.write("## 📄 Event Log")
if st.session_state.logs:
    log_df = pd.DataFrame(st.session_state.logs)
    st.dataframe(log_df, use_container_width=True)

    # Grafiek: Entries/Exits per uur
    st.write("## 📈 Entries & Exits per Hour")
    log_df["hour"] = pd.to_datetime(log_df["time"]).dt.hour
    hourly = log_df.groupby(["hour", "action"]).size().unstack(fill_value=0)
    fig2, ax2 = plt.subplots()
    hourly.plot(kind="bar", ax=ax2, stacked=True, color=["#90EE90", "#FF6347"])
    ax2.set_xlabel("Hour of Day")
    ax2.set_ylabel("Number of Events")
    ax2.legend(title="Action")
    st.pyplot(fig2)
else:
    st.info("No events recorded yet.")
