# styles.py
import tkinter as tk
from tkinter import ttk
from typing import Dict, Tuple

# 颜色定义
COLORS = {
    "primary": "#4A90E2",  # 主色
    "secondary": "#F5F5F5",  # 次要色
    "accent": "#FF6B6B",  # 强调色
    "success": "#6BCF7F",  # 成功色
    "warning": "#FFD93D",  # 警告色
    "danger": "#FF6B6B",  # 危险色
    "background": "#FFFFFF",  # 背景色
    "sidebar": "#F8F9FA",  # 侧边栏背景
    "statusbar": "#E9ECEF",  # 状态栏背景
    "text": "#212529",  # 文字色
    "muted": "#6C757D",  # 弱化文字色
    "border": "#DEE2E6",  # 边框色
    "hover": "#E3F2FD",  # 悬停色
    "selected": "#E3F2FD"  # 选中色
}

# 字体定义
FONTS = {
    "title": ("Microsoft YaHei", 16, "bold"),
    "subtitle": ("Microsoft YaHei", 12, "bold"),
    "normal": ("Microsoft YaHei", 10),
    "normal_bold": ("Microsoft YaHei", 10, "bold"),
    "small": ("Microsoft YaHei", 9),
    "small_bold": ("Microsoft YaHei", 9, "bold")
}


def configure_styles():
    """配置ttk样式"""
    style = ttk.Style()

    # 配置主题
    style.theme_use('clam')

    # 全局样式
    style.configure('.',
                    background=COLORS["background"],
                    foreground=COLORS["text"])

    # 配置按钮样式
    style.configure('TButton',
                    font=FONTS["normal"],
                    padding=6,
                    relief="flat")
    style.map('TButton',
              background=[('active', COLORS["hover"]),
                          ('pressed', COLORS["selected"])])

    style.configure('Primary.TButton',
                    background=COLORS["primary"],
                    foreground='white',
                    borderwidth=0)
    style.map('Primary.TButton',
              background=[('active', '#3A7BC8'), ('pressed', '#2C6BB0')])

    style.configure('Success.TButton',
                    background=COLORS["success"],
                    foreground='white',
                    borderwidth=0)
    style.map('Success.TButton',
              background=[('active', '#5ABF72'), ('pressed', '#4AA862')])

    style.configure('Warning.TButton',
                    background=COLORS["warning"],
                    foreground='white',
                    borderwidth=0)
    style.map('Warning.TButton',
              background=[('active', '#E6C336'), ('pressed', '#CCAA2D')])

    style.configure('Danger.TButton',
                    background=COLORS["danger"],
                    foreground='white',
                    borderwidth=0)
    style.map('Danger.TButton',
              background=[('active', '#E55A5A'), ('pressed', '#CC4949')])

    style.configure('Filter.TButton',
                    background=COLORS["sidebar"],
                    foreground=COLORS["text"],
                    borderwidth=0)
    style.map('Filter.TButton',
              background=[('active', COLORS["hover"])])

    # 配置Treeview样式
    style.configure('Treeview',
                    font=FONTS["small"],
                    rowheight=25,
                    background=COLORS["background"],
                    fieldbackground=COLORS["background"],
                    foreground=COLORS["text"],
                    borderwidth=1,
                    relief="solid")

    style.configure('Treeview.Heading',
                    font=FONTS["small_bold"],
                    background=COLORS["sidebar"],
                    foreground=COLORS["text"],
                    relief="flat",
                    borderwidth=1)

    style.map('Treeview',
              background=[('selected', COLORS["selected"])],
              foreground=[('selected', COLORS["text"])])

    # 标签样式
    style.configure('TLabel',
                    font=FONTS["normal"],
                    background=COLORS["background"],
                    foreground=COLORS["text"])

    style.configure('Title.TLabel',
                    font=FONTS["title"],
                    foreground=COLORS["primary"])

    style.configure('Subtitle.TLabel',
                    font=FONTS["subtitle"],
                    foreground=COLORS["text"])

    style.configure('Muted.TLabel',
                    foreground=COLORS["muted"])

    # 输入框样式
    style.configure('TEntry',
                    fieldbackground=COLORS["background"],
                    bordercolor=COLORS["border"],
                    lightcolor=COLORS["background"],
                    darkcolor=COLORS["background"])

    style.map('TEntry',
              fieldbackground=[('disabled', COLORS["sidebar"])])

    # 组合框样式
    style.configure('TCombobox',
                    fieldbackground=COLORS["background"],
                    background=COLORS["background"],
                    bordercolor=COLORS["border"])

    # 框架样式
    style.configure('TFrame',
                    background=COLORS["background"])

    style.configure('Card.TFrame',
                    background=COLORS["sidebar"],
                    relief="raised",
                    borderwidth=1)

    # 滚动条样式
    style.configure('Vertical.TScrollbar',
                    background=COLORS["sidebar"],
                    bordercolor=COLORS["border"],
                    arrowcolor=COLORS["muted"],
                    troughcolor=COLORS["background"])

    style.configure('Horizontal.TScrollbar',
                    background=COLORS["sidebar"],
                    bordercolor=COLORS["border"],
                    arrowcolor=COLORS["muted"],
                    troughcolor=COLORS["background"])

    return style


def create_rounded_button(parent, text, command, style="TButton", **kwargs):
    """创建圆角按钮（如果需要）"""
    btn = ttk.Button(parent, text=text, command=command, style=style, **kwargs)
    return btn


# 简化的颜色和字体访问函数
def get_color(color_name: str) -> str:
    """获取颜色"""
    return COLORS.get(color_name, COLORS["text"])


def get_font(font_name: str) -> Tuple[str, int, str]:
    """获取字体"""
    return FONTS.get(font_name, FONTS["normal"])