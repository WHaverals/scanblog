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
    return render_template('index_2.html', title='Home')


@app.route('/task_description')
@login_required
def task_description():
    return render_template('task_description.html')

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


@app.route('/save_annotation', methods=['POST'])
@login_required
def save_annotation():
    data = flask.request.json
    story_id = data['story_id']
    annotations = data['annotations']
    annotation = Annotation(
        user_id=int(current_user.id), story_id=int(story_id), annotation=annotations)
    db.session.add(annotation)
    db.session.commit()
    return flask.jsonify(status="OK")



@app.route('/scansion', methods=['GET', 'POST'])
@login_required
def scansion():
    user_id = int(current_user.id)
    fragments_done = Annotation.query.filter_by(done=1, user_id=user_id).all()
    if len(fragments_done) < 3000:
        with open("app/static/js/test.json") as f:
            data = json.load(f)
            story_ids = [story["story_id"] for story in data["stories"]]
            done = [fragment.story_id for fragment in fragments_done]
            story_ids = [id for id in story_ids if id not in done]
            if not story_ids:
                return render_template('index.html')
            story_id = random.sample(story_ids, 1)[0]
            story = next(story for story in data["stories"] if story["story_id"] == story_id)
            annotations = {syllable["id"]: {'syllable': syllable["text"], 'stressed': False}
                           for line in story["fragments"][0]["lines"] 
                           for word in line for syllable in word}
            return render_template('scansion.html', story_id=story_id, annotations=annotations, title=story["title"], lines=story["fragments"][0]["lines"])
    else:
        return redirect(url_for('index'))


# Route for finalizing and submitting annotation of verse lines
@app.route('/finalize_annotation', methods=['GET', 'POST'])
@login_required
def finalize_annotation():
    user_id = int(current_user.id)
    data = flask.request.json
    story_id = data['story_id']
    annotations = data['annotations']
    annotation = Annotation(
        user_id=int(current_user.id), story_id=int(story_id), annotation=annotations, done=1)
    db.session.add(annotation)
    db.session.commit()
    return flask.jsonify(status="OK")