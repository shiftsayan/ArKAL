from flask import Flask, render_template, request, g
from flask_sqlalchemy import SQLAlchemy
from parser import parse
import datetime, time
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(64), unique=False, nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    code = db.Column(db.Integer, unique=False, nullable=False)
    time = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return "[{}, {}, {}, {}]".format(type(self), self.name, self.code, self.time)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        data = parse(Event.query.all())
        return render_template("index.html", persons=data)
        # return render_template('index.html')
    return "POST"
    # Otherwise, we are logged in

@app.route("/delete", methods=["GET"])
def delete():
    for event in Event.query.all():
        db.session.delete(event)
        db.session.commit()
    return "Deleted."

@app.route("/post", methods=["POST"])
def post_image():
    try:
        event = Event(name=request.form["name"], code=int(request.form["code"]), time=int(time.time()))
        db.session.add(event)
        db.session.commit()
        return "Success."
    except Exception as e:
        print("Post request threw an exception:\n {}.".format(e))
        return "Failure."

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
