# server/app.py
from flask import Flask
from flask_migrate import Migrate
from models import db

# Initialize Flask app
app = Flask(__name__)
# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)
# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Basic route for testing
@app.route('/')
def index():
    return '<h1>Flask SQLAlchemy Lab 2</h1>'

# Run the app
if __name__ == '__main__':
    app.run(port=5555, debug=True)