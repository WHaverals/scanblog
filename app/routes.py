import random

import flask
from flask import Flask, render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import app, db, login
from app.forms import LoginForm, RegistrationForm
from app.models import User, Annotation, Fragment, Syllable

import json
from sqlalchemy.types import TypeDecorator, VARCHAR
import logging

logging.basicConfig(filename='/var/log/scanblog.log',level=logging.DEBUG)
logger = logging.getLogger()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


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
    #if current_user.is_authenticated:
    #    return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, \
        language=form.language.data, middledutch=form.middledutch.data)
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
    logger.info('saving annotation with data %s', data)
    syl_id = data['syl_id']
    stressed = data['stressed']
    annotation = Annotation(user_id=int(current_user.id), \
    syllable_id=int(syl_id), stressed=stressed)
    db.session.add(annotation)
    db.session.commit()
    return flask.jsonify(status="OK")


@app.route('/scansion', methods=['GET', 'POST'])
@login_required
def scansion():
    logger.info('entering scansion')
    user_id = int(current_user.id)
    frag_ids_done = Annotation.get_fragments_done(user_id)
    logger.info("fragments done %s ", frag_ids_done)
    frag_ids = Fragment.get_all_ids()
    logger.info("all fragments %s", frag_ids)
    if len(frag_ids_done) < len(frag_ids):            
            frag_ids_n_done = [id for id in frag_ids if id not in frag_ids_done]
            if not frag_ids_n_done:
                return render_template('index.html')
            frag_id = random.sample(frag_ids_n_done, 1)[0]
            logger.info("frag_id choosen bij random %s", frag_id)
            title = Fragment.get_story_description(frag_id)
            logger.info("descr %s", title)
            lines = Syllable.convert_to_list(frag_id)
            #logger.info("lines %s", lines)
            return render_template('scansion.html', frag_id=frag_id, title=title, lines=lines)
    else:
        return redirect(url_for('index'))


# Route for finalizing and submitting annotation of verse lines
@app.route('/finalize_annotation', methods=['GET', 'POST'])
@login_required
def finalize_annotation():
	user_id = int(current_user.id)
	data = flask.request.json
	logger.info('finalizing annotation with data %s', data)
	for el in data:
		syl_id = el['syl_id']
		annotation = Annotation(user_id=int(current_user.id), \
		syllable_id=int(syl_id), stressed=True, fragment_done = True)
		db.session.add(annotation)
	db.session.commit()
	return flask.jsonify(status="OK")
