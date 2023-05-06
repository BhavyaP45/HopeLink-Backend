from flask import Flask, redirect, render_template, request
#Import Libraries
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
#Import the local route for this application
import os

#Configure App
app = Flask(__name__, template_folder="templates", static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(400), nullable = False)
    name = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return '<Description %r>' %self.id

'''
Create Database
with app.app_context():
    db.create_all()
'''

@app.route('/', methods = ["POST", "GET"])
def index():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        name = request.form['name']

        new_post = Location(title = title, description = content, name = name)
    
        db.session.add(new_post)
        db.session.commit()
        return redirect("/")

        
    else:
        locations = Location.query.order_by(Location.date).all()
        return render_template('index.html', locations = locations)

if __name__ == "__main__":
    app.run(debug=True)
