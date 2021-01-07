from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '8bc2a72f05f2962d50de8b63a6f3c158'

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

@app.route('/account')
def account():
    return render_template('account.html', title='Account')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Welcome {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == '1234':
            flash('Welcome to your account', 'success')
            return redirect(url_for('home'))
        else:
            flash('Oops, check the fields', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(port=8000, debug=True)