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

def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
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
        # Lógica para actualizar el perfil del usuario
        return redirect(url_for('user', username=current_user.username))
    return render_template('edit_profile.html', form=form)

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!')
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    # Implementar la lógica de seguir a un usuario
    flash('You are now following {}!'.format(username))
    return redirect(url_for('user_profile', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    # Implementar la lógica de dejar de seguir a un usuario
    flash('You have stopped following {}.'.format(username))
    return redirect(url_for('user_profile', username=username))

