from firebase import firebase
import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response
firebase1 = firebase.FirebaseApplication('https://iottest1-9eb75-default-rtdb.firebaseio.com/', None)

app = Flask(__name__)       #Initialze flask constructor

#Add your own details
config = {
  "apiKey": "AIzaSyB8HQ1PB8xuiZWjXtWQGamanBFEH1DtwAQ",
  "authDomain": "temp-8dbcf.firebaseapp.com",
  "databaseURL": "https://temp-8dbcf-default-rtdb.firebaseio.com",
  "storageBucket": "temp-8dbcf.appspot.com"
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}


#main/ whereour sensor data displaying
@app.route('/main', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    # Data Format
    # [TIME, Temperature, Humidity]
    result1 = firebase1.get('/FirebaseIOT/humidity', None)
    result2 = firebase1.get('FirebaseIOT/temperature', None)
    result3 = firebase1.get('FirebaseIOT/smoke', None)
    Temperature = result1
    Humidity = result2 
    smoke = result3 

    data = [time() * 500, Temperature, Humidity, smoke]

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response

#test/ test
@app.route("/test")
def test():
    return render_template("test.html")

#Login
@app.route("/")
def login():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")

#Welcome page
@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        return render_template("welcome.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            #Redirect to welcome page
            return redirect(url_for('test'))
        except:
            #If there is any error, redirect back to login
            return redirect(url_for('test'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('test'))
        else:
            return redirect(url_for('test'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            #Append data to the firebase realtime database
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

if __name__ == "__main__":
    app.run(debug=True)
