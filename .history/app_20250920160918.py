from flask import Flask, render_template

app = Flask(__name__)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Register Page
@app.route("/register")
def register():
    return render_template("register.html")

# Login Page
@app.route("/login")
def login():
    return render_template("login.html")

# Vendor Page
@app.route("/vendor")
def vendor():
    return render_template("vendor.html")

# Dashboard Page
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Blog Page
@app.route("/blog")
def blog():
    return render_template("blog.html")

# Blog Single Page
@app.route("/blog-single")
def blog_single():
    return render_template("blog-single.html")

# About Page
@app.route("/about")
def about():
    return render_template("about.html")

# Contact Page
@app.route("/contact")
def contact():
    return render_template("contact.html")

# Privacy Page
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

# Terms Page
@app.route("/terms")
def terms():
    return render_template("terms.html")

# Admin Login Page
@app.route("/admin-login")
def admin_login():
    return render_template("admin-login.html")

# Admin Dashboard Page
@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)
