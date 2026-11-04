from flask import Flask, jsonify, session, request
from config import db, migrate, bcrypt
from models import User
import os

app = Flask(
    __name__,
    instance_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance")
)

# Application configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "development-key-change-later"

# Connect Flask to our shared tools
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)

from routes.notes import notes_bp #import routes

app.register_blueprint(notes_bp)#connects that collection to flask app

# Import database models
import models


@app.route("/")
def home():
    return jsonify({"message": "Personal Notes API is running"}), 200
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}

    username =  data.get("username")
    password = data.get("password")
    confirmation = data.get("password_confirmation")

    if not username or not password or not confirmation:
        return jsonify({"errors": ["All fields are required"]}), 400
    if password != confirmation:
         return jsonify({"errors": ["Passwords do not match"]}), 400

   
        # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify ({"errors": ["Username already exists"]}), 409

    # Create a new user
    user = User(username=username)

    # Hash the password
    user.set_password(password)

    # Save the user to the database
    db.session.add(user)
    db.session.commit()

    # Log in the new user
    session["user_id"] = user.id

    return jsonify(user.to_dict()), 201
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
       return jsonify({"errors": ["Invalid username or password"]}), 401

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"errors":[ "Invalid username or password"]}), 401
    #remove previous login session
    session.clear()
    session["user_id"] = user.id

    return jsonify(user.to_dict()), 200
@app.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({}), 401

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({}), 401

    return jsonify(user.to_dict()), 200
@app.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)

    return jsonify({}), 200

    


if __name__ == "__main__":
    app.run(port=5555, debug=True)