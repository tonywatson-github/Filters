from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.filter import Filter
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt= Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=["POST"])
def register():
    if not User.valid(request.form):
        return redirect('/')
    data = {
        "first": request.form['first'],
        "last": request.form['last'],
        "email": request.form['email'],
        "passw": bcrypt.generate_password_hash(request.form['passw']) 
    }
    idd = User.save(data)
    session['idd'] = idd
    return redirect ('/dashboard')


@app.route('/login',methods=['POST'])
def login():
    user = User.emai(request.form)
    if not user:
        flash("Invalid email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.passw,request.form['passw']):
        flash("Invalid password","login")
        return redirect('/')
    session["idd"] = user.id
    return redirect("/dashboard")


@app.route('/dashboard')
def dashboard():
    if 'idd' not in session:
        return redirect ('/logout')
    data = {
        'id' : session['idd']
        }
    return render_template('dashboard.html', user= User.one(data), filters = Filter.all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

