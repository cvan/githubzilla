import hashlib
import json
import sys
import urllib

import requests
from pyquery import PyQuery as pq

sys.path.append('services')
import services
import services.bugs

from flask import Flask, jsonify, render_template, request

app = Flask(__name__, static_folder='media')


@app.route('/', methods=['GET', 'POST'])
def home():
    return watch()


@app.route('/watch', methods=['GET', 'POST'])
def watch():
    milestone = request.form.get('bz_milestone')

    if request.method == 'POST':
        product = request.form.get('bz_product')
        services.redis.sadd('products', product)

        milestone = request.form.get('bz_milestone')
        services.redis.sadd('products:%s:milestones' % product, milestone)

        gh_users = request.form.getlist('gh_users')
        for user in gh_users:
            print services.redis.sadd('products:%s:milestones:%s:gh_users' % (product, milestone), user)

        # TODO: Map bz_users to gh_users.
        bz_users = request.form.getlist('bz_users')
        for user in bz_users:
            print services.redis.sadd('products:%s:milestones:%s:bz_users' % (product, milestone), user)

    # TODO: Use redis queue for this.
    bugs = services.bugs.get_all(build=request.method == 'POST')

    return render_template('watch.html', **{
        'bugs': bugs
    })


@app.template_filter('gravatar_url')
def gravatar_url(email, size=40):
    return 'http://www.gravatar.com/avatar/%s?%s' % (
        hashlib.md5(email.lower()).hexdigest(),
        urllib.urlencode({'d': 'mm', 's': str(size)}))


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        port = 4000
    app.run(debug=True, port=port)
