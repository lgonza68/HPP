from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, DataForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from datetime import timezone
from app.models import User, Post
from app.email import send_password_reset_email
import pandas as pd
import joblib

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Guest'}
    return render_template('index.html', title='Home', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next_page')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect (url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for instructions on resetting your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user=User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.sesssion.commit()
        flash('Your password has been reset.')
        return redirect((url_for('login')))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>') 
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        
        
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data  
        db.session.commit()
        flash('Your changes have been saved!')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile', form=form)
        
        


@app.route('/aboutus')
def about():
    return render_template('aboutus.html', title='About')


@app.route('/data', methods=['GET', 'POST'])
@login_required
def data():
    form = DataForm(request.form)
    
    if request.method == "POST":
        lin_reg = joblib.load("lin_reg.pkl")
        
        HouseSqFootage = request.form.get("HouseSqFootage")
        YearBuilt = request.form.get("YearBuilt")
        ZipCode = request.form.get("ZipCode")
        NumBedrooms = request.form.get("NumBedrooms")
        NumBathrooms = request.form.get("NumBathrooms")
        LotSize = request.form.get("LotSize")
        Basement = request.form.get("Basement")
        Remodeled = request.form.get("Remodeled")
        Garage = request.form.get("Garage")
        Pool = request.form.get("Pool")
        Porch = request.form.get("Porch")
        
        X = pd.DataFrame([[HouseSqFootage, YearBuilt, ZipCode, NumBedrooms, NumBathrooms, LotSize, Basement, Remodeled, Garage, Pool, Porch]], columns=["HouseSqFootage," "YearBuilt", "ZipCode", "NumBedrooms", "NumBathrooms", "LotSize", "Basement", "Remodeled", "Garage", "Pool", "Porch"])
    
        prediction = lin_reg.predict(X)[0]
        
    else:
        prediction = ""
        
    return render_template('dataEntry.html', output=prediction, form=form)                                                                                                                                            
                                                                                                                                                             
    
    #form = DataForm()
    #if form.validate_on_submit():
    #    name = form.name.data
    #    form.name.data = ''
    #return render_template('dataEntry.html', form=form)


@app.route("/HPP_Icon.png")
def image():
    return render_template("HPP_Icon.png")
