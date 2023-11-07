# http://localhost:5000/
from flask import Flask, render_template, request, jsonify, abort
import json

def read_tasks():
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    return tasks

def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)
app = Flask(__name__)

# Existing functions for reading and saving tasks

# ...

# Add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = {
        'title': request.form['title'],
        'category': request.form['category']
    }
    tasks = read_tasks()
    new_task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'completed': False,
        'category': data['category']
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

# Get a specific task by its ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            return jsonify(task)
    abort(404)  # Task not found

# Delete a specific task by its ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            return '', 204  # No content
    abort(404)  # Task not found

# Update a specific task by its ID
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = data.get('title', task['title'])
            task['category'] = data.get('category', task['category'])
            save_tasks(tasks)
            return jsonify(task)
    abort(404)  # Task not found

# Mark a task as completed
@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def mark_task_as_completed(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            save_tasks(tasks)
            return jsonify(task)
    abort(404)  # Task not found

# Get all task categories
@app.route('/tasks/categories/', methods=['GET'])
def get_all_categories():
    tasks = read_tasks()
    categories = set(task['category'] for task in tasks)
    return jsonify(list(categories))

# Get tasks from a specific category
@app.route('/tasks/categories/<category_name>', methods=['GET'])
def get_tasks_by_category(category_name):
    tasks = read_tasks()
    filtered_tasks = [task for task in tasks if task['category'] == category_name]
    return jsonify(filtered_tasks)

if __name__ == '__main__':
    app.run(debug=True)