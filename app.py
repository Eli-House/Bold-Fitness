from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "JCAilBNTz6CWp2v3ZQ=="

# TODO: Fill in methods and routes
@app.route("/",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]

        if password == "123":
            session["username"] = username
            return redirect(url_for("profile"))
        else:
            flash("Either password or username is incorrect", "error")
            return render_template("login.html")

@app.route("/exercise")
def exercise():
    return render_template("exercise.html")
    newexercise = Exercise(uname, passOne)
    db_session.add(newUser)
    db_session.commit()

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("/"))

@app.before_first_request
def setup():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
