# main.py
import tkinter as tk
from tkinter import messagebox
from data_handler import DataHandler
from task_manager import TaskManager
from gui import LoginWindow, MainWindow
import styles


class TaskManagementApp:
    """任务管理应用主类"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("个人任务与日程管理系统")

        # 设置样式
        styles.configure_styles()

        # 初始化数据处理器和任务管理器
        self.data_handler = DataHandler()
        self.task_manager = TaskManager(self.data_handler)

        # 设置窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 显示登录窗口
        self.show_login()

    def show_login(self):
        """显示登录窗口"""
        # 清除主窗口中的所有内容
        for widget in self.root.winfo_children():
            widget.destroy()

        # 创建登录窗口
        LoginWindow(self.root, self.task_manager, self.on_login_success)

    def on_login_success(self):
        """登录成功回调"""
        # 清除主窗口中的所有内容
        for widget in self.root.winfo_children():
            widget.destroy()

        # 创建主窗口
        self.main_window = MainWindow(self.root, self.task_manager)

        # 更新窗口标题
        self.root.title(f"个人任务与日程管理系统 - {self.task_manager.current_user}")

    def on_closing(self):
        """窗口关闭事件"""
        if messagebox.askokcancel("退出", "确定要退出程序吗？"):
            if hasattr(self, 'task_manager') and self.task_manager.current_user:
                self.task_manager.logout()
            self.root.destroy()

    def run(self):
        """运行应用"""
        # 居中显示窗口
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # 运行主循环
        self.root.mainloop()


if __name__ == "__main__":
    app = TaskManagementApp()
    app.run()