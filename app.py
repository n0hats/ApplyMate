import configparser
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import re
import os
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from PyPDF2 import PdfReader
from datetime import datetime, timezone
from sqlalchemy import event
from build.config import Config

# Download NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)
app.config.from_object(Config)


# Set secret key for session management and flashing messages
app.secret_key = os.urandom(24)  # or a manually set unique secret key
entry_name = 'Uploaded Resume'

# Load configuration from INI file
config = configparser.ConfigParser()

# Initialize the database with Flask app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Resumes model
class Resumes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))  # Updated to timezone-aware UTC)
    resume_hash = db.Column(db.String(64), nullable=False)  # SHA-256 hash is 64 characters long
    resume_text = db.Column(db.Text, nullable=False)

    def generate_resume_hash(self):
        """Generates a SHA-256 hash of the resume_text."""
        return hashlib.sha256(self.resume_text.encode('utf-8')).hexdigest()


@event.listens_for(Resumes, 'before_insert')
def before_insert_listener(mapper, connection, target):
    target.resume_hash = target.generate_resume_hash()

@event.listens_for(Resumes, 'before_update')
def before_update_listener(mapper, connection, target):
    target.resume_hash = target.generate_resume_hash()

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

# Define the clean_text function
def clean_text(text):
    # Remove special characters
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
    return text

# Define the HTML template
html_template = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Resume Upload</title>
  </head>
  <body>
    <h1>Upload Resume</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="resume">
      <input type="submit" value="Upload">
    </form>
    {% if cleaned_text %}
    <h2>Cleaned Resume Text</h2>
    <pre>{{ cleaned_text }}</pre>
    <form method="post" action="/approve">
      <input type="hidden" name="cleaned_text" value="{{ cleaned_text }}">
      <input type="submit" value="Approve">
    </form>
    {% endif %}
  </body>
</html>
"""

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

@app.route('/', methods=['GET', 'POST'])
def upload_resume():
    global entry_name
    if request.method == 'POST':
        file = request.files['resume']
        entry_name = file.filename
        if file:
            if file.filename.endswith('.pdf'):
                text = extract_text_from_pdf(file)
            else:
                text = file.read().decode('utf-8')
            cleaned_text = clean_text(text)
            return render_template_string(html_template, cleaned_text=cleaned_text)
    return render_template_string(html_template)

@app.route('/approve', methods=['POST'])
def approve_resume():
    global entry_name
    cleaned_text = request.form['cleaned_text']
    new_resume = Resumes(name=entry_name, resume_text=cleaned_text)
    db.session.add(new_resume)
    db.session.commit()
    flash(f"Resume text approved for {entry_name} and saved to the database!")
    return redirect(url_for('index'))

# Route for the homepage
@app.route('/home')
def index():
    # Render a simple template or return a string
    entries = Resumes.query.all()
    return render_template('index.html', entries=entries)

# Example route to add data to the database (optional)
@app.route('/add/<name>')
def add_name(name):
    new_entry = Resumes(name=name)
    db.session.add(new_entry)
    db.session.commit()
    return f"Added {name} to the database!"

# Route to delete a resume
@app.route('/delete/<int:id>')
def delete_resume(id):
    resume_to_delete = Resumes.query.get_or_404(id)
    db.session.delete(resume_to_delete)
    db.session.commit()
    return f"Deleted resume with ID {id} from the database!"

# Main section to run the app
if __name__ == '__main__':
    # Run the Flask application
    app.run()
