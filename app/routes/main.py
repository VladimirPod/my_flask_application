import os
from flask import Blueprint, render_template,current_app

# 1. Находим абсолютный путь к главной папке app/templates/
# os.path.dirname(__file__) указывает на app/routes/
# .. поднимает нас на уровень выше, в папку app/
base_dir = os.path.dirname(__file__)
main_templates = os.path.abspath(os.path.join(base_dir, '..', 'templates'))

# 2. Передаем этот точный путь в Blueprint
main_bp = Blueprint('main', __name__, template_folder=main_templates)

@main_bp.route('/')
def home():
    # ЭТИ СТРОКИ НАПЕЧАТАЮТ В ТЕРМИНАЛ ВСЕ ПУТИ ХРАНЕНИЯ ШАБЛОНОВ
    print("=== ОТЛАДКА ПУТЕЙ ШАБЛОНОВ ===")
    print("Главный путь приложения:", current_app.template_folder)
    print("Путь блупринта main:", main_bp.template_folder)
    print("Существует ли файл index.html по пути блупринта:", 
    os.path.exists(os.path.join(main_templates, 'index.html')))
    print("==============================")
    
    
    return render_template('index.html') # Теперь Flask железно найдет этот файл

