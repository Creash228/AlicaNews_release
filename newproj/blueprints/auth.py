from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from forms.auth import LoginForm, RegisterForm
from services.user_service import UserService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = UserService.get_by_email(db.session, form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        flash('Неверный email или пароль')
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            flash('Пароли не совпадают')
            return render_template('register.html', form=form)
        
        existing = UserService.get_by_email(db.session, form.email.data)
        if existing:
            flash('Пользователь с таким email уже существует')
            return render_template('register.html', form=form)
        
        user = UserService.create(
            db.session,
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        login_user(user)
        return redirect(url_for('main.index'))
    
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
    