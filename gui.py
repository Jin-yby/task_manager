import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, date
from typing import Optional, Callable
import styles


class LoginWindow:
    """登录窗口"""

    def __init__(self, parent, task_manager, on_login_success):
        self.parent = parent
        self.task_manager = task_manager
        self.on_login_success = on_login_success

        self.window = tk.Toplevel(parent)
        self.window.title("任务管理系统 - 登录")
        self.window.geometry("400x300")
        self.window.configure(bg=styles.COLORS["background"])
        self.window.resizable(False, False)

        # 居中显示
        self.window.transient(parent)
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 主框架
        main_frame = tk.Frame(self.window, bg=styles.COLORS["background"], padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = tk.Label(
            main_frame,
            text="任务管理系统",
            font=styles.FONTS["title"],
            bg=styles.COLORS["background"],
            fg=styles.COLORS["primary"]
        )
        title_label.pack(pady=(0, 20))

        # 登录表单框架
        form_frame = tk.Frame(main_frame, bg=styles.COLORS["background"])
        form_frame.pack(fill=tk.BOTH, expand=True)

        # 用户名
        tk.Label(
            form_frame,
            text="用户名:",
            font=styles.FONTS["normal"],
            bg=styles.COLORS["background"],
            fg=styles.COLORS["text"]
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(
            form_frame,
            textvariable=self.username_var,
            font=styles.FONTS["normal"],
            width=20
        )
        self.username_entry.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="ew")
        self.username_entry.focus()

        # 密码
        tk.Label(
            form_frame,
            text="密码:",
            font=styles.FONTS["normal"],
            bg=styles.COLORS["background"],
            fg=styles.COLORS["text"]
        ).grid(row=1, column=0, sticky="w", pady=(0, 20))

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            form_frame,
            textvariable=self.password_var,
            font=styles.FONTS["normal"],
            show="*",
            width=20
        )
        self.password_entry.grid(row=1, column=1, padx=(10, 0), pady=(0, 20), sticky="ew")

        # 按钮框架
        button_frame = tk.Frame(form_frame, bg=styles.COLORS["background"])
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # 登录按钮
        ttk.Button(
            button_frame,
            text="登录",
            command=self.login,
            style="Primary.TButton"
        ).pack(side=tk.LEFT, padx=(0, 10))

        # 注册按钮
        ttk.Button(
            button_frame,
            text="注册",
            command=self.register
        ).pack(side=tk.LEFT)

        # 绑定回车键
        self.window.bind('<Return>', lambda e: self.login())

    def login(self):
        """登录"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return

        try:
            if self.task_manager.login(username, password):
                self.window.destroy()
                self.on_login_success()
            else:
                messagebox.showerror("错误", "用户名或密码错误")
        except Exception as e:
            messagebox.showerror("错误", f"登录失败: {str(e)}")

    def register(self):
        """注册"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return

        if len(username) < 3:
            messagebox.showerror("错误", "用户名至少需要3个字符")
            return

        if len(password) < 6:
            messagebox.showerror("错误", "密码至少需要6个字符")
            return

        try:
            if self.task_manager.register(username, password):
                messagebox.showinfo("成功", "注册成功！请登录")
            else:
                messagebox.showerror("错误", "用户名已存在")
        except Exception as e:
            messagebox.showerror("错误", f"注册失败: {str(e)}")


class TaskDialog:
    """任务对话框（添加/编辑）"""

    def __init__(self, parent, title, task_manager, task_data=None, on_save=None):
        self.parent = parent
        self.task_manager = task_manager
        self.task_data = task_data
        self.on_save = on_save

        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("500x450")
        self.window.configure(bg=styles.COLORS["background"])
        self.window.resizable(False, False)

        # 居中显示
        self.window.transient(parent)
        self.window.grab_set()

        self.setup_ui()
        if task_data:
            self.load_task_data()

    def setup_ui(self):
        """设置UI"""
        # 主框架
        main_frame = tk.Frame(self.window, bg=styles.COLORS["background"], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = tk.Label(
            main_frame,
            text="任务详情",
            font=styles.FONTS["subtitle"],
            bg=styles.COLORS["background"],
            fg=styles.COLORS["primary"]
        )
        title_label.pack(pady=(0, 20))

        # 表单框架
        form_frame = tk.Frame(main_frame, bg=styles.COLORS["background"])
        form_frame.pack(fill=tk.BOTH, expand=True)

        row = 0

        # 任务名称
        tk.Label(
            form_frame,
            text="任务名称*:",
            font=styles.FONTS["normal"],
            bg=styles.COLORS["background"],
            fg=styles.COLORS["text"]
        ).grid(row=row, column=0, sticky="w", pady=(0, 10))

        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(
            form_frame,
            textvariable=self.title_var,
            font=styles.FONTS["normal"],
            width=30
        )
        self.title_entry.grid(row=row, column=1, padx=(10, 0), pady=(0, 10), sticky="ew")
        row += 1

        # 截止日期
        tk.Label(
            form_frame,
            text="截止日期*:",
            font=styles.FONTS["normal"],
            bg=styles.COLORS["background"],
            fg=styles.COLORS["text"]
        ).grid(row=row, column=0, sticky="w", pady=(0, 10))

        date_frame = tk.Frame(form_frame, bg=styles.COLORS["background"])
        date_frame.grid(row=row, column=1, padx=(10, 0), pady=(0, 10), sticky="w")

        self.year_var = tk.StringVar(value=str(date.today().year))
        self.month_var = tk.StringVar(value=str(date.today().month))
        self.day_var = tk.StringVar(value=str(date.today().day))

        ttk.Entry(date_frame, textvariable=self.year_var, width=6).pack(side=tk.LEFT)
        tk.Label(date_frame, text="年", bg=styles.COLORS["background"]).pack(side=tk.LEFT, padx=2)
        ttk.Entry(date_frame, textvariable=self.month_var, width=4).pack(side=tk.LEFT)
        tk.Label(date_frame, text="月", bg=styles.COLORS["background"]).pack(side=tk.LEFT, padx=2)
        ttk.Entry(date_frame, textvariable=self.day_var, width=4).pack(side=tk.LEFT)
        tk.Label(date_frame, text="日", bg=styles.COLORS["background"]).pack(side=tk.LEFT, padx=2)
        row += 1

        # 优先级
        tk.Label(
            form_frame,
            text="优先级:",
            font=styles.FONTS["normal"],
            bg=styles.COLORS["background"],
            fg=styles.COLORS["text"]
        ).grid(row=row, column=0, sticky="w", pady=(0, 10))

        self.priority_var = tk.StringVar(value="中")
        priority_combo = ttk.Combobox(
            form_frame,
            textvariable=self.priority_var,
            values=["高", "中", "低"],
            state="readonly",
            width=28
        )
        priority_combo.grid(row=row, column=1, padx=(10, 0), pady=(0, 10), sticky="w")
        row += 1

        # 分类
        tk.Label(
            form_frame,
            text="分类:",
            font=styles.FONTS["normal"],
            bg=styles.COLORS["background"],
            fg=styles.COLORS["text"]
        ).grid(row=row, column=0, sticky="w", pady=(0, 10))

        categories = self.task_manager.get_categories()
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(
            form_frame,
            textvariable=self.category_var,
            values=categories,
            width=28
        )
        category_combo.grid(row=row, column=1, padx=(10, 0), pady=(0, 10), sticky="w")
        row += 1

        # 任务描述
        tk.Label(
            form_frame,
            text="任务描述:",
            font=styles.FONTS["normal"],
            bg=styles.COLORS["background"],
            fg=styles.COLORS["text"]
        ).grid(row=row, column=0, sticky="nw", pady=(0, 10))

        self.description_text = scrolledtext.ScrolledText(
            form_frame,
            width=30,
            height=8,
            font=("Arial", 10)
        )
        self.description_text.grid(row=row, column=1, padx=(10, 0), pady=(0, 10), sticky="ew")
        row += 1

        # 按钮框架
        button_frame = tk.Frame(form_frame, bg=styles.COLORS["background"])
        button_frame.grid(row=row, column=0, columnspan=2, pady=(20, 0))

        # 保存按钮
        ttk.Button(
            button_frame,
            text="保存",
            command=self.save_task,
            style="Primary.TButton"
        ).pack(side=tk.LEFT, padx=(0, 10))

        # 取消按钮
        ttk.Button(
            button_frame,
            text="取消",
            command=self.window.destroy
        ).pack(side=tk.LEFT)

    def load_task_data(self):
        """加载任务数据"""
        if self.task_data:
            self.title_var.set(self.task_data.title)

            due_date = self.task_data.due_date
            self.year_var.set(str(due_date.year))
            self.month_var.set(str(due_date.month))
            self.day_var.set(str(due_date.day))

            self.priority_var.set(self.task_data.priority.to_string("zh"))
            self.category_var.set(self.task_data.category or "")
            self.description_text.delete(1.0, tk.END)
            self.description_text.insert(1.0, self.task_data.description or "")

    def save_task(self):
        """保存任务"""
        # 验证输入
        title = self.title_var.get().strip()
        if not title:
            messagebox.showerror("错误", "请输入任务名称")
            return

        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            day = int(self.day_var.get())
            due_date = date(year, month, day)
        except (ValueError, TypeError):
            messagebox.showerror("错误", "请输入有效的日期")
            return

        priority = self.priority_var.get()
        category = self.category_var.get().strip()
        description = self.description_text.get(1.0, tk.END).strip()

        if self.on_save:
            task_data = {
                'title': title,
                'due_date': due_date,
                'priority': priority,
                'category': category,
                'description': description
            }
            if self.task_data:
                task_data['task_id'] = self.task_data.id
            self.on_save(task_data)

        self.window.destroy()


class MainWindow:
    """主窗口"""

    def __init__(self, root, task_manager):
        self.root = root
        self.task_manager = task_manager
        self.current_filter = "all"  # all, active, completed, overdue

        self.setup_window()
        self.create_menu()
        self.create_widgets()
        self.check_overdue_tasks()
        self.refresh_task_list()

    def setup_window(self):
        """设置窗口"""
        self.root.title("个人任务与日程管理系统")
        self.root.geometry("1000x700")
        self.root.configure(bg=styles.COLORS["background"])

        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="刷新", command=self.refresh_task_list)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)

        # 任务菜单
        task_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="任务", menu=task_menu)
        task_menu.add_command(label="添加任务", command=self.add_task)
        task_menu.add_command(label="编辑选中任务", command=self.edit_selected_task)
        task_menu.add_command(label="删除选中任务", command=self.delete_selected_task)
        task_menu.add_separator()
        task_menu.add_command(label="标记为完成", command=self.mark_task_complete)
        task_menu.add_command(label="标记为未完成", command=self.mark_task_incomplete)

        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="视图", menu=view_menu)
        view_menu.add_command(label="所有任务", command=lambda: self.filter_tasks("all"))
        view_menu.add_command(label="未完成", command=lambda: self.filter_tasks("active"))
        view_menu.add_command(label="已完成", command=lambda: self.filter_tasks("completed"))
        view_menu.add_command(label="已过期", command=lambda: self.filter_tasks("overdue"))

        # 排序菜单
        sort_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="排序", menu=sort_menu)
        sort_menu.add_command(label="按截止日期", command=lambda: self.sort_tasks("due_date"))
        sort_menu.add_command(label="按优先级", command=lambda: self.sort_tasks("priority"))
        sort_menu.add_command(label="按创建时间", command=lambda: self.sort_tasks("created_at"))
        sort_menu.add_command(label="按标题", command=lambda: self.sort_tasks("title"))

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)

    def create_widgets(self):
        """创建界面部件"""
        # 顶部工具栏
        self.create_toolbar()

        # 左侧过滤面板
        self.create_filter_panel()

        # 中间任务列表
        self.create_task_list()

        # 右侧任务详情
        self.create_task_detail()

        # 状态栏
        self.create_statusbar()

    def create_toolbar(self):
        """创建工具栏"""
        toolbar = tk.Frame(self.root, bg=styles.COLORS["secondary"], height=50)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # 欢迎信息
        self.welcome_label = tk.Label(
            toolbar,
            text=f"欢迎, {self.task_manager.current_user}",
            font=styles.FONTS["normal_bold"],
            bg=styles.COLORS["secondary"],
            fg=styles.COLORS["text"]
        )
        self.welcome_label.pack(side=tk.LEFT, padx=10)

        # 搜索框
        search_frame = tk.Frame(toolbar, bg=styles.COLORS["secondary"])
        search_frame.pack(side=tk.RIGHT, padx=10)

        tk.Label(
            search_frame,
            text="搜索:",
            font=styles.FONTS["normal"],
            bg=styles.COLORS["secondary"],
            fg=styles.COLORS["text"]
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.search_tasks())
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=20
        )
        search_entry.pack(side=tk.LEFT)

        # 登出按钮
        ttk.Button(
            toolbar,
            text="登出",
            command=self.logout
        ).pack(side=tk.RIGHT, padx=5)

    def create_filter_panel(self):
        """创建过滤面板"""
        filter_panel = tk.Frame(self.root, bg=styles.COLORS["sidebar"], width=200)
        filter_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 2), pady=5)
        filter_panel.pack_propagate(False)

        # 过滤标题
        filter_title = tk.Label(
            filter_panel,
            text="任务过滤",
            font=styles.FONTS["subtitle"],
            bg=styles.COLORS["sidebar"],
            fg=styles.COLORS["primary"]
        )
        filter_title.pack(pady=(10, 20))

        # 过滤按钮
        filter_buttons = [
            ("所有任务", "all"),
            ("未完成", "active"),
            ("已完成", "completed"),
            ("已过期", "overdue")
        ]

        for text, filter_type in filter_buttons:
            btn = ttk.Button(
                filter_panel,
                text=text,
                command=lambda ft=filter_type: self.filter_tasks(ft),
                style="Filter.TButton" if filter_type == self.current_filter else "TButton"
            )
            btn.pack(fill=tk.X, padx=10, pady=5)

        # 分类过滤
        tk.Label(
            filter_panel,
            text="\n按分类:",
            font=styles.FONTS["small_bold"],
            bg=styles.COLORS["sidebar"],
            fg=styles.COLORS["text"]
        ).pack(pady=(20, 5))

        categories = self.task_manager.get_categories()
        if categories:
            for category in categories:
                btn = ttk.Button(
                    filter_panel,
                    text=category,
                    command=lambda c=category: self.filter_by_category(c)
                )
                btn.pack(fill=tk.X, padx=10, pady=2)
        else:
            tk.Label(
                filter_panel,
                text="无分类",
                font=styles.FONTS["small"],
                bg=styles.COLORS["sidebar"],
                fg=styles.COLORS["muted"]
            ).pack()

        # 统计信息
        self.stats_label = tk.Label(
            filter_panel,
            text="",
            font=styles.FONTS["small"],
            bg=styles.COLORS["sidebar"],
            fg=styles.COLORS["muted"],
            justify=tk.LEFT
        )
        self.stats_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        self.update_stats()

    def create_task_list(self):
        """创建任务列表"""
        list_frame = tk.Frame(self.root, bg=styles.COLORS["background"])
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=5)

        # 列表标题
        title_frame = tk.Frame(list_frame, bg=styles.COLORS["background"])
        title_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(
            title_frame,
            text="任务列表",
            font=styles.FONTS["subtitle"],
            bg=styles.COLORS["background"],
            fg=styles.COLORS["text"]
        ).pack(side=tk.LEFT)

        # 添加任务按钮
        ttk.Button(
            title_frame,
            text="+ 添加任务",
            command=self.add_task,
            style="Primary.TButton"
        ).pack(side=tk.RIGHT)

        # 任务表格
        columns = ("选择", "状态", "标题", "截止日期", "优先级", "分类")
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            height=20
        )

        # 设置列
        self.tree.heading("选择", text="选择")
        self.tree.heading("状态", text="状态")
        self.tree.heading("标题", text="标题")
        self.tree.heading("截止日期", text="截止日期")
        self.tree.heading("优先级", text="优先级")
        self.tree.heading("分类", text="分类")

        # 设置列宽
        self.tree.column("选择", width=50, anchor=tk.CENTER)
        self.tree.column("状态", width=80, anchor=tk.CENTER)
        self.tree.column("标题", width=200)
        self.tree.column("截止日期", width=100, anchor=tk.CENTER)
        self.tree.column("优先级", width=60, anchor=tk.CENTER)
        self.tree.column("分类", width=100)

        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 布局
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))

        # 绑定事件
        self.tree.bind("<<TreeviewSelect>>", self.on_task_select)
        self.tree.bind("<Double-Button-1>", lambda e: self.edit_selected_task())

    def create_task_detail(self):
        """创建任务详情面板"""
        detail_frame = tk.Frame(self.root, bg=styles.COLORS["sidebar"], width=300)
        detail_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(2, 5), pady=5)
        detail_frame.pack_propagate(False)

        # 详情标题
        detail_title = tk.Label(
            detail_frame,
            text="任务详情",
            font=styles.FONTS["subtitle"],
            bg=styles.COLORS["sidebar"],
            fg=styles.COLORS["primary"]
        )
        detail_title.pack(pady=(10, 20))

        # 详情内容框架
        self.detail_content = tk.Frame(detail_frame, bg=styles.COLORS["sidebar"])
        self.detail_content.pack(fill=tk.BOTH, expand=True, padx=10)

        # 初始显示提示
        self.show_detail_placeholder()

    def create_statusbar(self):
        """创建状态栏"""
        self.statusbar = tk.Label(
            self.root,
            text="就绪",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=styles.FONTS["small"],
            bg=styles.COLORS["statusbar"],
            fg=styles.COLORS["text"]
        )
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def show_detail_placeholder(self):
        """显示详情占位符"""
        for widget in self.detail_content.winfo_children():
            widget.destroy()

        tk.Label(
            self.detail_content,
            text="选择任务查看详情",
            font=styles.FONTS["normal"],
            bg=styles.COLORS["sidebar"],
            fg=styles.COLORS["muted"]
        ).pack(expand=True)

    def show_task_detail(self, task):
        """显示任务详情"""
        for widget in self.detail_content.winfo_children():
            widget.destroy()

        # 任务标题
        tk.Label(
            self.detail_content,
            text=task.title,
            font=styles.FONTS["subtitle"],
            bg=styles.COLORS["sidebar"],
            fg=styles.COLORS["text"],
            wraplength=280
        ).pack(pady=(0, 20))

        # 详细信息框架
        info_frame = tk.Frame(self.detail_content, bg=styles.COLORS["sidebar"])
        info_frame.pack(fill=tk.X, pady=(0, 20))

        # 状态
        status = task.get_status()
        status_color = {
            "已完成": "#6BCF7F",
            "已过期": "#FF6B6B",
            "今天到期": "#FFD93D",
            "即将到期": "#FFA726",
            "进行中": "#4D96FF"
        }.get(status, "#888888")

        tk.Label(
            info_frame,
            text="状态:",
            font=styles.FONTS["small_bold"],
            bg=styles.COLORS["sidebar"],
            fg=styles.COLORS["text"]
        ).grid(row=0, column=0, sticky="w", pady=2)
        tk.Label(
            info_frame,
            text=status,
            font=styles.FONTS["small"],
            bg=styles.COLORS["sidebar"],
            fg=status_color
        ).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=2)

        # 截止日期
        tk.Label(
            info_frame,
            text="截止日期:",
            font=styles.FONTS["small_bold"],
            bg=styles.COLORS["sidebar"],
            fg=styles.COLORS["text"]
        ).grid(row=1, column=0, sticky="w", pady=2)
        tk.Label(
            info_frame,
            text=task.due_date.strftime("%Y年%m月%d日"),
            font=styles.FONTS["small"],
            bg=styles.COLORS["sidebar"],
            fg=styles.COLORS["text"]
        ).grid(row=1, column=1, sticky="w", padx=(10, 0), pady=2)

        # 优先级
        tk.Label(
            info_frame,
            text="优先级:",
            font=styles.FONTS["small_bold"],
            bg=styles.COLORS["sidebar"],
            fg=styles.COLORS["text"]
        ).grid(row=2, column=0, sticky="w", pady=2)
        tk.Label(
            info_frame,
            text=task.priority.to_string("zh"),
            font=styles.FONTS["small"],
            bg=styles.COLORS["sidebar"],
            fg=task.get_priority_color()
        ).grid(row=2, column=1, sticky="w", padx=(10, 0), pady=2)

        # 分类
        if task.category:
            tk.Label(
                info_frame,
                text="分类:",
                font=styles.FONTS["small_bold"],
                bg=styles.COLORS["sidebar"],
                fg=styles.COLORS["text"]
            ).grid(row=3, column=0, sticky="w", pady=2)
            tk.Label(
                info_frame,
                text=task.category,
                font=styles.FONTS["small"],
                bg=styles.COLORS["sidebar"],
                fg=styles.COLORS["text"]
            ).grid(row=3, column=1, sticky="w", padx=(10, 0), pady=2)

        # 创建时间
        tk.Label(
            info_frame,
            text="创建时间:",
            font=styles.FONTS["small_bold"],
            bg=styles.COLORS["sidebar"],
            fg=styles.COLORS["text"]
        ).grid(row=4, column=0, sticky="w", pady=2)
        tk.Label(
            info_frame,
            text=task.created_at.strftime("%Y-%m-%d %H:%M"),
            font=styles.FONTS["small"],
            bg=styles.COLORS["sidebar"],
            fg=styles.COLORS["text"]
        ).grid(row=4, column=1, sticky="w", padx=(10, 0), pady=2)

        # 描述标题
        tk.Label(
            self.detail_content,
            text="任务描述:",
            font=styles.FONTS["small_bold"],
            bg=styles.COLORS["sidebar"],
            fg=styles.COLORS["text"],
            anchor="w"
        ).pack(fill=tk.X, pady=(10, 5))

        # 描述内容
        if task.description:
            description_text = scrolledtext.ScrolledText(
                self.detail_content,
                width=30,
                height=10,
                font=("Arial", 9),
                wrap=tk.WORD,
                bg="#f0f0f0",
                relief=tk.FLAT
            )
            description_text.insert(1.0, task.description)
            description_text.config(state=tk.DISABLED)
            description_text.pack(fill=tk.BOTH, expand=True)
        else:
            tk.Label(
                self.detail_content,
                text="无描述",
                font=styles.FONTS["small"],
                bg=styles.COLORS["sidebar"],
                fg=styles.COLORS["muted"],
                wraplength=280
            ).pack(fill=tk.X, pady=5)

        # 操作按钮
        button_frame = tk.Frame(self.detail_content, bg=styles.COLORS["sidebar"])
        button_frame.pack(fill=tk.X, pady=(20, 0))

        if not task.completed:
            ttk.Button(
                button_frame,
                text="标记完成",
                command=lambda: self.mark_task_complete(task.id),
                style="Success.TButton"
            ).pack(side=tk.LEFT, padx=(0, 5))
        else:
            ttk.Button(
                button_frame,
                text="标记未完成",
                command=lambda: self.mark_task_incomplete(task.id),
                style="Warning.TButton"
            ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            button_frame,
            text="编辑",
            command=lambda: self.edit_task(task)
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            button_frame,
            text="删除",
            command=lambda: self.delete_task(task.id),
            style="Danger.TButton"
        ).pack(side=tk.LEFT)

    def refresh_task_list(self):
        """刷新任务列表"""
        # 清空当前列表
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 获取任务列表
        tasks = self.task_manager.get_all_tasks()

        # 应用过滤
        if self.current_filter == "active":
            tasks = [t for t in tasks if not t.completed]
        elif self.current_filter == "completed":
            tasks = [t for t in tasks if t.completed]
        elif self.current_filter == "overdue":
            tasks = self.task_manager.get_overdue_tasks()

        # 应用搜索
        search_text = self.search_var.get().strip()
        if search_text:
            tasks = self.task_manager.search_tasks(search_text)

        # 应用排序
        if hasattr(self, 'current_sort'):
            tasks = self.task_manager.sort_tasks(self.current_sort[0], self.current_sort[1])

        # 添加到列表
        for task in tasks:
            status = task.get_status()
            status_color = {
                "已完成": "#6BCF7F",
                "已过期": "#FF6B6B",
                "今天到期": "#FFD93D",
                "即将到期": "#FFA726",
                "进行中": "#4D96FF"
            }.get(status, "#888888")

            priority_color = task.get_priority_color()

            # 插入数据
            item = self.tree.insert(
                "",
                tk.END,
                values=(
                    "✓" if task.completed else "",
                    status,
                    task.title,
                    task.due_date.strftime("%Y-%m-%d"),
                    task.priority.to_string("zh"),
                    task.category
                ),
                tags=(task.id,)
            )

            # 设置行颜色
            if task.completed:
                self.tree.item(item, tags=("completed",))
            elif status == "已过期":
                self.tree.item(item, tags=("overdue",))

        # 更新统计信息
        self.update_stats()
        self.statusbar.config(text=f"共 {len(tasks)} 个任务")

    def update_stats(self):
        """更新统计信息"""
        all_tasks = len(self.task_manager.get_all_tasks())
        active_tasks = len([t for t in self.task_manager.get_all_tasks() if not t.completed])
        completed_tasks = len([t for t in self.task_manager.get_all_tasks() if t.completed])
        overdue_tasks = len(self.task_manager.get_overdue_tasks())

        stats_text = f"""统计信息:
总任务: {all_tasks}
未完成: {active_tasks}
已完成: {completed_tasks}
已过期: {overdue_tasks}"""

        self.stats_label.config(text=stats_text)

    def filter_tasks(self, filter_type):
        """过滤任务"""
        self.current_filter = filter_type
        self.refresh_task_list()

        # 更新按钮样式
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_name() == "filter_panel":
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button):
                        if child["text"] in ["所有任务", "未完成", "已完成", "已过期"]:
                            if (child["text"] == "所有任务" and filter_type == "all") or \
                                    (child["text"] == "未完成" and filter_type == "active") or \
                                    (child["text"] == "已完成" and filter_type == "completed") or \
                                    (child["text"] == "已过期" and filter_type == "overdue"):
                                child.config(style="Filter.TButton")
                            else:
                                child.config(style="TButton")

    def filter_by_category(self, category):
        """按分类过滤"""
        tasks = self.task_manager.get_tasks_by_category(category)
        self.show_filtered_tasks(tasks, f"分类: {category}")

    def show_filtered_tasks(self, tasks, title):
        """显示过滤后的任务"""
        # 清空当前列表
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 添加到列表
        for task in tasks:
            status = task.get_status()
            self.tree.insert(
                "",
                tk.END,
                values=(
                    "✓" if task.completed else "",
                    status,
                    task.title,
                    task.due_date.strftime("%Y-%m-%d"),
                    task.priority.to_string("zh"),
                    task.category
                ),
                tags=(task.id,)
            )

        self.statusbar.config(text=f"{title} - 共 {len(tasks)} 个任务")

    def sort_tasks(self, by, reverse=False):
        """排序任务"""
        self.current_sort = (by, reverse)
        self.refresh_task_list()
        sort_name = {"due_date": "截止日期", "priority": "优先级",
                     "created_at": "创建时间", "title": "标题"}[by]
        direction = "降序" if reverse else "升序"
        self.statusbar.config(text=f"已按{sort_name}{direction}排序")

    def search_tasks(self):
        """搜索任务"""
        self.refresh_task_list()

    def on_task_select(self, event):
        """任务选择事件"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            task_id = self.tree.item(item, "tags")[0]
            task = self.task_manager.get_task(task_id)
            if task:
                self.show_task_detail(task)

    def add_task(self):
        """添加任务"""

        def save_callback(task_data):
            from task_manager import Task, Priority
            task = Task(
                title=task_data['title'],
                due_date=task_data['due_date'],
                priority=Priority.from_string(task_data['priority']),
                category=task_data['category'],
                description=task_data['description']
            )
            self.task_manager.add_task(task)
            self.refresh_task_list()
            self.update_stats()
            messagebox.showinfo("成功", "任务添加成功")

        TaskDialog(self.root, "添加任务", self.task_manager, on_save=save_callback)

    def edit_task(self, task):
        """编辑任务"""

        def save_callback(task_data):
            self.task_manager.update_task(
                task_data['task_id'],
                title=task_data['title'],
                due_date=task_data['due_date'],
                priority=task_data['priority'],
                category=task_data['category'],
                description=task_data['description']
            )
            self.refresh_task_list()
            self.show_detail_placeholder()
            messagebox.showinfo("成功", "任务更新成功")

        TaskDialog(self.root, "编辑任务", self.task_manager, task, save_callback)

    def edit_selected_task(self):
        """编辑选中的任务"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个任务")
            return

        item = selection[0]
        task_id = self.tree.item(item, "tags")[0]
        task = self.task_manager.get_task(task_id)

        if task:
            self.edit_task(task)
        else:
            messagebox.showerror("错误", "任务不存在")

    def delete_task(self, task_id):
        """删除任务"""
        if messagebox.askyesno("确认", "确定要删除这个任务吗？"):
            if self.task_manager.delete_task(task_id):
                self.refresh_task_list()
                self.show_detail_placeholder()
                messagebox.showinfo("成功", "任务删除成功")
            else:
                messagebox.showerror("错误", "删除失败")

    def delete_selected_task(self):
        """删除选中的任务"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个任务")
            return

        item = selection[0]
        task_id = self.tree.item(item, "tags")[0]
        self.delete_task(task_id)

    def mark_task_complete(self, task_id=None):
        """标记任务为完成"""
        if task_id is None:
            selection = self.tree.selection()
            if not selection:
                messagebox.showwarning("警告", "请先选择一个任务")
                return
            item = selection[0]
            task_id = self.tree.item(item, "tags")[0]

        task = self.task_manager.get_task(task_id)
        if task and not task.completed:
            task.mark_complete()
            self.task_manager.save_tasks()
            self.refresh_task_list()
            if hasattr(self, 'detail_content'):
                self.show_detail_placeholder()
            messagebox.showinfo("成功", "任务已标记为完成")

    def mark_task_incomplete(self, task_id=None):
        """标记任务为未完成"""
        if task_id is None:
            selection = self.tree.selection()
            if not selection:
                messagebox.showwarning("警告", "请先选择一个任务")
                return
            item = selection[0]
            task_id = self.tree.item(item, "tags")[0]

        task = self.task_manager.get_task(task_id)
        if task and task.completed:
            task.mark_incomplete()
            self.task_manager.save_tasks()
            self.refresh_task_list()
            if hasattr(self, 'detail_content'):
                self.show_detail_placeholder()
            messagebox.showinfo("成功", "任务已标记为未完成")

    def check_overdue_tasks(self):
        """检查过期任务"""
        overdue_tasks = self.task_manager.get_overdue_tasks()
        upcoming_tasks = self.task_manager.get_upcoming_tasks(days=1)

        if overdue_tasks:
            messagebox.showwarning("提醒", f"您有 {len(overdue_tasks)} 个任务已过期！")

        if upcoming_tasks:
            messagebox.showinfo("提醒", f"您有 {len(upcoming_tasks)} 个任务今天到期！")

    def show_about(self):
        """显示关于对话框"""
        about_text = """个人任务与日程管理系统

版本: 1.0
作者: Gin
描述: 基于Tkinter的桌面任务管理应用

主要功能:
• 用户登录与注册
• 任务增删改查
• 任务分类与优先级
• 到期提醒
• 数据持久化存储

"""

        messagebox.showinfo("关于", about_text)

    def logout(self):
        """登出"""
        if messagebox.askyesno("确认", "确定要登出吗？"):
            self.task_manager.logout()
            self.root.destroy()