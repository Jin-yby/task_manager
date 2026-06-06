from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
from enum import Enum
import heapq


class Priority(Enum):
    """任务优先级枚举"""
    HIGH = 3
    MEDIUM = 2
    LOW = 1

    @staticmethod
    def from_string(priority_str: str) -> 'Priority':
        """从字符串转换为枚举"""
        priority_map = {
            "高": Priority.HIGH,
            "中": Priority.MEDIUM,
            "低": Priority.LOW,
            "high": Priority.HIGH,
            "medium": Priority.MEDIUM,
            "low": Priority.LOW
        }
        return priority_map.get(priority_str.lower(), Priority.MEDIUM)

    def to_string(self, lang: str = "zh") -> str:
        """枚举转换为字符串"""
        if lang == "zh":
            return {Priority.HIGH: "高", Priority.MEDIUM: "中", Priority.LOW: "低"}[self]
        else:
            return self.name.lower().capitalize()


class Task:
    """任务类"""

    def __init__(self,
                 title: str,
                 due_date: date,
                 priority: Priority = Priority.MEDIUM,
                 description: str = "",
                 category: str = "",
                 task_id: Optional[str] = None):
        self.id = task_id or f"task_{datetime.now().timestamp()}_{hash(title)}"
        self.title = title
        self.due_date = due_date
        self.priority = priority
        self.description = description
        self.category = category
        self.completed = False
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "priority": self.priority.value,
            "description": self.description,
            "category": self.category,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """从字典创建任务"""
        task = cls(
            title=data["title"],
            due_date=data["due_date"],
            priority=Priority(data["priority"]),
            description=data.get("description", ""),
            category=data.get("category", ""),
            task_id=data.get("id")
        )
        task.completed = data.get("completed", False)
        task.created_at = data.get("created_at", datetime.now())
        task.completed_at = data.get("completed_at")
        return task

    def get_status(self) -> str:
        """获取任务状态"""
        today = date.today()
        if self.completed:
            return "已完成"
        elif self.due_date < today:
            return "已过期"
        elif self.due_date == today:
            return "今天到期"
        elif (self.due_date - today).days <= 3:
            return "即将到期"
        else:
            return "进行中"

    def get_priority_color(self) -> str:
        """获取优先级颜色"""
        return {
            Priority.HIGH: "#FF6B6B",  # 红色
            Priority.MEDIUM: "#FFD93D",  # 黄色
            Priority.LOW: "#6BCF7F"  # 绿色
        }[self.priority]

    def mark_complete(self) -> None:
        """标记为完成"""
        self.completed = True
        self.completed_at = datetime.now()

    def mark_incomplete(self) -> None:
        """标记为未完成"""
        self.completed = False
        self.completed_at = None


class TaskManager:
    """任务管理器"""

    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.current_user: Optional[str] = None
        self.tasks: List[Task] = []

    def login(self, username: str, password: str) -> bool:
        """用户登录"""
        if self.data_handler.validate_user(username, password):
            self.current_user = username
            self.load_tasks()
            return True
        return False

    def register(self, username: str, password: str) -> bool:
        """用户注册"""
        if self.data_handler.register_user(username, password):
            self.current_user = username
            self.tasks = []
            self.save_tasks()
            return True
        return False

    def logout(self) -> None:
        """用户登出"""
        if self.current_user:
            self.save_tasks()
        self.current_user = None
        self.tasks = []

    def load_tasks(self) -> None:
        """加载任务"""
        if not self.current_user:
            return

        tasks_data = self.data_handler.load_user_tasks(self.current_user)
        self.tasks = [Task.from_dict(task_data) for task_data in tasks_data]

    def save_tasks(self) -> None:
        """保存任务"""
        if not self.current_user:
            return

        tasks_data = [task.to_dict() for task in self.tasks]
        self.data_handler.save_user_tasks(self.current_user, tasks_data)

    def add_task(self, task: Task) -> None:
        """添加任务"""
        self.tasks.append(task)
        self.save_tasks()

    def update_task(self, task_id: str, **kwargs) -> bool:
        """更新任务"""
        for task in self.tasks:
            if task.id == task_id:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        if key == 'priority' and isinstance(value, str):
                            value = Priority.from_string(value)
                        setattr(task, key, value)
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False

    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self, filter_completed: Optional[bool] = None) -> List[Task]:
        """获取所有任务（可选过滤）"""
        if filter_completed is None:
            return self.tasks.copy()
        return [task for task in self.tasks if task.completed == filter_completed]

    def get_tasks_by_category(self, category: str) -> List[Task]:
        """按分类获取任务"""
        return [task for task in self.tasks if task.category == category]

    def get_overdue_tasks(self) -> List[Task]:
        """获取过期任务"""
        today = date.today()
        return [task for task in self.tasks
                if not task.completed and task.due_date < today]

    def get_upcoming_tasks(self, days: int = 3) -> List[Task]:
        """获取即将到期的任务"""
        today = date.today()
        end_date = today + timedelta(days=days)
        return [task for task in self.tasks
                if not task.completed and today <= task.due_date <= end_date]

    def get_categories(self) -> List[str]:
        """获取所有分类"""
        categories = set(task.category for task in self.tasks if task.category)
        return sorted(list(categories))

    def sort_tasks(self, by: str = "due_date", reverse: bool = False) -> List[Task]:
        """排序任务"""
        if by == "due_date":
            return sorted(self.tasks, key=lambda x: x.due_date, reverse=reverse)
        elif by == "priority":
            return sorted(self.tasks, key=lambda x: x.priority.value, reverse=reverse)
        elif by == "title":
            return sorted(self.tasks, key=lambda x: x.title.lower(), reverse=reverse)
        elif by == "created_at":
            return sorted(self.tasks, key=lambda x: x.created_at, reverse=reverse)
        else:
            return self.tasks.copy()

    def search_tasks(self, keyword: str) -> List[Task]:
        """搜索任务"""
        keyword = keyword.lower()
        return [task for task in self.tasks
                if keyword in task.title.lower() or keyword in task.description.lower()]