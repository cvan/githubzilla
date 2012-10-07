#!/usr/bin/env python

import sys
sys.path.append('..')

from services import *


# Index stuff based on week/milestone.
#print redis.delete('milestones')
#print redis.sadd('milestones', '2012-10-04')
#print redis.sadd('milestones', '2012-10-11')
milestones = list(redis.smembers('milestones'))
milestone = milestones[0]
print milestone


# Set users. (This should happen in the web view.)
#print redis.delete('users')
# users = ('cvan', 'andy', 'kumar')
#users = zip(users, (0,) * len(users))
#print redis.sadd('users', *users)


# Get users.
print redis.smembers('users')



# TODO: ZINCRBY myzset 2 "one"
# for each user for each week.
