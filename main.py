# http://localhost:5000/
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

# Läs in data från tasks.json
def read_tasks():
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    return tasks

# Spara data till tasks.json
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

# Endpoint för att visa alla tasks och lägga till en ny task
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

if __name__ == '__main__':
    app.run(debug=True)