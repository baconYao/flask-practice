from flask import Flask, render_template

# make an object with the imported Flask module. This object will be our WSGI application called app
app = Flask(__name__)

@app.route("/")
def homepage():
    """View function for Home Page."""
    # render_template 會自動去當前目錄下的 templates folder 找尋指定的 template 來使用
    return render_template("home.html")


@app.route("/about")
def about():
    """View function for About Page."""
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
