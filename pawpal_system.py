"""PawPal+ core skeleton.

Class names, attributes, and method stubs generated from diagrams/uml.mmd.
Data-holding objects (Owner, Pet, Task, ScheduledTask, DailyPlan) use
@dataclass. Scheduler is a plain service class (no data, just behavior).
No logic yet — fill in each method body.
"""

from __future__ import annotations

from dataclasses import dataclass, field


def _to_minutes(clock: str) -> int:
    """Convert a 'HH:MM' clock string to minutes since midnight."""
    hours, minutes = clock.split(":")
    return int(hours) * 60 + int(minutes)


def _to_clock(total_minutes: int) -> str:
    """Convert minutes since midnight back to a 'HH:MM' clock string."""
    return f"{total_minutes // 60:02d}:{total_minutes % 60:02d}"


@dataclass
class Owner:
    """The person the plan is built for; carries the day's time budget."""

    name: str
    available_minutes: int = 240
    day_start: str = "08:00"
    preferred_order: list[str] = field(default_factory=list)


@dataclass
class Pet:
    """Pet identity plus the care tasks that belong to this pet.

    Design note: per-pet care needs (e.g. meds, grooming) live here as ``tasks``,
    because what a pet needs varies per pet. Per-activity attributes (duration,
    priority, status) belong on Task. Scheduler.build_plan still takes a tasks
    list as an argument, so a caller may pass ``pet.tasks`` or any other list.
    """

    name: str
    species: str = "dog"
    age_years: int | None = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        self.tasks.append(task)


@dataclass
class Task:
    """One care activity to be scheduled."""

    title: str
    duration_minutes: int
    priority: str = "medium"
    status: str = "pending"

    def priority_rank(self) -> int:
        """Return a numeric rank for this task's priority (higher = more urgent)."""
        ranks = {"high": 3, "medium": 2, "low": 1}
        return ranks.get(self.priority.lower(), 0)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.status = "complete"


@dataclass
class ScheduledTask:
    """A Task placed on the timeline, with timing and a reason."""

    task: Task
    start_time: str
    end_time: str
    reason: str


@dataclass
class DailyPlan:
    """The result of scheduling: what was placed, what was skipped, and why."""

    owner: Owner
    pet: Pet
    scheduled: list[ScheduledTask] = field(default_factory=list)
    skipped: list[tuple[Task, str]] = field(default_factory=list)
    total_minutes_used: int = 0

    def summary(self) -> str:
        """Return a human-readable plan plus reasoning."""
        lines = [
            f"Daily plan for {self.pet.name} ({self.pet.species}) "
            f"— owner {self.owner.name}:"
        ]

        if self.scheduled:
            for item in self.scheduled:
                task = item.task
                lines.append(
                    f"  {item.start_time}–{item.end_time}  {task.title} "
                    f"({task.duration_minutes} min) [priority: {task.priority}] "
                    f"— {item.reason}"
                )
        else:
            lines.append("  (nothing scheduled)")

        if self.skipped:
            lines.append("Skipped:")
            for task, reason in self.skipped:
                lines.append(
                    f"  {task.title} ({task.duration_minutes} min) — {reason}"
                )

        lines.append(
            f"Total: {self.total_minutes_used} of "
            f"{self.owner.available_minutes} min used."
        )
        return "\n".join(lines)


class Scheduler:
    """Builds a DailyPlan from an owner, a pet, and a list of tasks."""

    def build_plan(self, owner: Owner, pet: Pet, tasks: list[Task]) -> DailyPlan:
        """Order and pack tasks into the owner's time budget; return a DailyPlan.

        Tasks are ordered by priority (highest first), with the owner's
        ``preferred_order`` breaking ties. Tasks are then packed in order onto
        the timeline starting at ``owner.day_start``; a task that would exceed
        the remaining time budget is skipped with a reason.
        """

        def sort_key(task: Task) -> tuple[int, int]:
            """Sort by priority (highest first), then owner's preferred order."""
            if task.title in owner.preferred_order:
                preference = owner.preferred_order.index(task.title)
            else:
                preference = len(owner.preferred_order)
            return (-task.priority_rank(), preference)

        ordered = sorted(tasks, key=sort_key)

        plan = DailyPlan(owner=owner, pet=pet)
        clock = _to_minutes(owner.day_start)
        used = 0

        for task in ordered:
            remaining = owner.available_minutes - used
            if task.duration_minutes <= remaining:
                start = _to_clock(clock)
                clock += task.duration_minutes
                end = _to_clock(clock)
                plan.scheduled.append(
                    ScheduledTask(
                        task=task,
                        start_time=start,
                        end_time=end,
                        reason=(
                            f"priority {task.priority}; fit within "
                            f"remaining {remaining} min"
                        ),
                    )
                )
                used += task.duration_minutes
            else:
                plan.skipped.append(
                    (
                        task,
                        f"needs {task.duration_minutes} min but only "
                        f"{remaining} min left",
                    )
                )

        plan.total_minutes_used = used
        return plan
