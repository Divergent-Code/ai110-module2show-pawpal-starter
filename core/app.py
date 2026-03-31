import streamlit as st
from core import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Initialize Session State ---
# We store the Owner object in session state so data persists between button clicks
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

# --- UI Header ---
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

# Display current pets
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
        task_title = st.text_input("Task Description (e.g., Morning Walk)")
        task_time = st.time_input("Time")
    with col2:
        selected_pet_name = st.selectbox("Assign to Pet", [p.name for p in owner.pets])
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
        task_freq = st.selectbox("Frequency", ["Daily", "Weekly", "Once"])

    if st.button("Add Task"):
        if task_title:
            # Format time to HH:MM string to match our class design
            time_str = task_time.strftime("%H:%M")
            new_task = Task(description=task_title, time=time_str, frequency=task_freq, priority=task_priority)
            
            # Find the correct pet object and add the task
            for p in owner.pets:
                if p.name == selected_pet_name:
                    p.add_task(new_task)
                    st.success(f"Added '{task_title}' to {p.name}'s schedule at {time_str}!")
        else:
            st.error("Please enter a task description.")

st.divider()

# --- Section 3: The Scheduler Engine ---
st.subheader("3. Today's Schedule")
st.caption("Powered by the PawPal+ Scheduler Brain")

sort_method = st.radio("Sorting Method:", ["Chronological (By Time)", "Smart (Priority, then Time)"], horizontal=True)

if st.button("Generate Schedule", type="primary"):
    brain = Scheduler(owner)
    all_tasks = brain.get_all_tasks()
    
    if not all_tasks:
        st.info("No tasks scheduled for today. You're all caught up!")
    else:
        # Determine sorting logic based on UI selection
        if "Smart" in sort_method:
            scheduled_tasks = brain.sort_by_priority_then_time(all_tasks)
        else:
            scheduled_tasks = brain.sort_by_time(all_tasks)
            
        # Check for conflicts
        conflicts = brain.detect_conflicts(all_tasks)
        if conflicts:
            st.warning(f"⚠️ Warning: We detected {len(conflicts)} scheduling conflict(s)! Check your times.")

        # Display Schedule
        st.markdown("### 📋 Your Itinerary")
        for task in scheduled_tasks:
            # We can figure out which pet this task belongs to for the UI
            pet_owner_name = "Unknown Pet"
            for p in owner.pets:
                if task in p.tasks:
                    pet_owner_name = p.name
                    break
            
            # Create a nice UI box for each task
            status = "✅" if task.completed else "⏳"
            st.markdown(f"**{task.time}** | {status} | **{task.priority} Priority** | {task.description} *(for {pet_owner_name})*")

# --- Save Data (Optional bonus matching UML) ---
st.divider()
if st.button("Save Data to JSON"):
    owner.save_to_json("pawpal_data.json")
    st.success("Data saved successfully!")