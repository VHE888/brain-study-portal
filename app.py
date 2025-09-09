from flask import Flask, render_template, request

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
    """
    Fetches publications from the database and renders the studies page.
    Now includes logic to filter results based on user selection.
    """
    # 1. Get filter choices from the URL query parameters (e.g., /studies?species_id=1)
    selected_species_id = request.args.get('species_id', type=int)
    selected_region_id = request.args.get('region_id', type=int)

    # 2. Start with a base query for all publications
    query = Publication.query

    # 3. Conditionally add filters to the query if a user made a selection
    if selected_species_id:
        # Join publications with datasets and filter by the selected species ID
        query = query.join(Publication.datasets).filter(Dataset.sid == selected_species_id)

    if selected_region_id:
        # Join through datasets and the association table to filter by region ID
        query = query.join(Publication.datasets).join(Dataset.regions).filter(Region.rid == selected_region_id)

    # 4. Execute the final query, ordering by date
    filtered_publications = query.order_by(Publication.publication_date.desc()).all()

    # 5. Fetch all species and regions to populate the filter dropdowns dynamically
    all_species = Species.query.order_by(Species.species_name).all()
    all_regions = Region.query.order_by(Region.brain_region_name).all()

    # 6. Render the template, passing all the necessary data
    return render_template(
        'studies.html',
        publications=filtered_publications,
        all_species=all_species,
        all_regions=all_regions,
        selected_species_id=selected_species_id,
        selected_region_id=selected_region_id
    )

@app.route('/help')
def help():
    """Renders the help page."""
    return render_template('help.html')



# --- MAIN EXECUTION BLOCK ---
# This code runs when you execute 'python app.py'
if __name__ == '__main__':
    # Starts the Flask development server.
    app.run(debug=True, host='0.0.0.0', port=5001)