from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import RegistrationForm, LoginForm, PostForm
from app.models import User, Post
from flask_login import logout_user
from scrapy.crawler import CrawlerProcess

from flask_login import login_required

from .scrapy_weather import WeatherSpider, weather_today

process = CrawlerProcess()
process.crawl(WeatherSpider)
process.start()


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', date=weather_today)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    surname=form.surname.data,
                    email=form.email.data,
                    age=form.age.data,
                    gender=form.gender.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/comments',  methods=['GET', 'POST'])
@login_required
def comments():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = PostForm()
    if form.validate_on_submit():
        user = Post(username=form.username.data,
                    email=form.email.data,
                    comments=form.comments.data
                    )
        db.session.add(user)
        db.session.commit()
        flash('Your post is now live!')

        return redirect(url_for('comments'))
    posts = Post.query.all()
    return render_template('comments.html', form=form, posts=posts)
