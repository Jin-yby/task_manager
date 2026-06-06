# auth.py
"""
用户认证模块
处理用户登录、注册、会话管理
"""
import hashlib
import json
import os
from typing import Optional, Tuple


class AuthManager:
    """认证管理器"""

    def __init__(self, data_dir: str = "data"):
        """
        初始化认证管理器

        Args:
            data_dir: 数据目录路径
        """
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self.current_user: Optional[str] = None

        # 确保目录存在
        os.makedirs(data_dir, exist_ok=True)

        # 初始化用户文件
        if not os.path.exists(self.users_file):
            self._save_users({})

    def _hash_password(self, password: str) -> str:
        """
        哈希密码

        Args:
            password: 原始密码

        Returns:
            哈希后的密码
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def _load_users(self) -> dict:
        """
        加载用户数据

        Returns:
            用户数据字典
        """
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_users(self, users: dict) -> None:
        """
        保存用户数据

        Args:
            users: 用户数据字典
        """
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    def register(self, username: str, password: str) -> Tuple[bool, str]:
        """
        注册新用户

        Args:
            username: 用户名
            password: 密码

        Returns:
            (是否成功, 消息)
        """
        # 验证输入
        username = username.strip()
        password = password.strip()

        if not username or not password:
            return False, "用户名和密码不能为空"

        if len(username) < 3:
            return False, "用户名至少需要3个字符"

        if len(password) < 6:
            return False, "密码至少需要6个字符"

        # 检查特殊字符
        if not username.isalnum():
            return False, "用户名只能包含字母和数字"

        users = self._load_users()

        if username in users:
            return False, "用户名已存在"

        # 注册用户
        users[username] = {
            "password_hash": self._hash_password(password),
            "created_at": self._get_current_time(),
            "last_login": None
        }

        self._save_users(users)

        # 创建用户数据目录
        user_data_dir = os.path.join(self.data_dir, "users", username)
        os.makedirs(user_data_dir, exist_ok=True)

        return True, "注册成功"

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        用户登录

        Args:
            username: 用户名
            password: 密码

        Returns:
            (是否成功, 消息)
        """
        # 验证输入
        username = username.strip()
        password = password.strip()

        if not username or not password:
            return False, "用户名和密码不能为空"

        users = self._load_users()

        if username not in users:
            return False, "用户名或密码错误"

        # 验证密码
        stored_hash = users[username].get("password_hash")
        input_hash = self._hash_password(password)

        if stored_hash != input_hash:
            return False, "用户名或密码错误"

        # 更新登录时间
        users[username]["last_login"] = self._get_current_time()
        self._save_users(users)

        # 设置当前用户
        self.current_user = username

        return True, f"欢迎回来，{username}！"

    def logout(self) -> None:
        """用户登出"""
        self.current_user = None

    def is_authenticated(self) -> bool:
        """
        检查是否已认证

        Returns:
            是否已登录
        """
        return self.current_user is not None

    def get_current_user(self) -> Optional[str]:
        """
        获取当前用户

        Returns:
            当前用户名，如果未登录则返回None
        """
        return self.current_user

    def change_password(self, username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        修改密码

        Args:
            username: 用户名
            old_password: 旧密码
            new_password: 新密码

        Returns:
            (是否成功, 消息)
        """
        # 验证当前用户
        if self.current_user != username:
            return False, "无权修改其他用户的密码"

        # 验证旧密码
        success, message = self.login(username, old_password)
        if not success:
            return False, "原密码错误"

        # 验证新密码
        new_password = new_password.strip()
        if len(new_password) < 6:
            return False, "新密码至少需要6个字符"

        # 更新密码
        users = self._load_users()
        users[username]["password_hash"] = self._hash_password(new_password)
        self._save_users(users)

        return True, "密码修改成功"

    def delete_account(self, username: str, password: str) -> Tuple[bool, str]:
        """
        删除账户

        Args:
            username: 用户名
            password: 密码

        Returns:
            (是否成功, 消息)
        """
        # 验证当前用户
        if self.current_user != username:
            return False, "无权删除其他用户的账户"

        # 验证密码
        success, message = self.login(username, password)
        if not success:
            return False, "密码错误"

        # 删除用户
        users = self._load_users()

        if username in users:
            del users[username]
            self._save_users(users)

            # 删除用户数据目录
            user_data_dir = os.path.join(self.data_dir, "users", username)
            if os.path.exists(user_data_dir):
                import shutil
                shutil.rmtree(user_data_dir)

            # 登出
            self.logout()

            return True, "账户删除成功"

        return False, "用户不存在"

    def _get_current_time(self) -> str:
        """
        获取当前时间字符串

        Returns:
            时间字符串
        """
        from datetime import datetime
        return datetime.now().isoformat()

    def get_all_users(self) -> list:
        """
        获取所有用户（仅管理员可用）

        Returns:
            用户列表
        """
        users = self._load_users()
        return list(users.keys())

    def get_user_info(self, username: str) -> Optional[dict]:
        """
        获取用户信息

        Args:
            username: 用户名

        Returns:
            用户信息字典，如果用户不存在则返回None
        """
        users = self._load_users()
        if username in users:
            info = users[username].copy()
            info.pop("password_hash", None)  # 移除密码哈希
            return info
        return None

    def validate_session(self) -> bool:
        """
        验证会话有效性

        Returns:
            会话是否有效
        """
        if not self.current_user:
            return False

        users = self._load_users()
        return self.current_user in users


class SessionManager:
    """会话管理器"""

    def __init__(self, auth_manager: AuthManager):
        """
        初始化会话管理器

        Args:
            auth_manager: 认证管理器实例
        """
        self.auth_manager = auth_manager
        self.login_time = None
        self.session_timeout = 3600  # 1小时超时

    def start_session(self, username: str) -> None:
        """
        开始新会话

        Args:
            username: 用户名
        """
        from datetime import datetime
        self.auth_manager.current_user = username
        self.login_time = datetime.now()

    def end_session(self) -> None:
        """结束当前会话"""
        self.auth_manager.logout()
        self.login_time = None

    def is_session_valid(self) -> bool:
        """
        检查会话是否有效

        Returns:
            会话是否有效
        """
        if not self.auth_manager.is_authenticated() or not self.login_time:
            return False

        from datetime import datetime
        current_time = datetime.now()
        elapsed = (current_time - self.login_time).total_seconds()

        return elapsed < self.session_timeout

    def get_remaining_time(self) -> int:
        """
        获取剩余会话时间（秒）

        Returns:
            剩余时间，如果会话无效则返回-1
        """
        if not self.is_session_valid():
            return -1

        from datetime import datetime
        current_time = datetime.now()
        elapsed = (current_time - self.login_time).total_seconds()

        return int(self.session_timeout - elapsed)