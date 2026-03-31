"""
main.py

Command Line Interface (CLI) entry point for the PawPal+ system.
Demonstrates programmatic instantiation of the Owner/Pet/Task hierarchy 
and executes the Scheduler's conflict detection algorithms.
"""
from datetime import datetime
from core import Owner, Pet, Task, Scheduler


def main():
    # 1. Setup Data
    me = Owner(name="Alex")
    dog = Pet(name="Buddy", species="Dog")
    cat = Pet(name="Luna", species="Cat")

    me.add_pet(dog)
    me.add_pet(cat)

    # 2. Add Tasks (Testing frequency options & Conflicts)
    dog.add_task(Task("Morning Walk", "08:00", "Daily", "High"))
    dog.add_task(Task("Morning Meds", "08:00", "Once", "High", target_date="2026-03-31"))  # Conflict!
    dog.add_task(Task("Flea Medicine", "10:00", "Once", "High", target_date="2026-03-31"))
    cat.add_task(Task("Litter Box Clean", "09:00", "Daily", "Low"))

    # 3. Use the Scheduler
    brain = Scheduler(me)
    today = datetime.now()
    daily_tasks = brain.get_schedule_for_date(today)
    schedule = brain.sort_by_time(daily_tasks)
    
    # Detect and report conflicts
    conflicts = brain.detect_conflicts(daily_tasks)
    if conflicts:
        print("\n[!] WARNING: Scheduling conflicts detected!")
        for t1, t2 in conflicts:
            print(f"  -> '{t1.description}' and '{t2.description}' at {t1.time}")

    # 4. Print formatted output
    print(f"\n--- {me.name}'s Schedule for {today.strftime('%Y-%m-%d')} ---")
    print("-" * 50)
    print(f"{'Time':<7} | {'Status':<6} | {'Priority':<8} | {'Task'}")
    print("-" * 50)
    
    for task in schedule:
        status = "[x]" if task.completed else "[ ]"
        print(f"{task.time:<7} | {status:<6} | {task.priority:<8} | {task.description}")
    print("-" * 50)


if __name__ == "__main__":
    main()
