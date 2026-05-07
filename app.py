import os
from flask import Flask, redirect, url_for, session
from dotenv import load_dotenv
from extensions import db

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from routes.auth import auth
from routes.camera import camera
from routes.logs import logs

app.register_blueprint(auth)
app.register_blueprint(camera)
app.register_blueprint(logs)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('camera.dashboard'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
