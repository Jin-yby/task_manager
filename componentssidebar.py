# components/sidebar.py
import tkinter as tk
from tkinter import ttk
from typing import Dict, Callable


class Sidebar:
    """侧边导航栏"""

    def __init__(self, parent, callbacks: Dict[str, Callable]):
        self.parent = parent
        self.callbacks = callbacks
        self.active_button = None
        self.setup_ui()

    def setup_ui(self):
        """设置侧边栏UI"""
        self.sidebar_frame = ttk.Frame(self.parent, width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        self.sidebar_frame.pack_propagate(False)

        # 标题区域
        title_frame = ttk.Frame(self.sidebar_frame)
        title_frame.pack(fill=tk.X, padx=10, pady=20)

        ttk.Label(title_frame, text="Smart Student\nTask Manager",
                  font=("Microsoft YaHei", 12, "bold")).pack(anchor=tk.W)

        # 导航按钮
        self.buttons = {}
        nav_items = [
            ("Dashboard", "📊", "dashboard"),
            ("My Tasks", "📝", "tasks"),
            ("Add Task", "➕", "add_task"),
            ("Smart Schedule", "🧠", "schedule"),
            ("Analytics", "📈", "analytics"),
        ]

        for text, icon, callback_key in nav_items:
            self.add_nav_button(text, icon, callback_key)

    def add_nav_button(self, text: str, icon: str, callback_key: str):
        """添加导航按钮"""
        btn_frame = ttk.Frame(self.sidebar_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        # 图标和文本
        icon_label = ttk.Label(btn_frame, text=icon, font=("Segoe UI Emoji", 14))
        icon_label.pack(side=tk.LEFT, padx=(0, 5))

        btn_text = ttk.Label(btn_frame, text=text,
                             font=("Microsoft YaHei", 10))
        btn_text.pack(side=tk.LEFT)

        # 绑定点击事件
        def on_click():
            self.set_active_button(btn_frame)
            self.callbacks.get(callback_key, lambda: None)()

        btn_frame.bind("<Button-1>", lambda e: on_click())
        icon_label.bind("<Button-1>", lambda e: on_click())
        btn_text.bind("<Button-1>", lambda e: on_click())

        # 保存按钮引用
        self.buttons[callback_key] = {
            "frame": btn_frame,
            "icon": icon_label,
            "text": btn_text
        }

    def set_active_button(self, button_frame):
        """设置激活按钮"""
        if self.active_button:
            self.active_button.configure(style="TFrame")

        self.active_button = button_frame
        self.active_button.configure(style="Active.TFrame")

        # 高亮样式
        self.active_button.configure(style="Active.TFrame")