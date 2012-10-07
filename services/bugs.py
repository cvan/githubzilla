#!/usr/bin/env python

import json
import sys
sys.path.append('..')

import requests

from services import *


# Set products.
#print redis.delete('products')

# print redis.sadd('products', 'marketplace')
# print redis.sadd('products', 'addons')
products = list(redis.smembers('products'))
# print products


# # Set milestones.
# print redis.delete('products:marketplace')
# print redis.delete('products:addons')
# for product in products:
#     print redis.delete('products:%s:milestones' % product)
#     print redis.sadd('products:%s:milestones' % product, '2012-10-04')
#     print redis.sadd('products:%s:milestones' % product, '2012-10-11')

#     print redis.sadd('products:%s:milestones:%s:users' % (product, '2012-10-04'), 'cvan@mozilla.com')
#     print redis.sadd('products:%s:milestones:%s:users' % (product, '2012-10-04'), 'amckay@mozilla.com')
#     print redis.sadd('products:%s:milestones:%s:users' % (product, '2012-10-04'), 'kumar.mcmillan@gmail.com')
#     print redis.sadd('products:%s:milestones:%s:users' % (product, '2012-10-04'), 'mattbasta@gmail.com')

#     print redis.sadd('products:%s:milestones:%s:users' % (product, '2012-10-11'), 'cvan@mozilla.com')
#     print redis.sadd('products:%s:milestones:%s:users' % (product, '2012-10-11'), 'amckay@mozilla.com')
#     print redis.sadd('products:%s:milestones:%s:users' % (product, '2012-10-11'), 'kumar.mcmillan@gmail.com')


# print
# print



def get_milestone_bugs(product, milestone, users):
    assignees = '|'.join(map(lambda x: 'assignee:%s' % x, users))

    bz_qs = settings.BZ_QS % {'product': product,
                              'assignees': assignees,
                              'milestone': milestone}
    url = settings.BZ_SEARCH_URL % {'fields': settings.BZ_FIELDS, 'qs': bz_qs}
    print '-------', bz_qs, '-------'
    r = requests.get(url, headers={'Accept': 'application/json'})
    return json.loads(r.content)


def set_milestone_bugs(product, milestone, user, bugs):
    for bug in bugs['bugs']:
        print redis.sadd('products:%s:milestones:%s:users:%s:bugs' % (product, milestone, user), json.dumps(bug))


def get_all(build=False):
    d = {}
    products = list(redis.smembers('products'))
    for product in products:
        milestones = list(redis.smembers('products:%s:milestones' % product))
        d[product] = {}
        print
        print product
        print '-' * 5
        for milestone in milestones:
            users = list(redis.smembers('products:%s:milestones:%s:users' % (product, milestone)))
            d[product][milestone] = {}
            print
            print '\t', milestone
            print '\t', '-' * 5
            for user in users:
                print '\t', '\t', user
                if build:
                    bugs = get_milestone_bugs(product, milestone, [user])
                    set_milestone_bugs(product, milestone, user, bugs)
                bugs = list(redis.smembers('products:%s:milestones:%s:users:%s:bugs' % (product, milestone, user)))
                d[product][milestone][user] = map(json.loads, bugs)
    return d


if __name__ == '__main__':
    try:
        build = sys.argv[1] == 'build'
    except IndexError:
        build = False
    get_all(build=build)
