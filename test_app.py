# test_app.py
import unittest
from datetime import date, timedelta
from data_handler import DataHandler
from task_manager import TaskManager, Task, Priority
import os
import shutil


class TestTaskManager(unittest.TestCase):
    """测试任务管理器"""

    def setUp(self):
        """测试前准备"""
        # 使用测试数据目录
        self.data_dir = "test_data"
        self.data_handler = DataHandler(data_dir=self.data_dir)
        self.task_manager = TaskManager(self.data_handler)

        # 注册测试用户
        self.test_username = "test_user"
        self.test_password = "password123"

        # 清除可能存在的测试用户
        if self.data_handler.user_exists(self.test_username):
            # 删除任务文件
            tasks_file = os.path.join(self.data_dir, "tasks", f"{self.test_username}_tasks.json")
            if os.path.exists(tasks_file):
                os.remove(tasks_file)

            # 从用户文件中删除
            users = self.data_handler._load_users()
            if self.test_username in users:
                del users[self.test_username]
                self.data_handler._save_users(users)

        # 注册新用户
        self.data_handler.register_user(self.test_username, self.test_password)
        self.task_manager.current_user = self.test_username
        self.task_manager.tasks = []

    def tearDown(self):
        """测试后清理"""
        # 清理数据目录
        if os.path.exists(self.data_dir):
            shutil.rmtree(self.data_dir)

    def test_task_creation(self):
        """测试任务创建"""
        task = Task("测试任务", date.today(), Priority.HIGH, "测试描述", "工作")
        self.assertEqual(task.title, "测试任务")
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(task.category, "工作")
        self.assertEqual(task.description, "测试描述")
        self.assertFalse(task.completed)
        self.assertIsInstance(task.id, str)

    def test_task_priority_conversion(self):
        """测试优先级转换"""
        # 从字符串转换
        self.assertEqual(Priority.from_string("高"), Priority.HIGH)
        self.assertEqual(Priority.from_string("中"), Priority.MEDIUM)
        self.assertEqual(Priority.from_string("低"), Priority.LOW)

        # 转换为字符串
        self.assertEqual(Priority.HIGH.to_string("zh"), "高")
        self.assertEqual(Priority.MEDIUM.to_string("zh"), "中")
        self.assertEqual(Priority.LOW.to_string("zh"), "低")

        # 默认语言
        self.assertEqual(Priority.HIGH.to_string(), "高")

    def test_task_status(self):
        """测试任务状态"""
        # 测试过期任务
        yesterday = date.today() - timedelta(days=1)
        task = Task("过期任务", yesterday, Priority.MEDIUM)
        self.assertEqual(task.get_status(), "已过期")

        # 测试今天到期
        today = date.today()
        task = Task("今天任务", today, Priority.MEDIUM)
        self.assertEqual(task.get_status(), "今天到期")

        # 测试即将到期
        tomorrow = date.today() + timedelta(days=1)
        task = Task("明天任务", tomorrow, Priority.MEDIUM)
        self.assertEqual(task.get_status(), "即将到期")

        # 测试进行中
        future = date.today() + timedelta(days=7)
        task = Task("未来任务", future, Priority.MEDIUM)
        self.assertEqual(task.get_status(), "进行中")

        # 测试已完成
        task = Task("已完成任务", date.today(), Priority.MEDIUM)
        task.mark_complete()
        self.assertEqual(task.get_status(), "已完成")

    def test_task_completion(self):
        """测试任务完成状态"""
        task = Task("测试任务", date.today(), Priority.MEDIUM)
        self.assertFalse(task.completed)
        self.assertIsNone(task.completed_at)

        # 标记为完成
        task.mark_complete()
        self.assertTrue(task.completed)
        self.assertIsNotNone(task.completed_at)

        # 标记为未完成
        task.mark_incomplete()
        self.assertFalse(task.completed)
        self.assertIsNone(task.completed_at)

    def test_task_dict_conversion(self):
        """测试任务字典转换"""
        task = Task(
            title="测试任务",
            due_date=date.today(),
            priority=Priority.HIGH,
            description="测试描述",
            category="工作"
        )

        # 转换为字典
        task_dict = task.to_dict()
        self.assertEqual(task_dict["title"], "测试任务")
        self.assertEqual(task_dict["priority"], Priority.HIGH.value)
        self.assertEqual(task_dict["category"], "工作")
        self.assertEqual(task_dict["description"], "测试描述")
        self.assertEqual(task_dict["completed"], False)

        # 从字典创建
        new_task = Task.from_dict(task_dict)
        self.assertEqual(new_task.title, task.title)
        self.assertEqual(new_task.priority, task.priority)
        self.assertEqual(new_task.category, task.category)
        self.assertEqual(new_task.due_date, task.due_date)
        self.assertEqual(new_task.completed, task.completed)

    def test_task_manager_operations(self):
        """测试任务管理器操作"""
        # 登录用户
        self.task_manager.login(self.test_username, self.test_password)

        # 添加任务
        task = Task("测试任务", date.today(), Priority.HIGH)
        self.task_manager.add_task(task)
        self.assertEqual(len(self.task_manager.tasks), 1)

        # 获取任务
        retrieved_task = self.task_manager.get_task(task.id)
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.title, "测试任务")
        self.assertEqual(retrieved_task.priority, Priority.HIGH)

        # 更新任务
        self.task_manager.update_task(
            task.id,
            title="更新后的任务",
            priority="低",  # 测试字符串输入
            description="新的描述"
        )
        updated_task = self.task_manager.get_task(task.id)
        self.assertEqual(updated_task.title, "更新后的任务")
        self.assertEqual(updated_task.priority, Priority.LOW)
        self.assertEqual(updated_task.description, "新的描述")

        # 删除任务
        result = self.task_manager.delete_task(task.id)
        self.assertTrue(result)
        self.assertEqual(len(self.task_manager.tasks), 0)

    def test_task_filtering(self):
        """测试任务过滤"""
        # 登录用户
        self.task_manager.login(self.test_username, self.test_password)

        # 添加几个测试任务
        today = date.today()

        # 已完成任务
        task1 = Task("已完成任务", today, Priority.LOW)
        task1.mark_complete()
        self.task_manager.add_task(task1)

        # 未完成任务
        task2 = Task("未完成任务", today, Priority.MEDIUM)
        self.task_manager.add_task(task2)

        # 过期任务
        task3 = Task("过期任务", today - timedelta(days=7), Priority.HIGH)
        self.task_manager.add_task(task3)

        # 测试过滤
        all_tasks = self.task_manager.get_all_tasks()
        self.assertEqual(len(all_tasks), 3)

        active_tasks = self.task_manager.get_all_tasks(filter_completed=False)
        self.assertEqual(len(active_tasks), 2)  # task2 和 task3

        completed_tasks = self.task_manager.get_all_tasks(filter_completed=True)
        self.assertEqual(len(completed_tasks), 1)  # task1

        overdue_tasks = self.task_manager.get_overdue_tasks()
        self.assertEqual(len(overdue_tasks), 1)  # task3

    def test_task_sorting(self):
        """测试任务排序"""
        # 登录用户
        self.task_manager.login(self.test_username, self.test_password)

        today = date.today()

        # 添加不同优先级的任务
        task1 = Task("低优先级任务", today + timedelta(days=3), Priority.LOW)
        task2 = Task("高优先级任务", today, Priority.HIGH)
        task3 = Task("中优先级任务", today + timedelta(days=1), Priority.MEDIUM)

        self.task_manager.add_task(task1)
        self.task_manager.add_task(task2)
        self.task_manager.add_task(task3)

        # 按优先级排序（高优先在前）
        sorted_by_priority = self.task_manager.sort_tasks(by="priority", reverse=True)
        self.assertEqual(sorted_by_priority[0].priority, Priority.HIGH)
        self.assertEqual(sorted_by_priority[1].priority, Priority.MEDIUM)
        self.assertEqual(sorted_by_priority[2].priority, Priority.LOW)

        # 按截止日期排序（早的在前）
        sorted_by_date = self.task_manager.sort_tasks(by="due_date")
        self.assertEqual(sorted_by_date[0].due_date, today)
        self.assertEqual(sorted_by_date[1].due_date, today + timedelta(days=1))
        self.assertEqual(sorted_by_date[2].due_date, today + timedelta(days=3))

    def test_data_persistence(self):
        """测试数据持久化"""
        # 注册新用户
        new_user = "persistence_user"
        new_password = "test123"

        # 清除旧数据
        if self.data_handler.user_exists(new_user):
            users = self.data_handler._load_users()
            del users[new_user]
            self.data_handler._save_users(users)

        # 注册用户
        self.assertTrue(self.data_handler.register_user(new_user, new_password))

        # 创建任务管理器并登录
        task_manager1 = TaskManager(self.data_handler)
        self.assertTrue(task_manager1.login(new_user, new_password))

        # 添加任务
        task = Task("持久化测试", date.today(), Priority.HIGH, "测试数据持久化")
        task_manager1.add_task(task)

        # 保存任务
        task_manager1.save_tasks()

        # 创建新的任务管理器实例
        task_manager2 = TaskManager(self.data_handler)
        self.assertTrue(task_manager2.login(new_user, new_password))

        # 验证数据
        self.assertEqual(len(task_manager2.tasks), 1)
        loaded_task = task_manager2.tasks[0]
        self.assertEqual(loaded_task.title, "持久化测试")
        self.assertEqual(loaded_task.priority, Priority.HIGH)
        self.assertEqual(loaded_task.description, "测试数据持久化")

    def test_user_authentication(self):
        """测试用户认证"""
        # 测试用户存在检查
        self.assertTrue(self.data_handler.user_exists(self.test_username))
        self.assertFalse(self.data_handler.user_exists("不存在的用户"))

        # 测试用户验证
        self.assertTrue(self.data_handler.validate_user(self.test_username, self.test_password))
        self.assertFalse(self.data_handler.validate_user(self.test_username, "错误密码"))
        self.assertFalse(self.data_handler.validate_user("不存在的用户", "密码"))

    def test_task_search(self):
        """测试任务搜索"""
        # 登录用户
        self.task_manager.login(self.test_username, self.test_password)

        # 添加测试任务
        task1 = Task("Python编程作业", date.today(), Priority.HIGH, "完成Python作业")
        task2 = Task("数学练习题", date.today(), Priority.MEDIUM, "完成数学习题")
        task3 = Task("英语阅读", date.today(), Priority.LOW, "阅读英语文章")

        self.task_manager.add_task(task1)
        self.task_manager.add_task(task2)
        self.task_manager.add_task(task3)

        # 测试搜索
        python_tasks = self.task_manager.search_tasks("python")
        self.assertEqual(len(python_tasks), 1)
        self.assertEqual(python_tasks[0].title, "Python编程作业")

        # 测试搜索不区分大小写
        math_tasks = self.task_manager.search_tasks("数学")
        self.assertEqual(len(math_tasks), 1)
        self.assertEqual(math_tasks[0].title, "数学练习题")

        # 测试搜索描述
        eng_tasks = self.task_manager.search_tasks("英语")
        self.assertEqual(len(eng_tasks), 1)
        self.assertEqual(eng_tasks[0].title, "英语阅读")

        # 测试无结果
        no_tasks = self.task_manager.search_tasks("不存在的关键词")
        self.assertEqual(len(no_tasks), 0)


def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("开始运行个人任务管理系统测试")
    print("=" * 60)

    # 加载测试套件
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTaskManager)

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 60)
    print("测试结果统计:")
    print(f"运行测试数: {result.testsRun}")
    print(f"通过测试数: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败测试数: {len(result.failures)}")
    print(f"错误测试数: {len(result.errors)}")
    print("=" * 60)

    if result.wasSuccessful():
        print("🎉 所有测试通过！代码质量良好。")
    else:
        print("⚠️  部分测试失败，请检查代码。")

        # 显示失败详情
        if result.failures:
            print("\n失败测试详情:")
            for test, traceback in result.failures:
                print(f"\n{test.id()}:")
                print(traceback)

        if result.errors:
            print("\n错误测试详情:")
            for test, traceback in result.errors:
                print(f"\n{test.id()}:")
                print(traceback)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()

    # 根据测试结果返回适当的退出码
    import sys

    sys.exit(0 if success else 1)