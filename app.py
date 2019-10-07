from flask import Flask, render_template, request, redirect, url_for, jsonify, json
from pymongo import MongoClient
import requests
import json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
#from flask_jwt_extended import JWTManager
#from flask_jwt_extended import (create_access_token)
#from flask_bcrypt import Bcrypt
#from flask_cors import CORS
import os
#import jsonify

# host = os.environ.get('MONGODB_URI', 'mongodb://<heroku_h8zw53pl>:<bghbgh123->@ds229118.mlab.com:29118/heroku_h8zw53pl')
# mclient = MongoClient(host=f'{host}?retryWrites=false')
# db = client.get_default_database()

client = MongoClient()
db = client.DogWebsite  # was Poodle
doginfo = db.doginfo

app = Flask(__name__)

# app.config['MONGO_DBNAME'] = 'mernloginreg'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/mernloginreg'
# app.config['JWT_SECRET_KEY'] = 'secret'

# mongo = PyMongo(app)
# bcrypt = Bcrypt(app)
# jwt = JWTManager(app)

# @app.route('/')
# def index():
#    """Return homepage."""
#    return render_template('home.html', msg='Homepage')
# @app.route('/users/register', methods=["GET", "POST"])
# def register(methods=["GET", "POST"]):
#     users = mongo.db.users
#     test = users.find()
#     print(test)
#     # print(f'User: {users}')
#     # request.get_json(force=True)
#     email = request.get_json(force=True)['email']
#     print(f'Email is: {email}')
#     password = bcrypt.generate_password_hash(
#         request.get_json()['password'].decode('utf-8'))
#     print(f'Password is: {password}')

#     user_id = users.insert({
#         'email': email,
#         'password': password,
#     })

#     new_user = users.find_one({'_id': user_id})
#     result = {'email': new+user['email'] + ' registered'}
#     print(f"Result is: {result}")
#     return jsonify({'result': result})
#     # return render_template('register_login.html' password=password, email=email, result=result)


# @app.route('/users/login')
# def login(methods=["GET", "POST"]):
#     users = mongo.db.users
#     email = request.get_json()['email']
#     password = requests.get_json()['password']
#     result = ""

#     response = user.find_one({'email': email})

#     if response:
#         if bcrypt.check_password_hash(response['password'], password):
#             access_token = create_access_token(identity={
#                 'email': response['email']}
#             )
#             result = jsonify({"token": access_token})
#         else:
#             result = jsonify({"error": "Invalid username and or password"})
#     else:
#         result = jsonify({"result": "no results found"})
#     return result
#     # return render_template('register_login.html' password=password, email=email, result=result)


@app.route('/')
def index():
    """Show all dogs for sale."""
    lmt = 4
    query = request.args.get('query')
    params = {
    "q": query,
    "limit": lmt
    }
    r = requests.get("https://dog.ceo/api/breed/{}/images/random/{}".format(params["q"], params["limit"]))

    if r.status_code == 200:
        dogs = json.loads(r.content)['message']
        print(dogs)
    else:
        dogs = "https://www.pexels.com/photo/adorable-animal-breed-canine-356378/"

    return render_template('index.html', doginfo=doginfo.find(), dogs = dogs)


@app.route('/buy')
def buy_dogs():
    """Show all dogs for sale."""
    # Run authenication step
    return render_template('buy_dogs.html', doginfo=doginfo.find())


@app.route('/sell')
def sell_new():
    """Sell a new dog."""
    return render_template('sell_new.html')


@app.route('/', methods=['POST'])
def dog_submit():
    """Sell a new dog."""
    print(request.form.to_dict())
    return redirect(url_for('sell_new'))


@app.route('/sell', methods=['POST'])
def insert_dog_data():
    """Submit a new dog."""
    doginfos = {
        'breed': request.form.get('breed'),
        'description': request.form.get('description'),
        'picture': request.form.get('picture'),
        'location': request.form.get('location')
    }
    #doginfo_id = doginfo.insert_one(doginfo).inserted_id
    doginfo.insert_one(doginfos)
    return redirect(url_for('buy_dogs'))


@app.route('/buy/<dog_id>')
def dog_show(dog_id):
    """Show a single dog."""
    dog = doginfo.find_one({'_id': ObjectId(dog_id)})
    return render_template('dog_show.html', dog=dog)


@app.route('/buy/<dog_id>/edit')
def dog_edit(dog_id):
    """Show the edit form for a dog."""
    dog = doginfo.find_one({'_id': ObjectId(dog_id)})
    return render_template('dog_edit.html', dog=dog)


@app.route('/buy/<dog_id>', methods=['POST'])
def dog_update(dog_id):
    """Submit an edited dog."""
    updated_dog = {
        'breed': request.form.get('breed'),
        'description': request.form.get('description'),
        'picture': request.form.get('picture'),
        'location': request.form.get('location')
    }
    doginfo.update_one(
        {'_id': ObjectId(dog_id)},
        {'$set': updated_dog})
    return redirect(url_for('dog_show', dog_id=dog_id))


@app.route('/buy/<dog_id>/delete', methods=['POST'])
def dog_delete(dog_id):
    """Delete one dog."""
    doginfo.delete_one({'_id': ObjectId(dog_id)})
    return redirect(url_for('buy_dogs'))


if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
