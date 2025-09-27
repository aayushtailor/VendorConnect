from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Demo home route
@app.route("/")
def home():
    return render_template("index.html")

# Registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        # Later we’ll save this to database
        return f"User {username} registered successfully!"
    return render_template("register.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        # Later we’ll check this from database
        return f"Welcome back, {email}!"
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
