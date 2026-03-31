# main.py
from core import Owner, Pet, Task, Scheduler

def main():
    # 1. Setup Data
    me = Owner(name="Alex")
    dog = Pet(name="Buddy", species="Dog")
    cat = Pet(name="Luna", species="Cat")

    me.add_pet(dog)
    me.add_pet(cat)

    # 2. Add Tasks
    dog.add_task(Task("Morning Walk", "08:00", "Daily", "High"))
    dog.add_task(Task("Evening Feed", "18:00", "Daily", "Medium"))
    cat.add_task(Task("Litter Box Clean", "09:00", "Daily", "Low"))

    # 3. Use the Scheduler
    brain = Scheduler(me)
    all_tasks = brain.get_all_tasks()
    schedule = brain.sort_by_time(all_tasks)

    # 4. Print formatted output
    print(f"\n--- {me.name}'s PawPal+ Schedule ---")
    print("-" * 45)
    print(f"{'Time':<7} | {'Status':<6} | {'Priority':<8} | {'Task'}")
    print("-" * 45)
    
    for task in schedule:
        status = "[x]" if task.completed else "[ ]"
        print(f"{task.time:<7} | {status:<6} | {task.priority:<8} | {task.description}")
    print("-" * 45)

if __name__ == "__main__":
    main()