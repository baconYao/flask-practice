from flask import Flask

# make an object with the imported Flask module. This object will be our WSGI application called app
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
