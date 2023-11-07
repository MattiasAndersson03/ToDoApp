# http://localhost:5000/
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

# Läser av task från json filen
def read_tasks():
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    return tasks

# Sparar nya task till json filen
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
            'completed': False,
            'category': data['category']
        }
        tasks.append(new_task)
        save_tasks(tasks)

    tasks = read_tasks()
    return render_template('tasks.html', tasks=tasks)

# Vägen för att markera en task som klar
@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            save_tasks(tasks)
            break
    return redirect(url_for('tasks'))

# Vägen för att plocka bort en task
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)  # Tar bort en task från listan
            save_tasks(tasks)   # spar listan efter en task är bort plockad
            break
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(debug=True)