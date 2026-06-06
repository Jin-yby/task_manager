# analytics.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Any
from data_handler import DataHandler
from task_manager import TaskManager, Task, Priority


class AnalyticsDashboard:
    """高级分析与统计面板"""

    def __init__(self, parent, task_manager: TaskManager):
        self.parent = parent
        self.task_manager = task_manager
        self.figures = {}  # 存储图表对象
        self.setup_ui()

    def setup_ui(self):
        """设置分析面板UI"""
        # 创建主框架
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建标题
        title_label = ttk.Label(
            self.main_frame,
            text="Analytics & Insights",
            font=("Microsoft YaHei", 18, "bold")
        )
        title_label.pack(pady=(0, 20))

        # 创建图表容器 - 2x2网格
        self.chart_grid = ttk.Frame(self.main_frame)
        self.chart_grid.pack(fill=tk.BOTH, expand=True)

        # 创建4个图表区域
        self.create_chart_frames()

        # 初始加载图表
        self.refresh_charts()

    def create_chart_frames(self):
        """创建图表框架"""
        # 图表1: 任务状态分布 (饼图)
        self.pie_frame = ttk.LabelFrame(
            self.chart_grid,
            text="Task Status Distribution",
            padding=10
        )
        self.pie_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # 图表2: 任务按科目分布 (水平条形图)
        self.bar_frame = ttk.LabelFrame(
            self.chart_grid,
            text="Tasks by Subject",
            padding=10
        )
        self.bar_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # 图表3: 优先级分布 (柱状图)
        self.priority_frame = ttk.LabelFrame(
            self.chart_grid,
            text="Priority Score Distribution",
            padding=10
        )
        self.priority_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # 图表4: 完成统计 (列表+进度条)
        self.stats_frame = ttk.LabelFrame(
            self.chart_grid,
            text="Completion Stats",
            padding=10
        )
        self.stats_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # 配置网格权重
        self.chart_grid.columnconfigure(0, weight=1)
        self.chart_grid.columnconfigure(1, weight=1)
        self.chart_grid.rowconfigure(0, weight=1)
        self.chart_grid.rowconfigure(1, weight=1)

    def refresh_charts(self):
        """刷新所有图表"""
        self.refresh_status_pie_chart()
        self.refresh_subject_bar_chart()
        self.refresh_priority_chart()
        self.refresh_completion_stats()

    def refresh_status_pie_chart(self):
        """刷新任务状态饼图"""
        # 清除旧图表
        for widget in self.pie_frame.winfo_children():
            widget.destroy()

        # 获取状态数据
        status_counts = self.task_manager.get_status_distribution()
        labels = list(status_counts.keys())
        sizes = list(status_counts.values())
        colors = ['#FF6B6B', '#4A90E2', '#6BCF7F']  # 红、蓝、绿

        # 创建图表
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.0f%%',
            colors=colors,
            startangle=90,
            wedgeprops={'edgecolor': 'w', 'linewidth': 1}
        )

        # 设置字体
        for text in texts:
            text.set_fontsize(9)
            text.set_fontname("Microsoft YaHei")
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_fontname("Microsoft YaHei")
            autotext.set_color('white')
            autotext.set_weight('bold')

        ax.set_title('Task Status Distribution', fontsize=11, fontname="Microsoft YaHei")

        # 嵌入到Tkinter
        canvas = FigureCanvasTkAgg(fig, self.pie_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 保存图表对象
        self.figures['status_pie'] = (fig, canvas)

    def refresh_subject_bar_chart(self):
        """刷新科目分布条形图"""
        # 清除旧图表
        for widget in self.bar_frame.winfo_children():
            widget.destroy()

        # 获取科目数据
        subject_counts = self.task_manager.get_subject_distribution()
        subjects = list(subject_counts.keys())
        counts = list(subject_counts.values())

        # 创建图表
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        bars = ax.barh(
            subjects,
            counts,
            color=['#6C5CE7', '#00B894', '#FDCB6E', '#E17055'],
            height=0.6
        )

        # 添加数值标签
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + 0.1,
                bar.get_y() + bar.get_height() / 2,
                f'{int(width)}',
                ha='left',
                va='center',
                fontsize=9,
                fontname="Microsoft YaHei"
            )

        ax.set_xlabel('Number of Tasks', fontsize=10, fontname="Microsoft YaHei")
        ax.set_title('Tasks by Subject', fontsize=11, fontname="Microsoft YaHei")
        ax.set_xlim(0, max(counts) + 2)

        # 嵌入到Tkinter
        canvas = FigureCanvasTkAgg(fig, self.bar_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 保存图表对象
        self.figures['subject_bar'] = (fig, canvas)

    def refresh_priority_chart(self):
        """刷新优先级分布图"""
        # 清除旧图表
        for widget in self.priority_frame.winfo_children():
            widget.destroy()

        # 获取优先级数据
        priority_counts = self.task_manager.get_priority_distribution()
        priorities = list(priority_counts.keys())
        counts = list(priority_counts.values())

        # 创建图表
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        bars = ax.bar(
            priorities,
            counts,
            color=['#FFD93D', '#FF9F1C', '#E71D36'],
            alpha=0.8
        )

        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.1,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=9,
                fontname="Microsoft YaHei"
            )

        ax.set_xlabel('Priority Score', fontsize=10, fontname="Microsoft YaHei")
        ax.set_ylabel('Tasks', fontsize=10, fontname="Microsoft YaHei")
        ax.set_title('Priority Score Distribution', fontsize=11, fontname="Microsoft YaHei")
        ax.set_xticks(priorities)

        # 嵌入到Tkinter
        canvas = FigureCanvasTkAgg(fig, self.priority_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 保存图表对象
        self.figures['priority_bar'] = (fig, canvas)

    def refresh_completion_stats(self):
        """刷新完成统计"""
        # 清除旧内容
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # 获取统计
        stats = self.task_manager.get_completion_stats()

        # 创建统计显示
        stats_container = ttk.Frame(self.stats_frame)
        stats_container.pack(fill=tk.BOTH, expand=True)

        # 完成率
        rate_frame = ttk.Frame(stats_container)
        rate_frame.pack(fill=tk.X, pady=5)

        ttk.Label(rate_frame, text="Overall Completion Rate:",
                  font=("Microsoft YaHei", 10, "bold")).pack(side=tk.LEFT)

        rate_value = ttk.Label(rate_frame, text=f"{stats['completion_rate']}%",
                               font=("Microsoft YaHei", 10, "bold"),
                               foreground="#4A90E2")
        rate_value.pack(side=tk.RIGHT)

        # 任务状态统计
        for status, count in stats['status_counts'].items():
            stat_row = ttk.Frame(stats_container)
            stat_row.pack(fill=tk.X, pady=2)

            # 状态图标和标签
            icon = "✅" if status == "Completed" else "⏳" if status == "In Progress" else "❌"
            ttk.Label(stat_row, text=f"{icon} {status}:").pack(side=tk.LEFT)
            ttk.Label(stat_row, text=str(count)).pack(side=tk.RIGHT)

        # 添加进度条
        progress_frame = ttk.Frame(stats_container)
        progress_frame.pack(fill=tk.X, pady=5)

        ttk.Label(progress_frame, text="Progress:").pack(side=tk.LEFT)

        progress_var = tk.DoubleVar(value=stats['completion_rate'])
        progress = ttk.Progressbar(
            progress_frame,
            variable=progress_var,
            maximum=100,
            length=200
        )
        progress.pack(side=tk.RIGHT, padx=5)