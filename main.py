# http://localhost:5000/
from flask import Flask, request, jsonify, render_template, redirect
import json

app = Flask(__name__, template_folder='templates')

@app.errorhandler(404) # Fångar upp man skriver en endpoint som inte finns
def not_found(error):
    return jsonify({"message": "Ej giltig endpoint"}), 404

@app.route('/tasks/html', methods=['GET']) # Plockar fram templaten
def tasks_html():
    tasks = read_tasks()
    return render_template('tasks.html', tasks=tasks)

@app.route('/', methods=['GET', 'POST']) # Fångar upp task som skapa på sidan och skicka till save task
def tasks_page():
    if request.method == 'POST':
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
        return jsonify(new_task)

    tasks = read_tasks()
    return render_template('tasks.html', tasks=tasks)

def read_tasks(): # Används för att läsa uppgifterna från json filen
    try:

        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    return tasks
def save_tasks(tasks): # Sparar task till json filen
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

@app.route('/tasks', methods=['GET', 'POST']) # plockar fram även lägar till nya task
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
            'completed': False,
            'category': data['category']
        }
        tasks.append(new_task)
        save_tasks(tasks)
        return redirect('/tasks/html')

    tasks = read_tasks()
    return jsonify(tasks)

@app.route('/tasks/completed', methods=['GET']) # ploackar fram completed tasks
def completed_tasks():
    tasks = read_tasks()
    completed_tasks = [task for task in tasks if task['completed'] is True]

    if not completed_tasks:
        return "No completed tasks found"
    return jsonify(completed_tasks)

@app.route('/tasks/incomplete', methods=['GET']) # plockar from de incompleted tasks
def incomplete_tasks():
    tasks = read_tasks()
    incomplete_tasks = [task for task in tasks if task['completed'] is False]

    if not incomplete_tasks:
        return "No incompleted tasks found", 404
    return jsonify(incomplete_tasks)

@app.route('/tasks/<int:task_id>', methods=['PUT']) # Ändrar en task med specifikt id
def update_task(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            data = {
                'title': request.form['title'],
                'category': request.form['category']
            }
            task['title'] = data['title']
            task['category'] = data['category']
            save_tasks(tasks)
            return jsonify(task)
    return "Task not found", 404

@app.route('/tasks/<int:task_id>/complete', methods=['PUT']) # Ändra en task till completed true
def complete_task(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            save_tasks(tasks)
            return "Task marked as completed", 200
    return "Task not found", 404

@app.route('/tasks/<int:task_id>', methods=['DELETE']) # PLockar bort tasks
def delete_task(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            return jsonify({"message": "Task deleted"})
    return "Task not found", 404

@app.route('/tasks/<int:task_id>', methods=['GET']) #Hämtar en task med ett specifikt id
def get_task(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            return jsonify(task)
    return "Task not found", 404

@app.route('/tasks/categories', methods=['GET']) # Hämtar alla olika kategorier
def get_unique_categories():
    tasks = read_tasks()
    unique_categories = set(task['category'] for task in tasks)
    return jsonify(list(unique_categories))

@app.route('/tasks/categories/<string:category_name>', methods=['GET']) # Hämtar task från en specifik kategori
def get_tasks_by_category(category_name):
    tasks = read_tasks()
    tasks_in_category = [task for task in tasks if task['category'] == category_name]

    if not tasks_in_category:
        return "Category not found", 404
    return jsonify(tasks_in_category)

if __name__ == '__main__':
    app.run(debug=True)

