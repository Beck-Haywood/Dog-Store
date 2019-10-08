from flask import Flask, render_template, request, redirect, url_for, jsonify, json
from pymongo import MongoClient
import requests
import json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os


# host = os.environ.get('MONGODB_URI', 'mongodb://<heroku_h8zw53pl>:<bghbgh123->@ds229118.mlab.com:29118/heroku_h8zw53pl')
# mclient = MongoClient(host=f'{host}?retryWrites=false')
# db = client.get_default_database()

client = MongoClient()
db = client.DogWebsite  # was Poodle
doginfo = db.doginfo

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    """Show all dogs for sale."""
    lmt = 8
    query = request.form.get('query')
    params = {
    "q": query,
    "limit": lmt
    }
    r = requests.get("https://dog.ceo/api/breed/{}/images/random/{}".format(params["q"], params["limit"]))
    #print(query)
    if r.status_code == 200:
        dogs = json.loads(r.content)['message']
        #print(dogs)
    else:
        dogs = ""
    b = requests.get("https://dog.ceo/api/breeds/list/all")
    breeds = json.loads(b.content)['message']
    return render_template('index.html', doginfo=doginfo.find(), dogs = dogs, breeds = breeds)

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
        #'picture': request.form.get('picture'),
        'location': request.form.get('location'),
        'contact': request.form.get('contact')
    }
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
        #'picture': request.form.get('picture'),
        'location': request.form.get('location'),
        'contact': request.form.get('contact')

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
