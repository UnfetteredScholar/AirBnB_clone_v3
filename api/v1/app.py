#!/usr/bin/python3
"""
Defines the Flask API
"""
from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(exception):
    """The Flask app/request context end event listener"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """
    404 Error handler
    """
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
