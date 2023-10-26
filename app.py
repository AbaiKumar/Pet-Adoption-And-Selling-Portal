from Classes import *
from Model import *
from flask import Flask, jsonify, request, render_template, session, redirect, url_for, send_from_directory
from flask_cors import CORS
from datetime import datetime
from ML import *
import os
from PIL import *

app = Flask(__name__)
app.secret_key = 'QWJhaWt1bWFyIEk='
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["POST", "GET"])
def signup():
    if session and session['username']:
        return redirect(url_for('dashboard'))
    elif request.method == "GET":
        return render_template("signup.html", msg=None)
    else:
        usr = User(request.form["mail"], request.form["pwd"])
        if data.createAccount(request.form["mail"], usr):
            return redirect(url_for('login'))
        else:
            return render_template("signup.html", msg="Account already exists")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if session and session['username']:
            return redirect(url_for('dashboard'))
        return render_template("login.html", msg=None)
    else:
        if data.loginAccount(request.form["mail"], request.form["pwd"]) == True:
            session['username'] = request.form["mail"]
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html", msg="Invalid User or Password")


@app.route("/survey", methods=["POST", "GET"])
def survey():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    elif request.method == "POST":
        time_commitment = request.form.get('time_commitment')
        living_space = request.form.get('living_space')
        activity_level = request.form.get('activity_level')
        preferences = request.form.getlist('preferences')
        travel_frequency = request.form.get('travel_frequency')
        noise_tolerance = request.form.get('noise_tolerance')
        username = session.get('username')
        usrsurvey = Usersurvey(time_commitment, living_space,
                               activity_level, preferences, travel_frequency, noise_tolerance)
        data.updatesurvey(username, usrsurvey)
        return redirect(url_for('dashboard'))
    else:
        return render_template("survey.html")


@app.route('/logout')
def logout():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    session.pop('username', None)  # Remove the 'username' from the session
    # Redirect to the login page or another page of your choice
    return redirect(url_for('login'))


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    elif 'petImage' not in request.files:
        return redirect(request.url)

    file = request.files['petImage']
    price = request.form['price']
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    image_id = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    new_file_name = f'{image_id}-{session.get("username")}.{file_extension}'

    # Save the uploaded file with the new name
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_file_name)
    file.save(file_path)
    breed = ml.predict_breed_and_habits(file_path)
    data.uploadpet(image_id, breed, session['username'], file_path, price)
    return redirect(url_for('dashboard'))


@app.route('/static/<path:filename>')
def static_file(filename):
    return app.send_static_file(filename)


@app.route('/dashboard')
def dashboard():
    print("hi")
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    print(session['username'])
    return render_template("dashboard.html")


@app.route('/addPets')
def addPets():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return render_template("petupload.html")


@app.route('/getRecommended', methods=["POST", "GET"])
def getRecommended():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return jsonify(data.getMatchedPets(session.get('username')))


@app.route('/getAdoption', methods=["POST", "GET"])
def getAdoption():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return jsonify(data.getAdoptionPets(session.get('username')))


@app.route('/uploads/<path:filename>')
def getPetImage(filename):
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/confirmation', methods=["GET"])
def confirmation():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    print(session.get('username'))
    print("session confirm")
    data.confirm(session.get('username'), request.args.get("id"))
    return redirect(url_for('dashboard'))


@app.route('/confirm1', methods=["GET"])
def confirm1():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    data.sellerConfirm(request.args.get("id"))
    return redirect(url_for('orders'))


@app.route('/confirm2', methods=["GET"])
def confirm2():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    data.buyerConfirm(request.args.get("id"))
    return redirect(url_for('orders'))


@app.route('/cancel1', methods=["GET"])
def cancel1():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    data.sellerCancel(request.args.get("id"))
    return redirect(url_for('orders'))


@app.route('/cancel2', methods=["GET"])
def cancel2():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    data.buyerCancel(request.args.get("id"))
    return redirect(url_for('orders'))


@app.route('/orders', methods=["GET"])
def orders():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return render_template("orders.html")


@app.route('/getOrders', methods=["POST", "GET"])
def order():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return jsonify(data.orderList(session['username']))


@app.route("/admin", methods=["POST", "GET"])
def admin():
    if request.method == "POST":
        breed = request.form.get('breed')
        time_commitment = request.form.get('time_commitment')
        living_space = request.form.get('living_space')
        activity_level = request.form.get('activity_level')
        preferences = request.form.getlist('preferences')
        travel_frequency = request.form.get('travel_frequency')
        noise_tolerance = request.form.get('noise_tolerance')
        pet = petsurveyupdate(breed, time_commitment, living_space,
                              activity_level, preferences, travel_frequency, noise_tolerance)
        data.updatebreed(breed, pet)
        return redirect(url_for('admin'))
    else:
        return render_template("admin.html")


@app.route('/remove', methods=["GET"])
def remove():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    data.remove(request.args.get("id"))
    return redirect(url_for('sell'))


@app.route('/sell', methods=["GET"])
def sell():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return render_template("sell.html")


@app.route('/getsell', methods=["POST", "GET"])
def getsell():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return jsonify(data.getsell(session.get('username')))


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
