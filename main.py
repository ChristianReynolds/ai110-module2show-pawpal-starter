"""Demo script for PawPal+.

Builds one owner with two pets, gives each pet a few care tasks, and prints
"Today's Schedule" for each pet to the terminal.

Run with:  python3 main.py
"""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    # One owner who has 90 minutes to spend on pet care today.
    owner = Owner(
        name="Sam",
        available_minutes=90,
        day_start="08:00",
        preferred_order=["Morning walk", "Feeding"],
    )

    # Two pets.
    biscuit = Pet(name="Biscuit", species="Golden Retriever", age_years=3)
    mochi = Pet(name="Mochi", species="cat", age_years=5)

    # Tasks for each pet, with different durations and priorities.
    biscuit_tasks = [
        Task("Morning walk", duration_minutes=30, priority="high"),
        Task("Feeding", duration_minutes=10, priority="high"),
        Task("Enrichment", duration_minutes=20, priority="medium"),
        Task("Nail trim", duration_minutes=15, priority="low"),
    ]
    mochi_tasks = [
        Task("Feeding", duration_minutes=10, priority="high"),
        Task("Give meds", duration_minutes=5, priority="high"),
        Task("Brush coat", duration_minutes=15, priority="medium"),
    ]

    scheduler = Scheduler()

    print("=" * 48)
    print("Today's Schedule")
    print("=" * 48)

    for pet, tasks in [(biscuit, biscuit_tasks), (mochi, mochi_tasks)]:
        plan = scheduler.build_plan(owner, pet, tasks)
        print()
        print(plan.summary())


if __name__ == "__main__":
    main()
