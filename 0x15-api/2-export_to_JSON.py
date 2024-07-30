#!/usr/bin/python3
"""
This Python script extends the previous task to export the employee's TODO
list progress and completed tasks to a JSON file named after the employee's ID.
"""
import json
import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]))
        sys.exit(1)

    employee_id = sys.argv[1]
    base_url = "https://jsonplaceholder.typicode.com"
    user_url = "{}/users/{}".format(base_url, employee_id)
    todo_url = "{}/todos?userId={}".format(base_url, employee_id)

    try:
        user_response = requests.get(user_url)
        user_response.raise_for_status()
        user_data = user_response.json()
        employee_name = user_data.get("username")

        todo_response = requests.get(todo_url)
        todo_response.raise_for_status()
        todo_data = todo_response.json()

        json_data = {employee_id: []}
        for task in todo_data:
            task_title = task.get("title")
            task_status = task.get("completed")
            json_data[employee_id].append({"task": task_title,
                                           "completed": task_status,
                                           "username": employee_name})

        json_file = "{}.json".format(employee_id)
        with open(json_file, mode='w') as file:
            json.dump(json_data, file)
        print("Data exported to {} successfully.".format(json_file))
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        sys.exit(1)
