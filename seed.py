import json
from datetime import datetime
from app import app
from models import db, Publication, Dataset, Species, Region

def get_or_create(session, model, **kwargs):
    """
    Checks if an instance of a model exists in the database.
    If it exists, it returns the instance.
    If it does not exist, it creates a new instance and returns it.
    This is useful for lookup tables like Species and Region to avoid duplicates.
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

def seed_database():
    """
    Reads publication data from seed_data.json and populates the database.
    This is scalable and idempotent for the lookup tables (Species, Region).
    """
    with app.app_context():
        # Optional: Decide if you want to wipe the db every time.
        # For production, you might want to only add new data.
        print("Dropping all tables to start fresh...")
        db.drop_all()
        print("Creating all tables based on models...")
        db.create_all()

        # Load the data from the JSON file
        try:
            with open('seed_data.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("Error: seed_data.json not found. Aborting.")
            return

        print(f"Found {len(data)} publications in seed_data.json. Seeding database...")

        for pub_data in data:
            # Create the Publication object
            publication = Publication(
                title=pub_data['title'],
                journal=pub_data['journal'],
                publication_date=datetime.strptime(pub_data['publication_date'], '%Y-%m-%d').date()
            )
            db.session.add(publication)
            db.session.commit() # Commit to get the PID for linking datasets

            # Create associated datasets
            for ds_data in pub_data.get('datasets', []):
                # Use get_or_create for species to avoid duplicates
                species = get_or_create(db.session, Species, species_name=ds_data['species'])

                # Use get_or_create for each region
                region_objects = []
                for region_name in ds_data.get('regions', []):
                    region = get_or_create(db.session, Region, brain_region_name=region_name)
                    region_objects.append(region)

                # Create the Dataset object and link everything
                dataset = Dataset(
                    url=ds_data['url'],
                    publication=publication,
                    species=species,
                    regions=region_objects
                )
                db.session.add(dataset)

        # Final commit to save all the new datasets
        db.session.commit()
        print("Database seeding complete.")

if __name__ == '__main__':
    seed_database()