from flask import render_template, redirect, url_for, flash, request
from flask import current_app as app
from app import db
from .models import User, Post, Follower
from .forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .minio_utils import upload_file_to_minio  


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Alguno de los campos introducidos no son correctos')
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/dashboard')
@login_required
def dashboard():
    posts = Post.query.order_by(Post.created_at.desc()).all()  # Obtiene todos los posts ordenados
    return render_template('dashboard.html', posts=posts)

@app.route('/dashboard/admin_panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('No tienes permiso para acceder a esta página', 'error')
        return redirect(url_for('dashboard'))

    users = User.query.all()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user_to_delete = User.query.get(user_id)
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('Usuario eliminado con éxito', 'success')
        else:
            flash('Usuario no encontrado', 'error')

    return render_template('admin_panel.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if user:
            flash('Username or email already exists. Please choose a different one.')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred. Username or email might already be taken.')
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
        current_username = current_user.username
        new_username = form.username.data
        new_email = form.email.data

        # Comprueba si el nuevo nombre de usuario ya existe
        existing_user = User.query.filter((User.username == new_username) & (User.username != current_username)).first()
        if existing_user:
            flash('El nombre de usuario ya está en uso. Por favor, elige otro.', 'error')
            return redirect(url_for('edit_profile'))

        # Actualiza los datos del usuario
        try:
            current_user.username = new_username
            current_user.email = new_email
            db.session.commit()
            flash('Tu perfil ha sido actualizado con éxito.', 'success')
        except Exception as e:
            flash('Ocurrió un error al actualizar tu perfil.', 'error')
            db.session.rollback()

    return render_template('edit_profile.html', form=form)



@app.route('/create_post', methods=['POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        content = form.content.data
        image_file = request.files['image']
        if image_file:
            # Asegúrate de que el nombre del archivo sea seguro
            filename = secure_filename(image_file.filename)
            # Sube el archivo a MinIO y obtén la URL de la imagen
            image_url = upload_file_to_minio(image_file, filename)
            
            # Crea el post con la URL de la imagen
            post = Post(content=content, image_url=image_url, author=current_user)
        else:
            # Crea el post sin imagen
            post = Post(content=content, author=current_user)
        
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
    else:
        flash('Please correct the form errors.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/follow/<username>')
@login_required
def follow(username):
    # Implementar lógica de seguir a un usuario aquí
    flash('You are now following {}!'.format(username))
    return redirect(url_for('user', username=username))      # IMPLEMENTAR LOGICAS PARA FOLLOW Y UNFOLLOW

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    # Implementar lógica de dejar de seguir a un usuario aquí
    flash('You have stopped following {}.'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/hello')
def hello():
    return '<h1>Hello, World!</h1>'


