#!/usr/bin/python3
"""
This Python script extends the previous task to export the employee's TODO list
progress and completed tasks to a CSV file named after the employee's ID.
The script takes the employee ID as a command-line argument and
generates a CSV file with the required information.
"""
import csv
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

        csv_file = "{}.csv".format(employee_id)
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            for task in todo_data:
                task_id = task.get("id")
                task_title = task.get("title")
                task_status = task.get("completed")
                writer.writerow([employee_id, employee_name,
                                task_status, task_title])
        print("Data exported to {} successfully.".format(csv_file))
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        sys.exit(1)
