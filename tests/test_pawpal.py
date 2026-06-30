"""Tests for PawPal+ core behaviors."""

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    """Task Completion: mark_complete() should change the task's status."""
    task = Task("Morning walk", duration_minutes=30, priority="high")

    # A new task starts out pending, then becomes complete once marked.
    assert task.status == "pending"
    task.mark_complete()
    assert task.status == "complete"


def test_add_task_increases_pet_task_count():
    """Task Addition: adding a task to a Pet should increase its task count."""
    pet = Pet(name="Biscuit", species="dog")

    assert len(pet.tasks) == 0
    pet.add_task(Task("Feeding", duration_minutes=10, priority="high"))
    assert len(pet.tasks) == 1
