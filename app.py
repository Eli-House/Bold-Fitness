from flask import *
from database import init_db, db_session
from models import *
from sqlalchemy import func


app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "JCAilBNTz6CWp2v3ZQ=="

# TODO: Fill in methods and routes
@app.route("/login",methods=["GET", "POST"])
@app.route("/",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        users = db_session.query(User.username, User.password)
        username = request.form["username"]
        password = request.form["password"]
        
        login = False
        for usernames, passwords in users:
            if username == usernames and password == passwords:
                login = True
                session["username"] = username
                return redirect(url_for("profile"))
        if login == False:
            flash("Either password or username is incorrect", "error")
            return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
     if request.method == "GET":
        return render_template("signup.html")
     else:
        newusername = request.form["newusername"]
        newpassword = request.form["newpassword"]
        checkpassword = request.form["checkpassword"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        age = request.form["age"]
        weight = request.form["weight"]
        height = request.form["height"]

        taken = False
        users = db_session.query(User.username)
        for names in users:
            if newusername == names:
                flash("Username is taken.", "error")
                taken = True
                break
            
        if taken == False:
            if newpassword == checkpassword:
                newUser = User(newusername, newpassword, firstname, lastname, age, weight, height)
                db_session.add(newUser)
                db_session.commit()
                session["username"] = newusername 
                return redirect(url_for("profile"))
            else: 
                flash("Passwords don't match", "error")
                return render_template("signup.html")

@app.route("/exercise")
def exercise():
    upperLifts = db_session.query(Lift.name, Lift.muscle_group, Lift.discription).where(Lift.upper_lower == 1)
    lowerLifts = db_session.query(Lift.name, Lift.muscle_group, Lift.discription).where(Lift.upper_lower == 2)
    latestWorkouts = db_session.query(Workout.lift_id, Workout.num_reps).where(Workout.user_id == session["username"]).order_by(Workout.id.desc()).limit(4)
    uCount = 1
    lCount = 1
    wCount = 1
    uOneName = uOneMg = uOneDis = uTwoName = uTwoMg = uTwoDis = uThreeName = uThreeMg = uThreeDis = uFourName = uFourMg = uFourDis = ""
    lOneName = lOneMg = lOneDis = lTwoName = lTwoMg = lTwoDis = lThreeName = lThreeMg = lThreeDis = lFourName = lFourMg = lFourDis = ""
    wOneName = wOneReps = wTwoName = wTwoReps = wThreeName= wThreeReps = wFourName = wFourReps = ""

    for lifts in upperLifts:
        if uCount == 1:
            uOneName = lifts[0]
            uOneMg = lifts[1]
            uOneDis = lifts[2]
        if uCount == 2:
            uTwoName = lifts[0]
            uTwoMg = lifts[1]
            uTwoDis = lifts[2]
        if uCount == 3:
            uThreeName = lifts[0]
            uThreeMg = lifts[1]
            uThreeDis = lifts[2]
        if uCount == 4:
            uFourName = lifts[0]
            uFourMg = lifts[1]
            uFourDis = lifts[2]
        uCount = uCount + 1
    
    for lifts in lowerLifts:
        if lCount == 1:
            lOneName = lifts[0]
            lOneMg = lifts[1]
            lOneDis = lifts[2]
        if lCount == 2:
            lTwoName = lifts[0]
            lTwoMg = lifts[1]
            lTwoDis = lifts[2]
        if lCount == 3:
            lThreeName = lifts[0]
            lThreeMg = lifts[1]
            lThreeDis = lifts[2]
        if lCount == 4:
            lFourName = lifts[0]
            lFourMg = lifts[1]
            lFourDis = lifts[2]
        lCount = lCount + 1

    for workouts in latestWorkouts:
        if wCount == 1:
            wOneName = workouts[0]
            wOneReps = workouts[1]
        if wCount == 2:
            wTwoName = workouts[0]
            wTwoReps = workouts[1]
        if wCount == 3:
            wThreeName = workouts[0]
            wThreeReps = workouts[1]
        if wCount == 4:
            wFourName = workouts[0]
            wFourReps = workouts[1]
        wCount = wCount + 1
        
    return render_template("exercise.html", uOneName = uOneName, uOneMg = uOneMg, uOneDis = uOneDis, uTwoName = uTwoName, uTwoMg = uTwoMg, uTwoDis = uTwoDis, uThreeName = uThreeName, uThreeMg = uThreeMg, uThreeDis = uThreeDis, uFourName = uFourName, uFourMg = uFourMg, uFourDis = uFourDis, lOneName = lOneName, lOneMg = lOneMg, lOneDis = lOneDis, lTwoName = lTwoName, lTwoMg = lTwoMg, lTwoDis = lTwoDis, lThreeName = lThreeName, lThreeMg = lThreeMg, lThreeDis = lThreeDis, lFourName = lFourName, lFourMg = lFourMg, lFourDis = lFourDis, wOneName = wOneName, wOneReps = wOneReps, wTwoName = wTwoName, wTwoReps = wTwoReps, wThreeName = wThreeName, wThreeReps = wThreeReps, wFourName = wFourName, wFourReps = wFourReps)
    

@app.route("/profile", methods=["GET", "POST"])
def profile():
    currentUser = session["username"]
    userInfo = db_session.query(User.first_name , User.last_name , User.age , User.weight , User.height).where(User.username == currentUser).first()
    learnedExercises = db_session.query(Workout.lift_id).where(Workout.user_id == currentUser).distinct()
    favorite = db_session.query(Workout.lift_id, func.count(Workout.lift_id)).group_by(Workout.lift_id).order_by(func.count(Workout.lift_id).desc())[0]
    fExercise = favorite[0]
    display = ', '.join(map(str, userInfo))
    workouts = []
    for learned in learnedExercises:
        learned = str(learned)[2:]
        learned = learned[:len(learned)-3]
        workouts.append(learned)

    if request.method == "GET":
        return render_template("profile.html", currentUser=currentUser, display=display, workouts=workouts, fExercise=fExercise)
    else:
        exName = request.form["exName"]
        reps = request.form["reps"]
       
        newWorkout = Workout(currentUser, exName, reps)
        db_session.add(newWorkout)
        db_session.commit()
        favorite = db_session.query(Workout.lift_id, func.count(Workout.lift_id)).group_by(Workout.lift_id).order_by(func.count(Workout.lift_id).desc())[0]
        learnedExercises = db_session.query(Workout.lift_id).where(Workout.user_id == currentUser).distinct()
        workouts = []
        for learned in learnedExercises:
            learned = str(learned)[2:]
            learned = learned[:len(learned)-3]
            workouts.append(learned)
        fExercise = favorite[0]
        return render_template("profile.html", currentUser=currentUser, display=display, workouts=workouts, fExercise=fExercise)
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
