from flask import Flask, render_template

# Import the db object and models from models.py
from models import db, Publication, Dataset, Species, Region

# --- APP SETUP ---
app = Flask(__name__)

# Load configuration from the separate config.py file
app.config.from_pyfile('instance/config.py')

# Initialize the app with the database object from models.py.
db.init_app(app)


# --- APPLICATION ROUTES ---
# These functions define what content is served for each URL.
@app.route('/')
def home():
    """Renders the home page."""
    # This route will show a simple welcome page.
    return render_template('index.html', page='home')

@app.route('/studies')
def studies():
    """Renders the studies page, fetching all publications from the database."""
    all_publications = Publication.query.order_by(Publication.publication_date.desc()).all()
    return render_template('studies.html', publications=all_publications)



# --- MAIN EXECUTION BLOCK ---
# This code runs when you execute 'python app.py'
if __name__ == '__main__':
    # Starts the Flask development server.
    app.run(debug=True, host='0.0.0.0', port=5001)