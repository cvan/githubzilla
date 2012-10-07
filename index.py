import json
import sys

import requests
from pyquery import PyQuery as pq

sys.path.append('services')
import services.bugs

from flask import Flask, jsonify, render_template, request

app = Flask(__name__, static_folder='media')


@app.route('/', methods=['GET', 'POST'])
def home():
    return watch()


@app.route('/watch', methods=['GET', 'POST'])
def watch():
    bugs = services.bugs.get_all()
    return render_template('watch.html', **{
        'bugs': bugs
    })



if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        port = 4000
    app.run(debug=True, port=port)
