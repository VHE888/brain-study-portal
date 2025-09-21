# Brain Study Portal

## Database Website to Help Facilitate Alzheimer’s Disease Research

This is a lightweight Flask web application designed to support researchers by providing a portal to browse scientific publications and related datasets. It is particularly aimed at facilitating studies in Alzheimer’s disease and brain-related research.

The application uses SQLAlchemy to manage a relational database with four core tables: **Publication**, **Dataset**, **Species**, and **Region**. Each publication can link to multiple datasets, which are associated with specific species and brain regions. Users can explore the database and filter publications dynamically by species and brain region through the web interface.

### Features
- **Home Page (`/`)**: Welcome page introducing the portal.  
- **Studies Page (`/studies`)**: Displays publications, with filtering options for species and brain region.  
- **Help Page (`/help`)**: Provides guidance on how to use the portal.  

### Technical Details
- Configuration (e.g., database connection string, secret key) is stored in `instance/config.py`.  
- HTML templates are organized in the `templates/` folder.  
- The application runs on port **5001** by default and can be launched with `python app.py`.  

This project provides a foundation for managing and exploring brain-related publication datasets and can be extended with new data types, search features, and visualizations as research needs evolve.
