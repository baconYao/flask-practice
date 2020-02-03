from flask import Flask, render_template, abort
from forms import SignUpForm, LoginForm, EditPetForm
from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# make an object with the imported Flask module. This object will be our WSGI application called app
app = Flask(__name__)
# 設定SECRET_KEY for sinup.html 的 CSRF 使用 (必須要有SECRET_KEY)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paws.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Pet(db.Model):
    """Model for Pets."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    age = db.Column(db.String)
    bio = db.Column(db.String)
    posted_by = db.Column(db.String, db.ForeignKey("user.id"))


class User(db.Model):
    """Model for Users."""
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    # This back-reference will enable us to point to a row in User by using pet.user.
    pets = db.relationship('Pet', backref='user')


db.create_all()

# Create "team" user and add it to session
team = User(full_name="Pet Rescue Team", email="team@petrescue.co", password="adminpass")
db.session.add(team)

# Create all pets
nelly = Pet(name="Nelly", age="5 weeks", bio="I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.")
yuki = Pet(name="Yuki", age="8 months", bio="I am a handsome gentle-cat. I like to dress up in bow ties.")
basker = Pet(name="Basker", age="1 year", bio="I love barking. But, I love my friends more.")
mrfurrkins = Pet(name="Mr. Furrkins", age="5 years", bio="Probably napping.")

# Add all pets to the session
db.session.add(nelly)
db.session.add(yuki)
db.session.add(basker)
db.session.add(mrfurrkins)

# Commit changes in the session
try:
    db.session.commit()
except Exception as e:
    print("Error: %s" % e)
    db.session.rollback()
finally:
    db.session.close()

# """Information regarding the Pets in the System."""
# pets = [
#     {
#         "id": 1,
#         "name":
#         "Nelly",
#         "age": "5 weeks",
#         "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles."
#     },
#     {"id": 2, "name": "Yuki", "age": "8 months", "bio": "I am a handsome gentle-cat. I like to dress up in bow ties."},
#     {"id": 3, "name": "Basker", "age": "1 year", "bio": "I love barking. But, I love my friends more."},
#     {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Probably napping."},
# ]

# """Information regarding the Users in the System."""
# users = [
#     {"id": 1, "full_name": "Pet Rescue Team", "email": "team@pawsrescue.co", "password": "adminpass"},
# ]


@app.route("/")
def homepage():
    """View function for Home Page."""
    # render_template 會自動去當前目錄下的 templates folder 找尋指定的 template 來使用
    pets = Pet.query.all()
    return render_template("home.html", pets=pets)


@app.route("/about")
def about():
    """View function for About Page."""
    return render_template("about.html")


@app.route("/details/<int:pet_id>", methods=["POST", "GET"])
def pet_details(pet_id):
    """View function for Detail Page."""
    form = EditPetForm()
    pet = Pet.query.get(pet_id)
    if pet is None:
        abort(404, description="No Pet was Found with the given ID")
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.age = form.age.data
        pet.bio = form.bio.data
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("details.html", pet=pet, form=form, message="A Pet with this name already exists!")
    return render_template("details.html", pet=pet, form=form)


@app.route("/delete/<int:pet_id>")
def delete_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None:
        abort(404, description="No Pet was Found with the given ID")
    db.session.delete(pet)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('homepage'))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """View function for Signup Page."""
    form = SignUpForm()
    if form.validate_on_submit():
        print("Submitted and Valid.")
        new_user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            password=form.password.data
        )
        # new_user = {
        #     "id": len(users)+1,
        #     "full_name": form.full_name.data,
        #     "email": form.email.data,
        #     "password": form.password.data
        # }
        # users.append(new_user)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print("Sing up error: %s" % e)
            db.session.rollback()
            return render_template(
                "signup.html",
                form=form,
                message="This Email already exists in the system! Please Log in instead."
            )
        finally:
            db.session.close()
        return render_template("signup.html", message="Successfully signed up")
    elif form.errors:
        print(form.errors.items())
    return render_template("signup.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # user = next(
        #     (user for user in users if user["email"] == form.email.data and user["password"] == form.password.data),
        #     None
        # )

        # 透過 get (Primary key) 取得 user 訊息
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        if user is None:
            return render_template("login.html", form=form, message="Wrong Credentials. Please Try Again.")
        else:
            print("User: %s" % user)
            # why did we not directly store the user object in the session variable?
            # That is a perfectly valid question. The reason is that this object is not JSON serializable and we can not use such objects in the session dictionary.
            session['user'] = user.id
            return render_template("login.html", message="User: '%s' Successfully Logged In!" % user.full_name)
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('homepage'))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
