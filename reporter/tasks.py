# sheldon woodward
# jan 8, 2019

import os
import requests

from rest_framework import status

from MRGen.celery import app
from reporter import api_urls


@app.task
def get_computers(watchman_group_id=None, api_key=str()):
    """
    Queries the Watchman Monitoring '/computers' endpoint with a group ID to retrieve a list of all monitored
    computers along with any warnings that these computers currently have.

    :param watchman_group_id: The group ID of computers to query.
    :param api_key: An optional API key to use if no WATCHMAN_API_KEY environment variable is set.
    :return: Returns the request made by the task.
    """
    # construct query parameters
    query_params = {
        'api_key': os.getenv('WATCHMAN_API_KEY', api_key),
        'expand[]': 'plugin_results',
    }
    if watchman_group_id is not None:
        query_params['group_id'] = watchman_group_id
    # make request
    url = api_urls.watchman['base'].format('computers')
    req = requests.get(url, query_params)
    # return results or error
    if req.status_code != status.HTTP_200_OK:
        raise Exception
    return req
