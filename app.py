from flask import Flask, render_template, request, redirect, url_for
#from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Navigate to /sell_dogs to see dogs for sale!')

# OUR MOCK ARRAY OF PROJECTS
doginfo = [
    { 'breed': 'Goldendoodle', 'age': '1 month' },
    { 'breed': 'Labradoodle', 'age': '1 year' }
]

@app.route('/sell_dogs')
def sell_dogs():
    """Show all playlists."""
    return render_template('sell_dogs.html', doginfo=doginfo)

if __name__ == '__main__':
    app.run(debug=True)