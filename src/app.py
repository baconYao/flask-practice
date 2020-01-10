from flask import Flask, render_template

# make an object with the imported Flask module. This object will be our WSGI application called app
app = Flask(__name__)


@app.route("/")
def hello():
    # render_template 會自動去當前目錄下的 templates folder 找尋指定的 template 來使用
    return render_template("home.html")


@app.route("/educative")
def learn():
    return "Happy Learning at Educative!"


@app.route("/name/<my_name>")
def greatings(my_name):
    """View function to greet the user by name."""
    return "Welcome " + my_name + "!"


@app.route('/square/<int:number>')
def show_square(number):
    """View that shows the square of the number passed by URL"""
    return "Square of " + str(number) + " is: " + str(number * number)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
