"""Main application and routing logic""" 

from decouple import config
from flask import Flask,render_template, request
from .models import DB, User,Tweet

def create_app():
    """Create and configure app"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = config('ENV')
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title ="Home",users= users) 


    @app.route('/user/<name>')
    def view_user(name):
        user = User.query.filter_by(name=name).first()
        uid = user.id
        tweets = Tweet.query.filter_by(user_id=uid).all()
        return render_template('user.html',title="Tweets", user = user,tweets=tweets)
   

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html',title='DB Reset', users =[])

    return app
