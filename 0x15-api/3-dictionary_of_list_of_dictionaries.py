#!/usr/bin/python3
"""
Export data in the JSON format.

Requirements:
- Records all tasks from all employees.
- File name must be: todo_all_employees.json
"""
import json
import requests
from sys import argv


if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com"

    # Get the list of users
    users_response = requests.get(f"{url}/users")
    users = users_response.json()

    # Get the list of tasks for all users
    all_tasks = {}
    for user in users:
        user_id = user["id"]
        username = user["username"]
        tasks_response = requests.get(f"{url}/todos?userId={user_id}")
        tasks = tasks_response.json()
        user_tasks = [{"username": username, "task": task["title"],
                      "completed": task["completed"]} for task in tasks]
        all_tasks[user_id] = user_tasks

    # Write the data to the JSON file
    with open("todo_all_employees.json", mode="w") as file:
        json.dump(all_tasks, file)
