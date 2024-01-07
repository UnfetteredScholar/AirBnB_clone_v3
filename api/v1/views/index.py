#!/usr/bin/python3
"""
Index blueprint definition
"""
from api.v1.views import app_views
from flask import jsonify


# @app_views.get("/status")
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Gets the API status"""
    return jsonify(status="OK")
