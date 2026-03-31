# app.py
import streamlit as st
from datetime import datetime
from core import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

st.title("🐾 PawPal+ Dashboard")
st.markdown(f"**Welcome back, {owner.name}!** Let's organize your pet care today.")

# --- Section 1: Manage Pets ---
st.subheader("1. Your Pets")

with st.expander("Add a New Pet"):
    pet_name = st.text_input("Pet Name")
    pet_species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
    if st.button("Add Pet"):
        if pet_name:
            new_pet = Pet(name=pet_name, species=pet_species)
            owner.add_pet(new_pet)
            st.success(f"Added {pet_name} the {pet_species}!")
        else:
            st.error("Please enter a pet name.")

if owner.pets:
    pet_names = [p.name for p in owner.pets]
    st.write("Current Pets:", ", ".join(pet_names))
else:
    st.info("You don't have any pets yet. Add one above!")

st.divider()

# --- Section 2: Manage Tasks ---
st.subheader("2. Add Care Tasks")

if not owner.pets:
    st.warning("Please add a pet first before creating tasks.")
else:
    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Task Description (e.g., Vet Appointment)")
        task_time = st.time_input("Time")
        selected_pet_name = st.selectbox("Assign to Pet", [p.name for p in owner.pets])
        
    with col2:
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
        task_freq = st.selectbox("Frequency", ["Daily", "Weekly", "Once"])
        
        # NEW: Dynamic inputs based on frequency
        target_day = None
        target_date = None
        
        if task_freq == "Weekly":
            target_day = st.selectbox("Day of the Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        elif task_freq == "Once":
            target_date_obj = st.date_input("Select Date")
            target_date = target_date_obj.strftime("%Y-%m-%d")

    if st.button("Add Task"):
        if task_title:
            time_str = task_time.strftime("%H:%M")
            new_task = Task(
                description=task_title, 
                time=time_str, 
                frequency=task_freq, 
                priority=task_priority,
                target_day=target_day,
                target_date=target_date
            )
            
            for p in owner.pets:
                if p.name == selected_pet_name:
                    p.add_task(new_task)
                    st.success(f"Added '{task_title}' to {p.name}'s schedule!")
        else:
            st.error("Please enter a task description.")

st.divider()

# --- Section 3: The Scheduler Engine ---
st.subheader("3. Schedule Viewer")

# NEW: Let the user pick which day they want to look at
view_date = st.date_input("Select a day to view its schedule", value=datetime.today())
sort_method = st.radio("Sorting Method:", ["Chronological (By Time)", "Smart (Priority, then Time)"], horizontal=True)

if st.button("Generate Schedule", type="primary"):
    brain = Scheduler(owner)
    
    # NEW: Convert Streamlit's date to a datetime object so our Brain can read it
    target_datetime = datetime.combine(view_date, datetime.min.time())
    daily_tasks = brain.get_schedule_for_date(target_datetime)
    
    if not daily_tasks:
        st.info("No tasks scheduled for this day. You're all caught up!")
    else:
        if "Smart" in sort_method:
            scheduled_tasks = brain.sort_by_priority_then_time(daily_tasks)
        else:
            scheduled_tasks = brain.sort_by_time(daily_tasks)

        # NEW: Display the specific date chosen
        st.markdown(f"### 📋 Itinerary for {view_date.strftime('%A, %b %d, %Y')}")
        for task in scheduled_tasks:
            pet_owner_name = "Unknown Pet"
            for p in owner.pets:
                if task in p.tasks:
                    pet_owner_name = p.name
                    break
            
            status = "✅" if task.completed else "⏳"
            freq_tag = f"[{task.frequency}]"
            
            st.markdown(f"**{task.time}** {freq_tag} | {status} | **{task.priority} Priority** | {task.description} *(for {pet_owner_name})*")

st.divider()
if st.button("Save Data to JSON"):
    owner.save_to_json("pawpal_data.json")
    st.success("Data saved successfully!")