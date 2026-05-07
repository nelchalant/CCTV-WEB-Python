from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db
from models.user import User
from models.log import Log
import bcrypt
import I_S_Y as Isy

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm  = request.form['confirm_password']

        if password != confirm:
            flash('Passwords do not match!')
            return redirect(url_for('auth.register'))

        if len(password) < 8:
            flash('Password must be at least 8 characters!')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!')
            return redirect(url_for('auth.register'))

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)

        log = Log(username=username, action='Registered an account')
        db.session.add(log)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(
            password.encode('utf-8'),
            user.password.encode('utf-8')
        ):
            session['username'] = username

            log = Log(username=username, action='Logged in')
            db.session.add(log)
            db.session.commit()

            return redirect(url_for('camera.dashboard'))
        else:
            flash('login failed')
            return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth.route('/logout')
def logout():
    username = session.get('username')

    if username:
        log = Log(username=username, action='Logged out')
        db.session.add(log)
        db.session.commit()

    session.pop('username', None)
    return redirect(url_for('auth.login'))
