import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        "title": "I like to play RPG",
        "author": "Lucas Campelo",
        "date": "December 28th, 2020",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec dui feugiat, euismod sem sed, ullamcorper leo. Suspendisse massa elit, tincidunt id convallis quis, vehicula id quam. Proin ut dictum tellus, non ornare ex. In vulputate feugiat leo, sit amet blandit nunc consequat vitae. Nulla ut feugiat neque, in efficitur arcu. Aenean vel tincidunt tellus, eget euismod quam. In at interdum nisi. Duis nisi augue, sagittis et ultrices nec, convallis sit amet quam. Ut ac enim sapien. Nam et nibh in leo tincidunt tempus et sit amet dui. Morbi massa nibh, vehicula at dignissim vel, sagittis vel sapien. Phasellus nec quam lacinia, scelerisque augue tincidunt, malesuada magna. Ut feugiat lacus est, id iaculis urna rhoncus efficitur. Sed nibh felis, interdum id odio sit amet, fermentum porta ex. Cras dapibus lorem velit, aliquam consectetur velit commodo non."
    },
    {
        "title": "I'm working with AI",
        "author": "Jamille Peres",
        "date": "February 30th, 2021",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec dui feugiat, euismod sem sed, ullamcorper leo. Suspendisse massa elit, tincidunt id convallis quis, vehicula id quam. Proin ut dictum tellus, non ornare ex. In vulputate feugiat leo, sit amet blandit nunc consequat vitae. Nulla ut feugiat neque, in efficitur arcu. Aenean vel tincidunt tellus, eget euismod quam. In at interdum nisi. Duis nisi augue, sagittis et ultrices nec, convallis sit amet quam. Ut ac enim sapien. Nam et nibh in leo tincidunt tempus et sit amet dui. Morbi massa nibh, vehicula at dignissim vel, sagittis vel sapien. Phasellus nec quam lacinia, scelerisque augue tincidunt, malesuada magna. Ut feugiat lacus est, id iaculis urna rhoncus efficitur. Sed nibh felis, interdum id odio sit amet, fermentum porta ex. Cras dapibus lorem velit, aliquam consectetur velit commodo non."
    }
]

@app.route('/')
def home():
    return render_template('home.html', title='Home', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)        
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, you can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Oops, check the fields', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pictures', picture_fn)
    
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pictures/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)