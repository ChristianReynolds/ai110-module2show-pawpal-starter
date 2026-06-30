"""PawPal+ core skeleton.

Class names, attributes, and method stubs generated from diagrams/uml.mmd.
Data-holding objects (Owner, Pet, Task, ScheduledTask, DailyPlan) use
@dataclass. Scheduler is a plain service class (no data, just behavior).
No logic yet — fill in each method body.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Owner:
    """The person the plan is built for; carries the day's time budget."""

    name: str
    available_minutes: int = 240
    day_start: str = "08:00"
    preferred_order: list[str] = field(default_factory=list)


@dataclass
class Pet:
    """Basic pet identity used for display."""

    name: str
    species: str = "dog"
    age_years: int | None = None


@dataclass
class Task:
    """One care activity to be scheduled."""

    title: str
    duration_minutes: int
    priority: str = "medium"

    def priority_rank(self) -> int:
        """Return a numeric rank for this task's priority (higher = more urgent)."""
        # TODO: map priority label -> int
        ...


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
        # TODO: build a readable summary of scheduled + skipped tasks
        ...


class Scheduler:
    """Builds a DailyPlan from an owner, a pet, and a list of tasks."""

    def build_plan(self, owner: Owner, pet: Pet, tasks: list[Task]) -> DailyPlan:
        """Order and pack tasks into the owner's time budget; return a DailyPlan."""
        # TODO: sort by priority, pack within available_minutes, assign times
        ...
