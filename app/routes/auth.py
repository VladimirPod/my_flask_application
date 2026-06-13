from flask import Blueprint, url_for, render_template, request, redirect, flash
from app.models import User
from app import db
# ИМПОРТ ЗДЕСЬ: импортируем класс User из файла моделей
from app.models import User 
import re

# Регулярное выражение для строгой проверки email (обязательно наличие точки и домена)
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

auth_bp = Blueprint('auth', __name__, template_folder='templates')



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not (username and email and password and confirm_password):
            flash('Все поля должны быть заполнены!')
            return redirect(url_for('auth.register'))
        
        # проверка с точным текстом ошибки
        if not re.match(EMAIL_REGEX, email):
            flash('Пожалуйста, ведите корректный email!')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Пароли не совпадают!')
            return redirect(url_for('auth.register'))
    
        if User.query.filter(User.email == email).first():
            flash('Пользователь с такой почтой уже существует!')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Регистрация успешна! Войдите в аккаунт.')        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')
    
    

@auth_bp.route('/login', methods=['GET', 'POST'] )
def login():
    return render_template('auth/login.html')