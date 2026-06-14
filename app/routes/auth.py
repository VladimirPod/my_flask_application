from flask import Blueprint, url_for, render_template, request, redirect, flash, get_flashed_messages
from app.models import User
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User 
import re
import os



# Регулярное выражение для строгой проверки email (обязательно наличие точки и домена)
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Определяем точный путь к папке templates внутри auth
auth_templates = os.path.join(os.path.dirname(__file__), 'templates')

auth_bp = Blueprint('auth', __name__, template_folder='templates')



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        get_flashed_messages()
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not (username and email and password and confirm_password):
            flash('Все поля должны быть заполнены!', 'danger')
            return redirect(url_for('auth.register'))
        
        # проверка с точным текстом ошибки
        if not re.match(EMAIL_REGEX, email):
            flash('Пожалуйста, ведите корректный email!', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Пароли не совпадают!', 'danger')
            return redirect(url_for('auth.register'))
    
        if User.query.filter(User.email == email).first():
            flash('Пользователь с такой почтой уже существует!', 'danger')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Регистрация успешна! Войдите в аккаунт.', 'success')        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')
    
    

@auth_bp.route('/login', methods=['GET', 'POST'] )
def login():
    if request.method == 'GET':
        get_flashed_messages()
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        if not re.match(EMAIL_REGEX, email):
            flash('Пожалуйста, ведите корректный email!', 'danger')
            return redirect(url_for('auth.login'))

        user = User.query.filter(User.email == email).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Вы успешно вошли в аккаунт!', 'success')
            return redirect(url_for('main.home'))
        
        else:
            flash('Неверный email или пароль!', 'danger')
            return redirect(url_for('auth.login'))
        
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    return render_template('auth/login.html')


    # Добавьте в самый конец app/routes/auth.py
@auth_bp.route('/logout')
@login_required # Защищает роут, чтобы выйти могли только те, кто вошел
    
def logout():
    logout_user() # Flask-Login уничтожает сессию пользователя
    flash('Вы успешно вышли из аккаунта!', 'success')
    return redirect(url_for('main.home')) # Перенаправляем на главную страницу

