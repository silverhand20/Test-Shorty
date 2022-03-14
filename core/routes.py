from datetime import datetime
import time
from core.models import ShortUrls
from core import app, db, api
from random import choice
import string
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange
from flask import render_template, request, flash, redirect, url_for
from flask import Flask, jsonify, request

class UrlForm(FlaskForm):
    """Class for WTF-FORM"""
    url = StringField('url', validators=[InputRequired(message='The URL is required!')])
    custom_id = StringField('custom_id')
    temporary_url = IntegerField('live_time', validators=[NumberRange(min=1, max=360, message='The URL is required!'), InputRequired(message='The URL is required!')])

def generate_short_id(num_of_chars: int):
    """Function to generate random short_id  of specified number of characters"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))


@app.route('/', methods=['GET', 'POST'])
def index():
    """Function get data for form and generate short_id  """
    form = UrlForm(request.form)
    if form.validate_on_submit():
        if request.method == 'POST':
            url = request.form['url']
            short_id = request.form['custom_id']
            temporary_url = request.form['temporary_url']

            if short_id and ShortUrls.query.filter_by(short_id=short_id).first() is not None:
                flash('Please enter different custom id!')
                return redirect(url_for('index'))

            if not short_id:
                short_id = generate_short_id(8)

            if not temporary_url:
                temporary_url = 90

            """Element to calculated time-life """
            seconds = time.time() + (int(temporary_url) * 24 * 60 * 60)

            """Element to Save data to db """
            new_link = ShortUrls(
                original_url=url, short_id=short_id, temporary_url=temporary_url, created_at=time.time(), expiration_at=seconds)
            try:
                db.session.add(new_link)
                db.session.commit()
                return redirect('/')
            except:
                return "ERROR:"

    short_urls = ShortUrls.query.all()
    return render_template('index.html', form=form, short_id=short_urls)

@app.route('/<short_id>')
def redirect_url(short_id):
    """Function to redirected to origin url by short_id  """
    link = ShortUrls.query.filter_by(short_id=short_id).first()
    if link:
        """Element when time-life is expair delete this link """
        if link.expiration_at <= time.time():
            flash('Invalid URL expiration_at TIME data was deleted')
            db.session.delete(link)
            db.session.commit()
            return redirect('/')
        else:
            return redirect(link.original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))
