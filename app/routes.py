from flask import render_template, redirect, url_for, flash, request
from . import app, db
from .models import User, Post, Follower
from .forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash



@app.route('/')
def index():
    posts = Post.query.all()  # O cualquier lógica para obtener los posts
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Lógica para verificar las credenciales y iniciar sesión
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Lógica para registrar al usuario
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.created_at.desc()).all()
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # Añadir lógica de actualización del perfil del usuario
        return redirect(url_for('user', username=current_user.username))
    return render_template('edit_profile.html', form=form)

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        # Lógica para crear un nuevo post
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    # Añadir lógica para seguir a un usuario
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    # Añadir lógica para dejar de seguir a un usuario
    return redirect(url_for('user', username=username))
