from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    app.config['SECRET_KEY'] = 'admin'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    # Импортируем созданный Blueprint
    from app.routes.auth import auth_bp
    # Регистрируем его в приложении. 
    # url_prefix добавит '/auth' ко всем ссылкам этого блюпринта автоматически.
    app.register_blueprint(auth_bp, url_prefix='/auth')

    with app.app_context():
        
        from app import models
        
        db.create_all()
    
    @app.route('/')
    def home():
        return '<h1>Главная страница сайта</h1><a href="/auth/register">Перейти к регистрации</a>'
    
    
    
    return app