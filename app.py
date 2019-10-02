from flask import Flask, render_template, request, redirect, url_for, jsonify, json
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
from flask_bcrypt import Bcrypt
from flask_cors import CORS

client = MongoClient()
db = client.PoodleWebsite
doginfo = db.doginfo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mernloginreg'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mernloginreg'
app.config['JWT_SECRET_KEY'] = 'secret'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)

#@app.route('/')
#def index():
#    """Return homepage."""
#    return render_template('home.html', msg='Homepage')
@app.route('/users/register', methods=['POST'])
def register():
    users = mongo.db.users
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password'].decode('utf-8'))

    user_id = users.insert({
    'email': email,
    'password': password,
    })

    new_user = users.find_one({'_id' : user_id})
    result = {'email' : new+user['email'] + ' registered'}
    return jsonift({'result' : result})

@app.route('/users/login', methods=['POST'])
def login():
    users = mongo.db.users
    email = request.get_json()['email']
    password = requests.get_json()['password']
    result = ""

    response = user.find_one({'email' : email})

    if response:
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity = {
            'email': response['email']}
            )
            result = jsonify({"token":access_token})
        else:
            result = jsonify({"error":"Invalid username and or password"})
    else:
        result = jsonify({"result":"no results found"})
    return result

'''@app.route('/')
def sell_dogs():
    """Show all dogs for sale."""
    return render_template('sell_dogs.html', doginfo=doginfo.find())

@app.route('/buy')
def buy_dogs():
    """Show all dogs for sale."""
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
        'description': request.form.get('description')
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
'''
if __name__ == '__main__':
    app.run(debug=True)