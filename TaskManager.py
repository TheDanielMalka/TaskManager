import data_models as dm
import json

class TaskManager:

    """ Main task management class.
       Handles task list operations: add, remove, edit, mark, save, load """

    def __init__(self):
        self.tasks:list = []

    def open_message(self) -> None:

        """" Displays main menu with available commands. """

        print("🚀 Welcome to DOCKERIZED TaskManager! 🐳\n"
              "our commands :\n"
              "<show> to show your current tasks\n"
              "<add> to add a task to the calender\n"
              "<remove> to remove a task [goes by task number]\n"
              "<edit> to edit a task name\n"
              "<mark> to mark the task as done\n"
              "<clear> to clear your done tasks\n"
              "<save> to save your task on the calendar\n"
              "<menu> to go back to the menu\n"
              "<exit> to quit")

    def show_tasks(self) -> None:

        """This function displays all tasks with their details: name, priority, category, created date"""

        if len(self.tasks) == 0:
            print("No Tasks on the calendar")
        else:
            for i, task in enumerate(self.tasks, 1):
                print(f"{i}. {task.task_name} | Priority: {task.priority} | Category: {task.category} | Created: {task.created_at}")

    def sort_tasks(self) -> None:

        """Sorts tasks by priority first, and then by created date"""

        self.tasks.sort(key=lambda task: (task.priority, task.created_at), reverse=True)
        print("Tasks sorted by Priority and then by Date.")

    def add_task(self, task:object) -> None:

        """Adds new task to list.
        Checks for duplicates and asks user confirmation if exists"""

        existing_list = []
        for t in self.tasks:
            existing_list.append(t.task_name)
        if task.task_name in existing_list:
                print("You already have that task in your tasks")
                inp = input("Wanna add it again? press 'y' to add again: ")
                if inp.lower() == "y":
                    self.tasks.append(task)
        else:
            self.tasks.append(task)

    def edit_task(self, num: int, new_name: str) -> None:

        """ Changes task name by task number """

        if 1 <= num <= len(self.tasks):
            old_name = self.tasks[num - 1].task_name
            self.tasks[num - 1].task_name = new_name
            print(f"Task {num} changed from '{old_name}' to '{new_name}'")
        else:
            print("Invalid task number. Edit failed.")

    def remove_task(self, num:int) -> None:

        """Removes task from list by task number """

        if not self.tasks:
            print("Your Task List is empty")

        elif 1 <= num <= len(self.tasks):
            removed = self.tasks.pop(num - 1)
            print(f"Task '{removed.task_name}' has been removed")

        else:
            print("Invalid task number")

    def mark_done(self, num:int) -> None:

        """ Marks task as done by adding checkmark to task name ✅ """

        while True:
            if 1 <= num <= len(self.tasks):
                temp = self.tasks[num-1]
                if "✅" not in temp.task_name:
                    print(f"Task: ({temp.task_name}) has been marked")
                    temp.task_name += "✅"
                    break
            else:
                print("Invalid Task Number Try Again")
            again = input("You entered invalid task number you wanna try again? ( y / n )")
            if again.lower() == "y":
                num = int(input("Enter task num"))
            else:
                break

    def clear_done_tasks(self) -> None:

        """ Removes all marked tasks from the list"""

        new_tasks = []
        for task in self.tasks:
            if "✅" not in task.task_name:
                new_tasks.append(task)
        self.tasks = new_tasks

    def save_to_file(self, file_path):

        """Saves all tasks to json file.
        Format:  "task_name": task.task_name,
                    "priority": task.priority,
                    "category": task.category,
                    "created_at": task.created_at """

        tasks_data = []
        for task in self.tasks:
            task_dict = {
                "task_name": task.task_name,
                "priority": task.priority,
                "category": task.category,
                "created_at": task.created_at
            }
            tasks_data.append(task_dict)
        with open(file_path, 'w', encoding='utf-8') as st:
            json.dump(tasks_data, st, indent=4, ensure_ascii=False)
        print(f"Data written to {file_path} successfully.")

    def load_from_file(self, file_path):

        """Loads tasks from json file into task list.
                Skips duplicates."""

        try:
            with open(file_path, 'r', encoding='utf-8') as rt:
                tasks_data = json.load(rt)
            for task in tasks_data:
                task_name = task["task_name"]
                priority = task["priority"]
                category = task["category"]
                time = task["created_at"]
                new_task_obj = dm.TaskAttributes(task_name, priority, category, time)
                exists = False
                for existing_task in self.tasks:
                    if existing_task.task_name == task_name:
                        exists = True
                        break
                if not exists:
                    self.tasks.append(new_task_obj)
        except FileNotFoundError:
            print("Your calendar is empty")

TaskManagerBank = TaskManager()
TaskManagerBank.load_from_file("./TaskManager.json")
TaskManagerBank.open_message()
user_input = input("Enter your choice \n").strip().lower()

if __name__ == "__main__":
    while user_input != "exit":
        if user_input == "menu":
            TaskManagerBank.open_message()
        elif user_input == "show":
            TaskManagerBank.sort_tasks()
            TaskManagerBank.show_tasks()
        elif user_input == "add":
            new_task = input("Enter your new task name \n").strip()
            task_obj = dm.build_task(new_task)
            TaskManagerBank.add_task(task_obj)
            print(f"Task: '{task_obj.task_name}' Added! [Priority: {task_obj.priority}, Category: {task_obj.category}]")
        elif user_input == "edit":
            print(f"Heres your tasks :\n")
            TaskManagerBank.show_tasks()
            try:
                task_num = int(input("Enter task number to edit: "))
                if 1 <= task_num <= len(TaskManagerBank.tasks):
                    new_name = input("Enter the new name for the task: ")
                    TaskManagerBank.edit_task(task_num, new_name)
                else:
                    print("Invalid task number")
            except ValueError:
                print("You must enter a valid number")

        elif user_input == "mark":
            print(f"Heres your tasks :\n")
            TaskManagerBank.show_tasks()
            try:
                mark_the_task = int(input(f"Enter task number to be marked \n"))
                TaskManagerBank.mark_done(mark_the_task)
            except ValueError:
                print("You must enter a valid number")

        elif user_input == "remove":
            print(f"Heres your tasks :\n")
            TaskManagerBank.show_tasks()
            try:
                remove_the_task = int(input(f"Enter task number to be removed \n"))
                TaskManagerBank.remove_task(remove_the_task)
            except ValueError:
                print("You must enter a valid number")

        elif user_input == "clear":
            TaskManagerBank.clear_done_tasks()
            print("Done tasks have been cleared.")

        elif user_input == "save":
            TaskManagerBank.sort_tasks()
            TaskManagerBank.save_to_file('./TaskManager.json')

        user_input = input("Enter your choice \n").strip().lower()
print("GoodBye")
