from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO
from datetime import datetime
import pandas as pd
import numpy as np

app = Flask(__name__)

# =========================
# CONFIGURATION
# =========================

app.config['SECRET_KEY'] = 'secret123'

# CHANGE PASSWORD IF YOUR POSTGRES PASSWORD IS DIFFERENT
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1485@localhost/taskdb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# =========================
# DATABASE MODELS
# =========================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(500))
    priority = db.Column(db.String(50))
    status = db.Column(db.String(50))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# =========================
# LOGIN MANAGER
# =========================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =========================
# REGISTER
# =========================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "User already exists"

        new_user = User(username=username, password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

# =========================
# LOGIN
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)
            return redirect(url_for('dashboard'))

        return "Invalid username or password"

    return render_template('login.html')

# =========================
# LOGOUT
# =========================

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# =========================
# DASHBOARD
# =========================

@app.route('/')
@login_required
def dashboard():

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    # =========================
    # PANDAS + NUMPY ANALYTICS
    # =========================

    task_list = []

    for task in tasks:
        task_list.append({
            'title': task.title,
            'status': task.status
        })

    df = pd.DataFrame(task_list)

    total_tasks = len(df)

    completed_tasks = 0
    pending_tasks = 0
    completion_percentage = 0

    if total_tasks > 0:

        completed_tasks = np.sum(df['status'] == 'Completed')

        pending_tasks = np.sum(df['status'] == 'Pending')

        completion_percentage = (completed_tasks / total_tasks) * 100

    return render_template(
        'index.html',
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        completion_percentage=round(completion_percentage, 2)
    )

# =========================
# ADD TASK API
# =========================

@app.route('/add_task', methods=['POST'])
@login_required
def add_task():

    title = request.form['title']
    description = request.form['description']
    priority = request.form['priority']
    status = request.form['status']

    new_task = Task(
        title=title,
        description=description,
        priority=priority,
        status=status,
        user_id=current_user.id
    )

    db.session.add(new_task)
    db.session.commit()

    # WebSocket Notification
    socketio.emit('task_update', {'message': 'New Task Added'})

    return redirect(url_for('dashboard'))

# =========================
# UPDATE TASK API
# =========================

@app.route('/update_task/<int:id>', methods=['POST'])
@login_required
def update_task(id):

    task = Task.query.get(id)

    task.title = request.form['title']
    task.description = request.form['description']
    task.priority = request.form['priority']
    task.status = request.form['status']

    db.session.commit()

    socketio.emit('task_update', {'message': 'Task Updated'})

    return redirect(url_for('dashboard'))

# =========================
# DELETE TASK API
# =========================

@app.route('/delete_task/<int:id>')
@login_required
def delete_task(id):

    task = Task.query.get(id)

    db.session.delete(task)
    db.session.commit()

    socketio.emit('task_update', {'message': 'Task Deleted'})

    return redirect(url_for('dashboard'))

# =========================
# GET ALL TASKS API
# =========================

@app.route('/tasks')
@login_required
def get_tasks():

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    task_data = []

    for task in tasks:
        task_data.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'created_date': task.created_date
        })

    return jsonify(task_data)

# =========================
# RUN APP
# =========================

if __name__ == '__main__':
    socketio.run(app, debug=True)   