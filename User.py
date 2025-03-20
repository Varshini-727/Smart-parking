from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
from config import MONGO_URI
# MongoDB connection
client = MongoClient(MONGO_URI)
db = client['user_database']
users_collection = db['users']

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if users_collection.find_one({"username": username}):
            flash("Username already exists!")
            return redirect(url_for("register"))
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({"username": username, "password": hashed_password})
        flash("Registration successful! Please log in.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = users_collection.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            session["user_id"] = str(user["_id"])
            flash("Login successful!")
            return redirect(url_for("dashboard"))
        flash("Invalid username or password!")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/area/<area_name>")
def area(area_name):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if area_name == "area1":
        video_path = "../static/area1.mp4"
        return render_template("area.html", video_path=video_path, area_name=area_name)
    if area_name == "area2":
        video_path = "../static/area1.mp4"
        return render_template("area2.html", video_path=video_path, area_name=area_name)
    if area_name == "area3":
        video_path = "../static/area1.mp4"
        return render_template("area3.html", video_path=video_path, area_name=area_name)    
    flash("Area not found!")
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)