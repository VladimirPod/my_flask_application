from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
import os


db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # 1. Находим корень ВСЕГО проекта (на уровень выше, чем текущий app/__init__.py)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # 2. Указываем точные пути к шаблонам и внешней папке instance
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    instance_dir = os.path.join(project_root, 'instance')
    
    # 3. Инициализируем Flask с указанием папки instance_path
    app = Flask(__name__, 
                template_folder=template_dir, 
                static_folder=static_dir,
                instance_path=instance_dir,          # Явно задаем внешнюю папку
                instance_relative_config=True)       # Позволяет использовать относительные пути
    
    
    app.config['SECRET_KEY'] = 'admin'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(instance_dir,'project.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    
    
    db.init_app(app)
    
    # 3. Инициализируем LoginManager
    login_manager.init_app(app)
    # Перенаправит гостя на страницу логина, если он полезет на защищенный роут
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите в аккаунт для доступа к этой странице.'
    # 4. Функция загрузки пользователя (загружает юзера из БД по ID из сессии)
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    
    with app.app_context():
        from app import models
        db.create_all()
        
    
    return app
