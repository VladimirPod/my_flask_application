from flask import Flask 


def create_app():
    app = Flask(__name__)
    
     # Импортируем созданный Blueprint
    from app.routes.auth import auth_bp
    
    
    # Регистрируем его в приложении. 
    # url_prefix добавит '/auth' ко всем ссылкам этого блюпринта автоматически.
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    @app.route('/')
    def home():
        return '<h1>Главная страница сайта</h1><a href="/auth/register">Перейти к регистрации</a>'
    
    
    
    return app