from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Upload folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ---------------- Database Setup ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Vendors Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT,
            business TEXT,
            category TEXT,
            city TEXT,
            phone TEXT,
            email TEXT UNIQUE,
            password TEXT,
            business_photo TEXT,
            personal_photo TEXT,
            description TEXT,
            is_verified INTEGER DEFAULT 0,
            views INTEGER DEFAULT 0
        )
    """)

    # Admins Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    # Default admin
    c.execute("SELECT * FROM admins WHERE email=?", ("admin@jaipurjewells.com",))
    if not c.fetchone():
        c.execute("INSERT INTO admins (email, password) VALUES (?, ?)", ("admin@jaipurjewells.com", "admin123"))

    conn.commit()
    conn.close()

init_db()

# ---------------- Main Routes ----------------
@app.route("/")
def home():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    # Fetch top 6 verified vendors
    c.execute("""
        SELECT id, fullname, business, category, city, phone, email, business_photo, personal_photo, is_verified 
        FROM vendors 
        WHERE is_verified=1 
        ORDER BY id DESC 
        LIMIT 6
    """)
    vendors = c.fetchall()
    conn.close()

    return render_template("index.html", vendors=vendors)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

# Vendor logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("home"))

# Admin logout
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    flash("Admin logged out successfully", "info")
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "vendor_id" not in session:
        return redirect(url_for("login"))

    vendor_id = session["vendor_id"]
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM vendors WHERE id=?", (vendor_id,))
    vendor = c.fetchone()
    conn.close()
    return render_template("dashboard.html", vendor=vendor)

# ---------------- Vendors ----------------
@app.route("/vendors")
def vendors_list():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    city = request.args.get("city", "").strip()

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    query = "SELECT id, fullname, business, category, city, phone, email, business_photo, personal_photo, is_verified FROM vendors WHERE is_verified=1"
    params = []

    if search:
        query += " AND (fullname LIKE ? OR business LIKE ? OR email LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    if category:
        query += " AND category LIKE ?"
        params.append(f"%{category}%")

    if city:
        query += " AND city LIKE ?"
        params.append(f"%{city}%")

    c.execute(query, tuple(params))
    vendors = c.fetchall()
    conn.close()

    return render_template("vendor.html", vendors=vendors, search=search, category=category, city=city)


@app.route("/vendor/<int:vendor_id>")
def vendor_profile(vendor_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Increment profile views
    c.execute("UPDATE vendors SET views = views + 1 WHERE id=?", (vendor_id,))
    conn.commit()

    # Fetch vendor
    c.execute("SELECT * FROM vendors WHERE id=?", (vendor_id,))
    vendor = c.fetchone()
    conn.close()

    if not vendor:
        flash("Vendor not found", "danger")
        return redirect(url_for("vendors_list"))

    return render_template("vendor_profile.html", vendor=vendor)

# ---------------- Register ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        business = request.form["business"]
        category = request.form["category"]
        city = request.form["city"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        description = request.form.get("description", "")

        # Check if email already exists
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT id FROM vendors WHERE email=?", (email,))
        existing = c.fetchone()
        if existing:
            conn.close()
            flash("Email already registered. Please login or use another email.", "error")
            return redirect(url_for("register"))

        # Handle file uploads
        business_photo = request.files["business_photo"]
        personal_photo = request.files["personal_photo"]
        business_filename = secure_filename(business_photo.filename)
        personal_filename = secure_filename(personal_photo.filename)
        business_photo.save(os.path.join(app.config["UPLOAD_FOLDER"], business_filename))
        personal_photo.save(os.path.join(app.config["UPLOAD_FOLDER"], personal_filename))

        # Insert vendor
        c.execute("""
            INSERT INTO vendors (
                fullname, business, category, city, phone, email, password,
                business_photo, personal_photo, description, is_verified
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fullname, business, category, city, phone, email, password,
            business_filename, personal_filename, description, 0
        ))
        conn.commit()
        conn.close()

        flash("Your account has been submitted for review. You will be notified once approved.", "info")
        return redirect(url_for("register"))

    return render_template("register.html")

# ---------------- Login ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # Admin login
        c.execute("SELECT * FROM admins WHERE email=? AND password=?", (email, password))
        admin = c.fetchone()
        if admin:
            session["admin"] = True
            conn.close()
            return redirect(url_for("admin_vendors"))

        # Vendor login
        c.execute("SELECT * FROM vendors WHERE email=? AND password=?", (email, password))
        vendor = c.fetchone()
        conn.close()

        if vendor:
            if vendor[11] == 1:  # is_verified
                session["vendor_id"] = vendor[0]
                return redirect(url_for("dashboard"))
            else:
                flash("Your account is under review.", "error")
                return redirect(url_for("login"))

        flash("Invalid credentials", "error")
    return render_template("login.html")

# ---------------- Admin ----------------
@app.route("/admin/vendors")
def admin_vendors():
    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM vendors")
    vendors = c.fetchall()
    conn.close()
    return render_template("admin_vendors.html", vendors=vendors)

@app.route("/notifications")
def notifications():
    if "vendor_id" not in session:
        return redirect(url_for("login"))
    return render_template("notifications.html")

@app.route("/admin/verify/<int:vendor_id>")
def verify_vendor(vendor_id):
    if "admin" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE vendors SET is_verified=1 WHERE id=?", (vendor_id,))
    conn.commit()
    conn.close()
    flash("Vendor verified!", "success")
    return redirect(url_for("admin_vendors"))

@app.route("/admin/unverify/<int:vendor_id>")
def unverify_vendor(vendor_id):
    if "admin" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE vendors SET is_verified=0 WHERE id=?", (vendor_id,))
    conn.commit()
    conn.close()
    flash("Vendor unverified!", "warning")
    return redirect(url_for("admin_vendors"))
# ---------------- Blogs ---------------
@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/blog/<slug>")
def blog_single(slug):
    return render_template("blog-single.html", slug=slug)

@app.route("/dashboard/edit", methods=["GET", "POST"])
def edit_profile():
    if "vendor_id" not in session:
        return redirect(url_for("login"))

    vendor_id = session["vendor_id"]
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if request.method == "POST":
        fullname = request.form["fullname"]
        business = request.form["business"]
        category = request.form["category"]
        city = request.form["city"]
        phone = request.form["phone"]
        description = request.form.get("description", "")

        # Handle optional photo updates
        business_filename, personal_filename = None, None
        if "business_photo" in request.files:
            business_photo = request.files["business_photo"]
            if business_photo and business_photo.filename:
                business_filename = secure_filename(business_photo.filename)
                business_photo.save(os.path.join(app.config["UPLOAD_FOLDER"], business_filename))

        if "personal_photo" in request.files:
            personal_photo = request.files["personal_photo"]
            if personal_photo and personal_photo.filename:
                personal_filename = secure_filename(personal_photo.filename)
                personal_photo.save(os.path.join(app.config["UPLOAD_FOLDER"], personal_filename))

        # Build update query dynamically
        update_query = """UPDATE vendors SET fullname=?, business=?, category=?, city=?, phone=?, description=?"""
        params = [fullname, business, category, city, phone, description]

        if business_filename:
            update_query += ", business_photo=?"
            params.append(business_filename)
        if personal_filename:
            update_query += ", personal_photo=?"
            params.append(personal_filename)

        update_query += " WHERE id=?"
        params.append(vendor_id)

        c.execute(update_query, tuple(params))
        conn.commit()
        conn.close()

        flash("Profile updated successfully!", "success")
        return redirect(url_for("dashboard"))

    # GET request → fetch current vendor data
    c.execute("SELECT * FROM vendors WHERE id=?", (vendor_id,))
    vendor = c.fetchone()
    conn.close()

    return render_template("edit_profile.html", vendor=vendor)


# ---------------- Run ----------------
if __name__ == "__main__":
    app.run(debug=True)
