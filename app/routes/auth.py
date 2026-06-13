from flask import Blueprint, url_for, render_template

auth_bp = Blueprint('auth', __name__, template_folder='templates')



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'] )
def login():
    return render_template('auth/login.html')