import random

import flask
from flask import Flask, render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import app, db, login
from app.forms import LoginForm, RegistrationForm
from app.models import User, Annotation, JSONEncodedDict

import json
from sqlalchemy.types import TypeDecorator, VARCHAR


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


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
    return render_template('login.html', title='Sign In', form=form)


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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

## UNDER CONSTRUCTION ###

        # if flask.request.method == 'POST':
        #     story_id.done = 1
        #     db.session.commit()


# @app.route('/save_annotation', methods=['GET', 'POST'])
# def save_annotation():
#     json = flask.request.json
#     print(json)
#     return

@app.route('/scansion', methods=['GET', 'POST'])
@login_required
def scansion():
    user_id = int(current_user.id)
    fragments_done = Annotation.query.filter_by(done=1, user_id=user_id).all()
    if len(fragments_done) == 2:
        return render_template('scansion.html')
    elif (fragments_done) < 2:
        with open("app/static/js/test.json") as f:
            data = json.load(f)
            story_ids = [story["story_id"] for story in data["stories"]]
            done = [fragment.story_id for fragment in fragments_done]
            story_ids = [id for id in story_ids if id not in done]
            story_id = random.sample(story_ids, 1)
            story = next(story for story in data if story["story_id"] == story_id)
            return render_template('scansion.html', title=story["title"], lines=story["lines"])
    
    # title = data["stories"][0]["title"]
    # lines = data["stories"][0]["fragments"][0]["lines"]
    # return render_template('scansion.html', title=title, lines=lines)