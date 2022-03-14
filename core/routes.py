import time
from flask_restful import Resource, reqparse, abort
from core.models import ShortUrls
from core import app, db, api
from random import choice
import string
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange
from flask import render_template, request, flash, redirect, url_for


"""-----------------------APP FUNCTIONAL------------------------------------"""

class UrlForm(FlaskForm):
    """Entity to WTF-FORM"""
    url = StringField('url', validators=[InputRequired(message='The URL is required!')])
    custom_id = StringField('custom_id')
    time_life = IntegerField('time_life', validators=[NumberRange(min=1, max=360, message='Minimum input value 1, maximum input value 360'), InputRequired(message='The Number is required!')])

def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters if custom_id is empty"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))

@app.route('/', methods=['GET', 'POST'])
def index():
    """Function get data at form UrlForm add save in models ShortUrls"""
    form = UrlForm(request.form)
    if form.validate_on_submit():
        if request.method == 'POST':

            """Entity what field in form needs"""
            url_form = request.form['url']
            custom_id_form = request.form['custom_id']
            time_life_form = request.form['time_life']

            """Validation"""
            if custom_id_form and ShortUrls.query.filter_by(short_id=custom_id_form).first() is not None:
                flash('Please enter different custom id!')
                return redirect(url_for('index'))

            if not custom_id_form:
                custom_id_form = generate_short_id(3)

            if not time_life_form:
                time_life_form = 90

            """Calculations expiry date"""
            days = time.time() + (int(time_life_form) * 24 * 60 * 60)

            """Save data in models ShortUrls"""
            new_link = ShortUrls(original_url=url_form, short_id=custom_id_form, time_life=time_life_form, created_at=time.time(), expiration_at=days)
            try:
                db.session.add(new_link)
                db.session.commit()
                return redirect('/')
            except:
                return "ERROR: Something wrong can't save data"

    """Get all Urls in model ShortUrls and render templates"""
    short_urls = ShortUrls.query.all()
    return render_template('index.html', form=form, short_id=short_urls)

@app.route('/<short_id>')
def redirect_url(short_id):
    """Function redirecting user to original link"""
    link = ShortUrls.query.filter_by(short_id=short_id).first()

    """Validation"""
    if link:
        if link.expiration_at <= time.time():
            """When the link lifetime is less than or equal to the current time, the link is removed"""
            flash('The life-time URL has expired, the URL will be removed')
            db.session.delete(link)
            db.session.commit()
            return redirect('/')
        else:
            return redirect(link.original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))


"""-----------------------API FUNCTION------------------------------------"""

"""Creating entity Arguments"""
urlpost_args = reqparse.RequestParser()
urlpost_args.add_argument("original_url", type=str, help="The URL is required!", required=True)
urlpost_args.add_argument("short_id", type=str, help="The ID is required!", required=True)
urlpost_args.add_argument("time_life", type=int, help="The Time Life is required!", required=True)

"""Api Get to Endpoint /list_urls"""
class URL_list(Resource):
    def get(self):
        urls = ShortUrls.query.all()
        data = {}
        for url in urls:
            data[url.id] = {"original_url": url.original_url, "short_id": "http://127.0.0.1:5000/" + url.short_id, url.time_life: "time_life"}
        return data

"""Api Post to Endpoint /create_urls"""
class URL_create(Resource):
    def post(self):
        """Entity api arguments"""
        args = urlpost_args.parse_args()
        url_api = args['original_url']
        short_id_api = args['short_id']
        time_life_api = args['time_life']

        """Validation"""
        if short_id_api and ShortUrls.query.filter_by(short_id=short_id_api).first() is not None:
            abort(409, message='Please enter different custom id!')

        if not url_api:
            abort(409, message='The URL is required!')

        if not time_life_api:
            time_life_api = 90

        if not short_id_api:
            short_id_api = generate_short_id(3)

        """Calculations expiry date"""
        days = time.time() + (int(time_life_api) * 24 * 60 * 60)

        """Save data in models ShortUrls"""
        new_link = ShortUrls(original_url=url_api, short_id=short_id_api, time_life=time_life_api, created_at=time.time(), expiration_at=days)
        try:
            db.session.add(new_link)
            db.session.commit()
            short_url = request.host_url + short_id_api
            return short_url
        except:
            return "ERROR: Something wrong can't save data"

""" Endpoints """
api.add_resource(URL_create, '/create_urls')
api.add_resource(URL_list, '/list_urls')
