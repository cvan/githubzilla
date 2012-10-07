#!/usr/bin/env python

import sys
sys.path.append('..')

import requests

from services import *


# Set milestones.
#print redis.delete('milestones')
#print redis.sadd('milestones', '2012-10-04')
#print redis.sadd('milestones', '2012-10-11')
milestones = list(redis.smembers('milestones'))

for milestone in milestones:
    print milestone


'''
# DESC -> ASC.
print redis.lrange('milestones', '0', '-1')


bz_product = settings.BZ_DEFAULT_PRODUCT
bz_milestone = settings.BZ_DEFAULT_MILESTONE

gh_user = settings.GH_DEFAULT_USER
gh_repo = settings.GH_DEFAULT_REPO

#gh_users
#bz_users

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
'''
