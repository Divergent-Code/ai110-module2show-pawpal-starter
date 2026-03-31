"""
app.py

Primary reactive UI for the application using Streamlit.
Streamlit executes top-to-bottom on every user interaction, so `st.session_state` 
is used to persist the central `Owner` object across reruns.
"""
import os
from datetime import datetime
import streamlit as st
from core import Owner, Pet, Task, Scheduler


# --- Constants ---
PRIORITY_ICONS = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
DEFAULT_PRIORITY_ICON = "⚪"


def get_pet_for_task(owner: Owner, task: Task) -> str:
    """Finds the pet name that owns the given task."""
    for pet in owner.pets:
        if task in pet.tasks:
            return pet.name
    return "Unknown Pet"


def format_freq_tag(task: Task) -> str:
    """Builds a frequency tag for display."""
    if task.frequency == "Daily":
        return "[Daily]"
    if task.frequency == "Weekly":
        return f"[Weekly: {task.target_day}]"
    return f"[Once: {task.target_date}]"


def render_login_page():
    """Renders the profile creation/loading page."""
    st.title("🐾 Welcome to PawPal+")
    st.markdown("Please load an existing profile or create a new one to get started.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Create New Profile")
        new_name = st.text_input("Your Name:")
        if st.button("Create Profile"):
            if new_name.strip():
                st.session_state.owner = Owner(name=new_name.strip())
                st.rerun()
            st.error("Please enter a name.")
            
    with col2:
        st.subheader("Load Existing Profile")
        load_name = st.text_input("Existing Profile Name:")
        if st.button("Load Profile"):
            name = load_name.strip()
            if not name:
                st.error("Please enter a name.")
            else:
                filename = f"{name}_pawpal_data.json"
                if os.path.exists(filename):
                    st.session_state.owner = Owner.load_from_json(filename)
                    st.rerun()
                st.error(f"Could not find {filename}.")
                
    st.stop()


def render_sidebar(owner: Owner):
    """Renders the sidebar with profile info."""
    with st.sidebar:
        st.markdown(f"**Current Profile:** {owner.name}")
        if st.button("Switch Profile"):
            st.session_state.owner = None
            st.rerun()


def render_pet_section(owner: Owner):
    """Renders the pet management section."""
    st.subheader("1. Your Pets")

    with st.expander("Add a New Pet"):
        pet_name = st.text_input("Pet Name")
        pet_species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
        if st.button("Add Pet"):
            if pet_name:
                owner.add_pet(Pet(name=pet_name, species=pet_species))
                st.success(f"Added {pet_name} the {pet_species}!")
            else:
                st.error("Please enter a pet name.")

    if owner.pets:
        st.write("Current Pets:", ", ".join(p.name for p in owner.pets))
    else:
        st.info("You don't have any pets yet. Add one above!")

    st.divider()


def render_task_section(owner: Owner):
    """Renders the task management section."""
    st.subheader("2. Add Care Tasks")

    if not owner.pets:
        st.warning("Please add a pet first before creating tasks.")
        return

    col1, col2 = st.columns(2)
    
    with col1:
        task_title = st.text_input("Task Description (e.g., Vet Appointment)")
        task_time = st.time_input("Time")
        selected_pet = st.selectbox("Assign to Pet", [p.name for p in owner.pets])
        
    with col2:
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
        task_freq = st.selectbox("Frequency", ["Daily", "Weekly", "Once"])
        
        target_day = None
        target_date = None
        
        if task_freq == "Weekly":
            target_day = st.selectbox("Day of the Week", 
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        elif task_freq == "Once":
            target_date = st.date_input("Select Date").strftime("%Y-%m-%d")

    if st.button("Add Task"):
        if not task_title:
            st.error("Please enter a task description.")
        else:
            time_str = task_time.strftime("%H:%M")
            new_task = Task(
                description=task_title,
                time=time_str,
                frequency=task_freq,
                priority=task_priority,
                target_day=target_day,
                target_date=target_date
            )
            
            for pet in owner.pets:
                if pet.name == selected_pet:
                    pet.add_task(new_task)
                    st.success(f"Added '{task_title}' to {pet.name}'s schedule!")
                    break

    st.divider()


def render_schedule_section(owner: Owner):
    """Renders the schedule viewer section."""
    st.subheader("3. Schedule Viewer")

    view_mode = st.radio("Select View Mode:", 
                         ["Single Day", "All Available Tasks (Master List)"], 
                         horizontal=True)

    if view_mode == "Single Day":
        view_date = st.date_input("Select a day to view", value=datetime.today())
        sort_method = st.radio("Sorting Method:", 
                               ["Chronological (By Time)", "Smart (Priority, then Time)"], 
                               horizontal=True)
    else:
        sort_method = st.radio("Sorting Method:", 
                               ["By Date & Frequency", "By Priority"], 
                               horizontal=True)

    if not st.button("Generate Schedule", type="primary"):
        return
        
    brain = Scheduler(owner)
    
    if view_mode == "Single Day":
        target_datetime = datetime.combine(view_date, datetime.min.time())
        tasks_to_display = brain.get_schedule_for_date(target_datetime)
        
        if not tasks_to_display:
            st.info("No tasks scheduled for this day!")
            return
            
        scheduled_tasks = (brain.sort_by_priority_then_time(tasks_to_display) 
                           if "Smart" in sort_method 
                           else brain.sort_by_time(tasks_to_display))
        
        st.markdown(f"### 📋 Itinerary for {view_date.strftime('%A, %b %d, %Y')}")
    else:
        tasks_to_display = brain.get_all_tasks()
        
        if not tasks_to_display:
            st.info("No tasks have been created yet!")
            return
            
        scheduled_tasks = (brain.sort_master_list_by_priority(tasks_to_display) 
                           if "Priority" in sort_method 
                           else brain.sort_master_list_by_date(tasks_to_display))
        
        st.markdown("### 📚 Master List of All Tasks")

    # Display tasks
    for task in scheduled_tasks:
        pet_name = get_pet_for_task(owner, task)
        status = "✅" if task.completed else "⏳"
        priority_icon = PRIORITY_ICONS.get(task.priority, DEFAULT_PRIORITY_ICON)
        freq_tag = format_freq_tag(task)
        
        st.markdown(f"**{task.time}** {freq_tag} | {status} | {priority_icon} "
                    f"**{task.priority}** | {task.description} *(for {pet_name})*")


def main():
    """Main entry point for the Streamlit app."""
    st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

    if "owner" not in st.session_state:
        st.session_state.owner = None

    if st.session_state.owner is None:
        render_login_page()

    owner = st.session_state.owner

    render_sidebar(owner)
    st.title("🐾 PawPal+ Dashboard")
    st.markdown(f"**Welcome back, {owner.name}!** Let's organize your pet care today.")

    render_pet_section(owner)
    render_task_section(owner)
    render_schedule_section(owner)

    st.divider()
    filename = f"{owner.name}_pawpal_data.json"
    if st.button(f"Save Data to {filename}"):
        owner.save_to_json(filename)
        st.success(f"Data saved successfully to {filename}!")


if __name__ == "__main__":
    main()
