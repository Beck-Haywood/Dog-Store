from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient()
db = client.PoodleWebsite
doginfo = db.doginfo

app = Flask(__name__)

#@app.route('/')
#def index():
#    """Return homepage."""
#    return render_template('home.html', msg='Homepage')

@app.route('/')
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
    doginfo = {
        'breed': request.form.get('breed'),
        'description': request.form.get('description')
    }
    #doginfo_id = doginfo.insert_one(doginfo).inserted_id
    doginfo.insert_one(doginfo)
    return redirect(url_for('buy_dogs'))


if __name__ == '__main__':
    app.run(debug=True)