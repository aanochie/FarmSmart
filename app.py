from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_login import current_user, LoginManager
from flask_qrcode import QRcode
# Written by: Steven (c2045361), Zheng (c2041164), Aitsam (c2031215)
# Asare (c2059143), Malak (c2001143), Nathan (c2026512)

def create_app():
    # Set the secret key for session management
    SECRET_KEY = 'secret key'
    app = Flask(__name__)
    # Configure the Flask application using the values from this module
    app.config.from_object(__name__)
    app.config['TESTING'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farm_smart.db'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['RECAPTCHA_PUBLIC_KEY'] = '6Ld5jykpAAAAAOMYsHsjLRPFaPMpWIDGO2lx9wIz'
    app.config['RECAPTCHA_PRIVATE_KEY'] = '6Ld5jykpAAAAAGovtwtXOmGLjZBz1uKLeirLVYay'
    app.secret_key = SECRET_KEY
    return app


app = create_app()
# Init database
database = SQLAlchemy(app)
qrcode = QRcode(app)


# Define a route for the homepage
@app.route('/')
def index():
    # Render the main/index.html template when accessing the homepage
    return render_template('main/index.html')


def requires_roles(*roles):
    """
    Decorator to require certain roles to access a view.
    """

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Check if the current user's role is in the allowed roles
            if current_user.role not in roles:
                # If not, render the 403 Forbidden page
                return render_template('403.html')
            # Otherwise, call the original function
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def login_required(f):
    """
    Decorator to require login to access a view.
    Unless in Testing mode
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the app is not in TESTING mode and the user is anonymous
        if not app.config.get('TESTING', False) and current_user.is_anonymous:
            # If so, redirect to the login page
            return redirect(url_for('users.login'))
        # Otherwise, call the original function
        return f(*args, **kwargs)

    return decorated_function


# Import blueprints
from admin.views import admin_blueprint
from quiz.views import quiz_blueprint
from users.views import users_blueprint
from forecast.forecast import forecast_bp
from search.views import search_blueprint
from map.map import map_bp

# Register the blueprints with the Flask application
app.register_blueprint(forecast_bp)
app.register_blueprint(map_bp)
app.register_blueprint(admin_blueprint)
app.register_blueprint(quiz_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(search_blueprint)

# Initialize the login manager
login_manager = LoginManager()
# Set the login view for the login manager
login_manager.login_view = 'users.login'
# Attach the login manager to the Flask app
login_manager.init_app(app)

from dbSetup import User


# Define the user loader callback for the login manager
@login_manager.user_loader
def load_user(id):
    # Return the user object for the given user ID
    return User.query.get(int(id))


# Error handler for 400 Bad Request
@app.errorhandler(400)
def bad_request(error):
    return render_template('400.html'), 400


# Error handler for 403 Forbidden
@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403


# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server(error):
    return render_template('500.html'), 500


# Error handler for 503 Service Unavailable
@app.errorhandler(503)
def service_unavailable(error):
    return render_template('503.html'), 503


if __name__ == '__main__':
    app.run(debug=True)
