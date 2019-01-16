# sheldon woodward
# jan 11, 2019

"""
API base URLs for use in requests.
"""

# watchman URLs
watchman = {
    'base': 'https://outofajam.monitoringclient.com/v2.5/{}'
}
watchman['group'] = watchman['base'].format('groups/{}')
watchman['groups'] = watchman['base'].format('groups')
watchman['computer'] = watchman['base'].format('computers/{}')
watchman['computers'] = watchman['base'].format('computers')
