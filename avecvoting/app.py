from flask import render_template, session, jsonify,request
from flask_cors import CORS
from __init__ import app

from config import host, port, debug
import manager
import voter
import voterWe
import voterAvec
import json
import user
CORS(app)

if __name__ == "__main__":

    app.logger.info(f"starting server at {host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)


