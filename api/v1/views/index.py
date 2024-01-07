#!/usr/bin/python3
"""
Index blueprint definition
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.get("/status")
def get_status():
    """Gets the API status"""
    return jsonify(status="OK")
