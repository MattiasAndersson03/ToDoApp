# http://localhost:5000/
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        data = {
            'title': request.form['title'],
            'category': request.form['category']
        }
        tasks = read_tasks()
        new_task = {
            'id': len(tasks) + 1,
            'title': data['title'],
            'completed': False,  # Set to False by default for new tasks
            'category': data['category']
        }
        tasks.append(new_task)
        save_tasks(tasks)

    tasks = read_tasks()
    return render_template('tasks.html', tasks=tasks)


@app.route('/tasks/<int:task_id>/complete', methods=['PUT']) #Gör så en task står som completed
def complete_task(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            save_tasks(tasks)
            break
    return redirect(url_for('tasks'))


@app.route('/tasks/<int:task_id>', methods=['DELETE']) # Tar bort en task
def delete_task(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            return "Task deleted", 204
    return "Task not found", 404

@app.route('/tasks/categories', methods=['GET'])
def get_unique_categories():
    tasks = read_tasks()
    unique_categories = set(task['category'] for task in tasks)
    return jsonify(list(unique_categories))

@app.route('/tasks/categories/<string:category_name>', methods=['GET']) #Hämtar task från en specifik kategori
def get_tasks_by_category(category_name):
    tasks = read_tasks()
    tasks_in_category = [task for task in tasks if task['category'] == category_name]
    return jsonify(tasks_in_category)

@app.route('/tasks', methods=['GET']) #Hämtar alla tasks
def get_all_tasks():
    tasks = read_tasks()
    return jsonify(tasks)
@app.route('/tasks/<int:task_id>', methods=['GET']) # Hämtar en task med specifikt id
def get_task(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            return jsonify(task)
    return "Uppgift ej hittad", 404

if __name__ == '__main__':
    app.run(debug=True)

# GET /tasks ✅
# POST /tasks
# GET /tasks/{task_id} ✅
# DELETE /tasks/{task_id} ✅
# PUT /tasks/{task_id}
# PUT /tasks/{task_id}/complete ✅
# GET /tasks/categories/ ✅
# GET /tasks/categories/{category_name} ✅