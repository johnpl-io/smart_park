#!/bin/bash
# Run the database population script
python populate.py

# Start the Flask application
python endpoints.py
