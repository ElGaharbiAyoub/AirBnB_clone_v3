#!/usr/bin/python3
"""app api"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Error 404"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def closer(err):
    """Closes storage session"""
    storage.close()


if __name__ == "__main__":
    """ Main Function """
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
