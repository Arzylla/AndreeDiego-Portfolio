from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy  # Mayúscula correcta
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user  # Nombres corregidos
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os  # Añadido para usar os.urandom

app = Flask(__name__)  # "Flask" con mayúscula
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'  # "URI" en lugar de "URL"
db = SQLAlchemy(app)
login_manager = LoginManager(app)  # "LoginManager" corregido
login_manager.login_view = 'login'

class User(UserMixin, db.Model):  # "UserMixin" corregido
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    project_url = db.Column(db.String(200))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html', name="Andree Emiliano Diego Romano")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/portfolio')
def portfolio():
    projects = Project.query.all()
    return render_template('portfolio.html', projects=projects)

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin():
    projects = Project.query.all()
    return render_template('admin.html', projects=projects)

@app.route('/add_project', methods=['POST'])
@login_required
def add_project():
    title = request.form.get('title')
    description = request.form.get('description')
    image_url = request.form.get('image_url')
    project_url = request.form.get('project_url')
    
    project = Project(
        title=title,
        description=description,
        image_url=image_url,
        project_url=project_url
    )
    db.session.add(project)
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
