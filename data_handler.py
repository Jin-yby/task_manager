import json
import os
from datetime import datetime, date
from typing import Dict, List, Any, Optional


class DataHandler:
    """数据处理类，负责所有数据的读写操作"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self.tasks_dir = os.path.join(data_dir, "tasks")

        # 确保目录存在
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(self.tasks_dir, exist_ok=True)

        # 初始化用户文件
        if not os.path.exists(self.users_file):
            self._save_users({})

    def _save_users(self, users_data: Dict) -> None:
        """保存用户数据"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)

    def _load_users(self) -> Dict:
        """加载用户数据"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _get_user_tasks_file(self, username: str) -> str:
        """获取用户任务文件路径"""
        return os.path.join(self.tasks_dir, f"{username}_tasks.json")

    def user_exists(self, username: str) -> bool:
        """检查用户是否存在"""
        users = self._load_users()
        return username in users

    def validate_user(self, username: str, password: str) -> bool:
        """验证用户登录"""
        users = self._load_users()
        if username in users:
            return users[username]["password"] == password
        return False

    def register_user(self, username: str, password: str) -> bool:
        """注册新用户"""
        users = self._load_users()

        if username in users:
            return False  # 用户已存在

        users[username] = {
            "password": password,
            "created_at": datetime.now().isoformat()
        }

        self._save_users(users)

        # 创建用户任务文件
        self.save_user_tasks(username, [])
        return True

    def save_user_tasks(self, username: str, tasks: List[Dict]) -> None:
        """保存用户任务"""
        tasks_file = self._get_user_tasks_file(username)

        # 转换日期对象为字符串
        serializable_tasks = []
        for task in tasks:
            task_copy = task.copy()
            if isinstance(task_copy.get('due_date'), date):
                task_copy['due_date'] = task_copy['due_date'].isoformat()
            if isinstance(task_copy.get('created_at'), datetime):
                task_copy['created_at'] = task_copy['created_at'].isoformat()
            if isinstance(task_copy.get('completed_at'), datetime):
                task_copy['completed_at'] = task_copy['completed_at'].isoformat()
            serializable_tasks.append(task_copy)

        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_tasks, f, ensure_ascii=False, indent=2)

    def load_user_tasks(self, username: str) -> List[Dict]:
        """加载用户任务"""
        tasks_file = self._get_user_tasks_file(username)

        try:
            with open(tasks_file, 'r', encoding='utf-8') as f:
                tasks = json.load(f)

            # 转换字符串为日期对象
            for task in tasks:
                if task.get('due_date'):
                    task['due_date'] = date.fromisoformat(task['due_date'])
                if task.get('created_at'):
                    task['created_at'] = datetime.fromisoformat(task['created_at'])
                if task.get('completed_at'):
                    task['completed_at'] = datetime.fromisoformat(task['completed_at'])

            return tasks
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_all_users(self) -> List[str]:
        """获取所有用户"""
        users = self._load_users()
        return list(users.keys())