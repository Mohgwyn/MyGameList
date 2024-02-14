import os

from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Resource, Api

from db import DataBase
from db.mongo import MongoDataBase
import auth


app = Flask(__name__, static_url_path='/static')
api = Api(app)

connection_string = os.getenv('CRUD_APP_CONNECTION_STRING')
if connection_string is None:
    print("Provide the MongoDB Connection String via the environment variable CRUD_APP_CONNECTION_STRING")
    exit(-1)
db: DataBase = MongoDataBase(connection_string)


class UserResource(Resource):
    def get(self, user):
        return db.user_exists(user=user)
    
api.add_resource(UserResource, '/api/user/<string:user>')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        if auth.login(user, password, db):
            return redirect(url_for('profile', user=user))
        else:
            return render_template('login.html', message='Invalid credentials')
    else:
        return render_template('login.html')
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        if auth.signup(db, user, password):
            return redirect(url_for('login'))
        else:
            return render_template('signup.html', message='User already exists')
    else:
        return render_template('signup.html')
    


@app.route('/profile/<user>')
def profile(user):
    if auth.is_logged_in(db):
        user_doc = db.user_exists(user)
        return render_template('profile.html', user=user, games=user_doc['game_list'])

if __name__ == '__main__':
    app.run(debug=True)