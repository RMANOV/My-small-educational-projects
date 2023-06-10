# Task management app
# Every professional has a lot of responsibilities and tasks to complete during the day. 
# Your app solves this problem by providing an easy way to organize tasks. 
# Each task has a title and description. 
# The user can list all unfinished tasks, create new, edit or delete an existing task. 
# Once deleted the task is considered done and is not visible any more. 
# The user can export the tasks in a file.
# Here is what you need to know:
# App requirements:
# You can use a platform and object-oriented programming (OOP) language of your preference.
# Python is choosen for this task.
# You have the freedom to choose the user interface, such as a web application, desktop app or console application.
# For this task a console application is choosen.
# The program should persist data upon restart.
# The export file format is of your choice.
# For this task a text file is choosen.
# You are required to write your own unit tests to ensure the functionality of your program.

# Check list for the task management app:
# 1. Check if the csv file is existing - if not create it
# 2. Check if the csv file is empty - if yes create the header
# 3. Check if the csv file is empty - if not read the file and create a list of tasks
# 4. Check if the user input is valid - if not ask for a valid input
# 5. Check if the user input is valid - if yes create a new task
# 6. Check if the user input is valid - if yes edit an existing task
# 7. Check if the user input is valid - if yes delete an existing task
# 8. Check if the user input is valid - if yes list all unfinished tasks
# 9. Check if the user input is valid - if yes export the tasks in a file
# 10. Check if the user input is valid - if yes exit the program


import csv
import os

class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description


class TaskManager:
    def __init__(self, filename):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Description"])
        else:
            with open(self.filename, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    self.tasks.append(Task(row[0], row[1]))

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "Description"])
            for task in self.tasks:
                writer.writerow([task.title, task.description])

    def create_task(self, title, description):
        self.tasks.append(Task(title, description))
        self.save_tasks()

    def edit_task(self, title, new_title, new_description):
        for task in self.tasks:
            if task.title == title:
                task.title = new_title
                task.description = new_description
                self.save_tasks()
                break

    def delete_task(self, title):
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                self.save_tasks()
                break

    def list_tasks(self):
        for task in self.tasks:
            print(f"Title: {task.title}, Description: {task.description}")

    def export_tasks(self, export_filename):
        with open(export_filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "Description"])
            for task in self.tasks:
                writer.writerow([task.title, task.description])


def main():
    task_manager = TaskManager("tasks.csv")

    while True:
        print("\n1. Create task")
        print("2. Edit task")
        print("3. Delete task")
        print("4. List tasks")
        print("5. Export tasks")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Enter title: ")
            description = input("Enter description: ")
            task_manager.create_task(title, description)
        elif choice == "2":
            title = input("Enter the title of the task to edit: ")
            new_title = input("Enter new title: ")
            new_description = input("Enter new description: ")
            task_manager.edit_task(title, new_title, new_description)
        elif choice == "3":
            title = input("Enter the title of the task to delete: ")
            task_manager.delete_task(title)
        elif choice =="4":
            task_manager.list_tasks()
        elif choice == "5":
            export_filename = input("Enter the name of the file to export to: ")
            task_manager.export_tasks(export_filename)
        elif choice == "6":
            break
        else:
            print("Invalid choice, please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
