from app import app
from flask import jsonify, Response, render_template
import json

@app.route('/')
def index():
    return render_template('build/index.html')

