"""
Plan Tracker for tracking plan execution history and statistics.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from .task_planner import Plan, Task, TaskStatus, TaskComplexity
import json
from pathlib import Path


class PlanTracker:
    """Tracks plan execution history and provides statistics."""

    def __init__(self, storage_path: str = "./data/plans"):
        """
        Initialize the plan tracker.

        Args:
            storage_path: Path to store plan history
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.current_plans: Dict[str, Plan] = {}

    def save_plan(self, plan: Plan) -> str:
        """
        Save a plan to storage.

        Args:
            plan: The plan to save

        Returns:
            The file path where the plan was saved
        """
        self.current_plans[plan.id] = plan

        file_path = self.storage_path / f"{plan.id}.json"
        with open(file_path, 'w') as f:
            json.dump(plan.to_dict(), f, indent=2)

        return str(file_path)

    def load_plan(self, plan_id: str) -> Optional[Plan]:
        """
        Load a plan from storage.

        Args:
            plan_id: The ID of the plan to load

        Returns:
            The loaded Plan object or None if not found
        """
        # Check cache first
        if plan_id in self.current_plans:
            return self.current_plans[plan_id]

        # Load from file
        file_path = self.storage_path / f"{plan_id}.json"
        if not file_path.exists():
            return None

        with open(file_path, 'r') as f:
            data = json.load(f)

        plan = self._dict_to_plan(data)
        self.current_plans[plan_id] = plan

        return plan

    def _dict_to_plan(self, data: Dict[str, Any]) -> Plan:
        """
        Convert a dictionary to a Plan object.

        Args:
            data: Dictionary representation of a plan

        Returns:
            Plan object
        """
        from datetime import datetime

        tasks = []
        for task_data in data.get("tasks", []):
            task = Task(
                id=task_data["id"],
                description=task_data["description"],
                status=TaskStatus(task_data["status"]),
                complexity=TaskComplexity(task_data["complexity"]),
                dependencies=task_data["dependencies"],
                estimated_time=task_data.get("estimated_time"),
                agent_type=task_data.get("agent_type"),
                result=task_data.get("result"),
                error=task_data.get("error"),
                created_at=datetime.fromisoformat(task_data["created_at"]),
                started_at=datetime.fromisoformat(task_data["started_at"]) if task_data.get("started_at") else None,
                completed_at=datetime.fromisoformat(task_data["completed_at"]) if task_data.get("completed_at") else None,
            )
            tasks.append(task)

        plan = Plan(
            id=data["id"],
            goal=data["goal"],
            tasks=tasks,
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            status=TaskStatus(data["status"]),
        )

        return plan

    def list_plans(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        List all saved plans.

        Args:
            limit: Maximum number of plans to return

        Returns:
            List of plan summaries
        """
        plans = []
        for file_path in self.storage_path.glob("*.json"):
            if len(plans) >= limit:
                break

            with open(file_path, 'r') as f:
                data = json.load(f)

            plans.append({
                "id": data["id"],
                "goal": data["goal"],
                "status": data["status"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
                "task_count": len(data["tasks"]),
            })

        # Sort by creation date, newest first
        plans.sort(key=lambda x: x["created_at"], reverse=True)

        return plans

    def get_plan_statistics(self, plan_id: str) -> Dict[str, Any]:
        """
        Get statistics for a specific plan.

        Args:
            plan_id: The ID of the plan

        Returns:
            Dictionary with plan statistics
        """
        plan = self.load_plan(plan_id)
        if not plan:
            return {}

        total_tasks = len(plan.tasks)
        completed_tasks = sum(1 for t in plan.tasks if t.status == TaskStatus.COMPLETED)
        failed_tasks = sum(1 for t in plan.tasks if t.status == TaskStatus.FAILED)
        pending_tasks = sum(1 for t in plan.tasks if t.status == TaskStatus.PENDING)
        in_progress_tasks = sum(1 for t in plan.tasks if t.status == TaskStatus.IN_PROGRESS)

        # Calculate completion percentage
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Calculate total time
        total_time = 0
        for task in plan.tasks:
            if task.started_at and task.completed_at:
                duration = (task.completed_at - task.started_at).total_seconds() / 60  # in minutes
                total_time += duration

        # Calculate complexity distribution
        complexity_dist = {}
        for task in plan.tasks:
            comp = task.complexity.value
            complexity_dist[comp] = complexity_dist.get(comp, 0) + 1

        return {
            "plan_id": plan.id,
            "goal": plan.goal,
            "status": plan.status.value,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completion_percentage": round(completion_percentage, 2),
            "total_time_minutes": round(total_time, 2),
            "complexity_distribution": complexity_dist,
            "created_at": plan.created_at.isoformat(),
            "updated_at": plan.updated_at.isoformat(),
        }

    def get_overall_statistics(self) -> Dict[str, Any]:
        """
        Get overall statistics across all plans.

        Returns:
            Dictionary with overall statistics
        """
        plans = self.list_plans()

        total_plans = len(plans)
        completed_plans = sum(1 for p in plans if p["status"] == TaskStatus.COMPLETED.value)
        failed_plans = sum(1 for p in plans if p["status"] == TaskStatus.FAILED.value)
        in_progress_plans = sum(1 for p in plans if p["status"] == TaskStatus.IN_PROGRESS.value)

        return {
            "total_plans": total_plans,
            "completed_plans": completed_plans,
            "failed_plans": failed_plans,
            "in_progress_plans": in_progress_plans,
            "success_rate": round(completed_plans / total_plans * 100, 2) if total_plans > 0 else 0,
        }

    def delete_plan(self, plan_id: str) -> bool:
        """
        Delete a plan from storage.

        Args:
            plan_id: The ID of the plan to delete

        Returns:
            True if deleted, False if not found
        """
        if plan_id in self.current_plans:
            del self.current_plans[plan_id]

        file_path = self.storage_path / f"{plan_id}.json"
        if file_path.exists():
            file_path.unlink()
            return True

        return False

    def clear_old_plans(self, days: int = 30):
        """
        Clear plans older than specified days.

        Args:
            days: Number of days to keep plans
        """
        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=days)

        for file_path in self.storage_path.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                created_at = datetime.fromisoformat(data["created_at"])
                if created_at < cutoff_date:
                    file_path.unlink()
                    plan_id = data["id"]
                    if plan_id in self.current_plans:
                        del self.current_plans[plan_id]
            except (json.JSONDecodeError, KeyError, ValueError):
                # Skip corrupted files
                continue
