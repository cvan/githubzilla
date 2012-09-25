import json
import sys

import requests
from pyquery import PyQuery as pq

from flask import Flask, jsonify, render_template, request

app = Flask(__name__, static_folder='media')

GH_URL = 'https://github.com'
GH_DEFAULT_USER = 'mozilla'
GH_DEFAULT_REPO = 'zamboni'
GH_SEARCH_URL = GH_URL + '/%(user)s/%(repo)s/search?q=%(bugs)s&choice=grep'

BZ_FIELDS = ('id,assigned_to,priority,summary,status,last_change_time,'
             'target_milestone,whiteboard')
BZ_SEARCH_URL = ('https://api-dev.bugzilla.mozilla.org/latest/bug?'
                 'include_fields=%(fields)s&quicksearch=%(qs)s')
# Example:
# :marketplace assignee:cvan|assignee:mattbasta target_milestone:2012-09-27
BZ_QS = ':%(product)s %(assignees)s target_milestone:%(milestone)s'

BZ_DEFAULT_PRODUCT = 'marketplace'
BZ_DEFAULT_MILESTONE = '2012-09-27'


@app.route('/', methods=['GET', 'POST'])
def home():
    return watch()


@app.route('/watch', methods=['GET', 'POST'])
def watch():
    return render_template('watch.html')


@app.route('/commits', methods=['GET', 'POST'])
def commits():
    bz_product = request.form.get('bz_product', BZ_DEFAULT_PRODUCT)
    bz_milestone = request.form.get('bz_milestone', BZ_DEFAULT_MILESTONE)

    gh_user = request.form.get('user', GH_DEFAULT_USER)
    gh_repo = request.form.get('repo', GH_DEFAULT_REPO)
    # NOTE: Unfortunately GitHub isn't nice enough to let us search this.
    #tree = request.form.get('tree', '')

    gh_users = request.args.getlist('gh_users')
    bz_users = request.args.getlist('bz_users')

    bz_assignees = '|'.join(map(lambda x: 'assignee:%s' % x, bz_users))

    bz_qs = BZ_QS % {'product': bz_product,
                     'assignees': bz_assignees,
                     'milestone': bz_milestone}
    r = requests.get(BZ_SEARCH_URL % {'fields': BZ_FIELDS, 'qs': bz_qs},
                     headers={'Accept': 'application/json'})
    #return jsonify(json.loads(r.content))
    bz_content = json.loads(r.content)


    # GitHub's search uses pipes for OR queries.
    bugs = '|'.join(str(bug['id']) for bug in bz_content['bugs'])

    r = requests.get(GH_SEARCH_URL % {'user': gh_user, 'repo': gh_repo,
                                      'bugs': bugs},
                     headers={'Accept': 'application/json'})
    content = pq(r.content)('.commit-group')

    # Because this is easy.
    content = (content.html().replace('href="/', 'href="%s/' % GH_URL)
                             .replace("href='/", "href='%s/" % GH_URL))

    # return jsonify({
    #     'content': r.content
    # })

    # These are the fixed bugs in this milestone!
    # TODO: We should make sure that the bug states reopened!

    # TODO: Do some analysis and return the ones not fixed too.
    return content


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        port = 4000
    app.run(debug=True, port=port)
