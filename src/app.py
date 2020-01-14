from flask import Flask, render_template, abort
from forms import SignUpForm

# make an object with the imported Flask module. This object will be our WSGI application called app
app = Flask(__name__)
# 設定SECRET_KEY for sinup.html 的 CSRF 使用 (必須要有SECRET_KEY)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'

"""Information regarding the Pets in the System."""
pets = [
    {
        "id": 1,
        "name":
        "Nelly",
        "age": "5 weeks",
        "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles."
    },
    {"id": 2, "name": "Yuki", "age": "8 months", "bio": "I am a handsome gentle-cat. I like to dress up in bow ties."},
    {"id": 3, "name": "Basker", "age": "1 year", "bio": "I love barking. But, I love my friends more."},
    {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Probably napping."},
]


@app.route("/")
def homepage():
    """View function for Home Page."""
    # render_template 會自動去當前目錄下的 templates folder 找尋指定的 template 來使用
    return render_template("home.html", pets=pets)


@app.route("/about")
def about():
    """View function for About Page."""
    return render_template("about.html")


@app.route("/details/<int:pet_id>")
def pet_details(pet_id):
    """View function for Detail Page."""
    pet = next((pet for pet in pets if pet["id"] == pet_id), None)
    if pet is None:
        abort(404, description="No Pet was Found with the given ID")
    return render_template("details.html", pet=pet)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """View function for Signup Page."""
    form = SignUpForm()
    if form.validate_on_submit():
        # for u_email, u_password in users.items():
        #     if u_email == form.email.data and u_password == form.password.data:
        #         return render_template("signup.html", message="Successfully Singed up")
        # return render_template("signup.html", form=form, message="Incorrect Email or Password")
        print("Submitted and Valid.")
    elif form.errors:
        print(form.errors.items())
    return render_template("signup.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
