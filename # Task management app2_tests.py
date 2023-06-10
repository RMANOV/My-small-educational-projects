import unittest
from unittest import mock
from unittest.mock import patch, mock_open
from task_manager import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.task_manager = TaskManager('test_tasks.csv')
        
    def test_create_task(self):
        self.task_manager.create_task('Task 1', 'Description 1')
        self.assertEqual(len(self.task_manager.tasks), 1)
        self.assertEqual(self.task_manager.tasks[0].title, 'Task 1')
        self.assertEqual(self.task_manager.tasks[0].description, 'Description 1')
        
    def test_edit_task(self):
        self.task_manager.create_task('Task 1', 'Description 1')
        self.task_manager.edit_task('Task 1', 'New Title', 'New Description')
        self.assertEqual(self.task_manager.tasks[0].title, 'New Title')
        self.assertEqual(self.task_manager.tasks[0].description, 'New Description')
        
    def test_delete_task(self):
        self.task_manager.create_task('Task 1', 'Description 1')
        self.task_manager.delete_task('Task 1')
        self.assertEqual(len(self.task_manager.tasks), 0)
        
    def test_list_tasks(self):
        self.task_manager.create_task('Task 1', 'Description 1')
        self.task_manager.create_task('Task 2', 'Description 2')
        self.task_manager.list_tasks()
        # Can't easily test the print output, so just check that the method runs without errors
        
    def test_export_tasks(self):
        self.task_manager.create_task('Task 1', 'Description 1')
        self.task_manager.create_task('Task 2', 'Description 2')
        self.task_manager.export_tasks('test_export.csv')
        with open('test_export.csv') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].strip(), 'Title,Description')
        self.assertEqual(lines[1].strip(), 'Task 1,Description 1')
        self.assertEqual(lines[2].strip(), 'Task 2,Description 2')

    def tearDown(self):
        os.remove('test_tasks.csv')
        os.remove('test_export.csv')

    def test_delete_task(self):
        self.task_manager.create_task('Task 1', 'Description 1')
        self.assertIn('Task 1', [task.title for task in self.task_manager.tasks])
        self.task_manager.delete_task('Task 1')
        self.assertNotIn('Task 1', [task.title for task in self.task_manager.tasks])

    def test_list_tasks(self):
        self.task_manager.create_task('Task 1', 'Description 1')
        self.task_manager.create_task('Task 2', 'Description 2')
        with mock.patch('builtins.print') as mocked_print:
            self.task_manager.list_tasks()
            mocked_print.assert_any_call('Title: Task 1, Description: Description 1')
            mocked_print.assert_any_call('Title: Task 2, Description: Description 2')

    class TestTaskManager(unittest.TestCase):
        @patch('builtins.open', new_callable=mock_open)
        def test_create_task(self, mock_open):
            task_manager = TaskManager("tasks.csv")
            task_manager.create_task("Test Task", "This is a test task.")
            self.assertEqual(len(task_manager.tasks), 1)
            self.assertEqual(task_manager.tasks[0].title, "Test Task")
            self.assertEqual(task_manager.tasks[0].description, "This is a test task.")


if __name__ == '__main__':
    unittest.main() 