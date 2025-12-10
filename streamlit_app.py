import streamlit as st
import pandas as pd

# --- Başlık ---
st.title("🚲 Secure Bike Parking System")
st.write("A prototype that tracks user IDs and available parking slots.")

# --- Başlangıç veri yapısı ---
TOTAL_SLOTS = 30

if "slots" not in st.session_state:
    st.session_state.slots = {i: None for i in range(1, TOTAL_SLOTS + 1)}  # 1–30 arası boş yerler

# --- Öğrenci giriş alanı ---
st.write("### 🔐 Student Entry")

student_id = st.text_input("Enter student ID")

col1, col2 = st.columns(2)

# --- Giriş (bisikleti park et) butonu ---
with col1:
    if st.button("Park Bike"):
        if not student_id:
            st.error("Please enter a student ID.")
        else:
            # Boş slot bul
            empty_slots = [slot for slot, user in st.session_state.slots.items() if user is None]
            
            if len(empty_slots) == 0:
                st.error("❌ No empty slots available!")
            else:
                assigned_slot = empty_slots[0]
                st.session_state.slots[assigned_slot] = student_id
                st.success(f"Bike parked at slot **{assigned_slot}**")

# --- Çıkış (bisikleti al) butonu ---
with col2:
    if st.button("Remove Bike"):
        if not student_id:
            st.error("Please enter a student ID.")
        else:
            # Öğrencinin kullandığı slotu bul
            user_slots = [slot for slot, user in st.session_state.slots.items() if user == student_id]
            if len(user_slots) == 0:
                st.warning("This student does not have a bike inside.")
            else:
                slot_to_free = user_slots[0]
                st.session_state.slots[slot_to_free] = None
                st.success(f"Bike removed from slot **{slot_to_free}**")

# --- Durum tablosu ---
st.write("### 📋 Current Parking Status")

data = {
    "Slot": list(st.session_state.slots.keys()),
    "Status": ["Free" if user is None else f"Taken by {user}" for user in st.session_state.slots.values()]
}

df = pd.DataFrame(data)
st.dataframe(df)

# --- Boş / Dolu özet ---
free = sum(1 for v in st.session_state.slots.values() if v is None)
taken = TOTAL_SLOTS - free

st.write("### 📊 Summary")
st.metric("Free Slots", free)
st.metric("Occupied Slots", taken)
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime

# --- LOG INITIALISATION ---
if "logs" not in st.session_state:
    st.session_state.logs = []

st.write("## 👤 Customer Entry / Exit")

customer_id = st.text_input("Customer ID")
selected_slot = st.selectbox("Select Slot", list(st.session_state.slots.keys()))
action = st.radio("Action", ["Enter", "Exit"])

if st.button("Confirm Action"):
    if customer_id.strip() == "":
        st.warning("Customer ID cannot be empty.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Slot status update
        if action == "Enter":
            st.session_state.slots[selected_slot] = customer_id
        else:
            st.session_state.slots[selected_slot] = None

        # Add to logs
        st.session_state.logs.append({
            "time": timestamp,
            "slot": selected_slot,
            "customer": customer_id,
            "action": action
        })

        st.success(f"{action} recorded for customer {customer_id} on slot {selected_slot}")

# --- DISPLAY LOG TABLE ---
st.write("## 📄 Event Log")
df_logs = pd.DataFrame(st.session_state.logs)
st.dataframe(df_logs)

# --- GRAPH: ENTRIES/EXITS PER HOUR ---
if len(df_logs) > 0:
    st.write("## 📊 Entry/Exit Frequency")

    df_logs["hour"] = pd.to_datetime(df_logs["time"]).dt.hour

    hourly = df_logs.groupby(["hour", "action"]).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(8, 4))
    hourly.plot(ax=ax)
    ax.set_title("Entries and Exits Per Hour")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Count")

    st.pyplot(fig)
else:
    st.info("No events recorded yet.")
# --- 📊 Grafiek: Bezet / Vrij Slots ---
import matplotlib.pyplot as plt

st.write("### 📊 Slot Usage Chart")

fig, ax = plt.subplots()

labels = ["Free Slots", "Occupied Slots"]
values = [free, taken]

ax.bar(labels, values)
ax.set_ylabel("Number of Slots")
ax.set_title("Parking Slot Usage Overview")

st.pyplot(fig)
# --- 📊 Grafiek: Free vs Occupied ---
import matplotlib.pyplot as plt

# Data voor grafiek
labels = ['Free Slots', 'Occupied Slots']
values = [free, taken]

fig, ax = plt.subplots()
ax.bar(labels, values)
ax.set_ylabel("Aantal")
ax.set_title("Parking Slot Overview")

st.pyplot(fig)
