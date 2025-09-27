from flask import Flask, render_template

app = Flask(__name__)

# Default Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Dynamic Route - opens any html file by name
@app.route("/<page>")
def render_page(page):
    try:
        return render_template(f"{page}.html")
    except:
        return "<h1>404 - Page Not Found</h1>", 404

if __name__ == "__main__":
    app.run(debug=True)
