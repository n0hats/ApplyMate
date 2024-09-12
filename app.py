import configparser
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load configuration from INI file
config = configparser.ConfigParser()

try:
    # Attempt to read the configuration file
    config.read("build/config.ini")

    # Access the database connection string
    app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['conn']

    # Access the environment setting
    app.config['ENV'] = config['environment']['env']

except KeyError as e:
    raise KeyError(f"Missing configuration section or option: {e}")

except Exception as e:
    raise Exception(f"Failed to load configuration: {e}")

# Disable SQLAlchemy event notifications to save resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set DEBUG mode based on environment
if app.config['ENV'] != 'prod':
    app.config['DEBUG'] = True
else:
    app.config['DEBUG'] = False

# Initialize the database with Flask app
db = SQLAlchemy(app)

# Define a simple model (optional)
class Resumes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Route for the homepage
@app.route('/')
def index():
    # Render a simple template or return a string
    entries = Resumes.query.all()
    return render_template('index.html', entries=entries)  # Assuming you have an index.html in your templates folder
    # Alternatively: return "Hello, World!"

# Example route to add data to the database (optional)
@app.route('/add/<name>')
def add_name(name):
    new_entry = Resumes(name=name)
    db.session.add(new_entry)
    db.session.commit()
    return f"Added {name} to the database!"

# Main section to run the app
if __name__ == '__main__':
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Run the Flask application
    app.run()
