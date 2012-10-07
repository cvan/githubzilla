#class Settings(dict):
#    __getattr__, __setattr__ = dict.get, dict.__setitem__


#settings = Settings()
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = None
REDIS_PASS = None

GH_URL = 'https://github.com'
GH_DEFAULT_USER = 'mozilla'
GH_DEFAULT_REPO = 'zamboni'
GH_SEARCH_URL = GH_URL + '/%(user)s/%(repo)s/search?q=%(bugs)s&choice=grep'

BZ_FIELDS = ('id,assigned_to,priority,summary,status,last_change_time,'
             'target_milestone,whiteboard')
BZ_SEARCH_URL = ('https://api-dev.bugzilla.mozilla.org/latest/bug?'
                 'include_fields=%(fields)s&quicksearch=%(qs)s')
# Example:
# ALL :marketplace assignee:cvan|assignee:mattbasta target_milestone:2012-09-27
BZ_QS = 'ALL :%(product)s %(assignees)s target_milestone:%(milestone)s'

BZ_DEFAULT_PRODUCT = 'marketplace'
BZ_DEFAULT_MILESTONE = '2012-10-11'
