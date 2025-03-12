'''
The website package for the Weather Application.

This package initializes the Flask application and includes the routes,
configuration, and other modules required to run the weather application.
It integrates with the OpenWeather API to fetch and display current weather
and forecast data.
'''

from flask import Flask
from website.routes import main

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    app.register_blueprint(main)

    return app