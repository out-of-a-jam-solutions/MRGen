# sheldon woodward
# jan 8, 2019

import os
import requests

from rest_framework import status

from MRGen.celery import app
from reporter import api_urls


@app.task
def get_watchman_group(group_id, api_key=str()):
    """
    Queries the Watchman Monitoring '/groups/<group_id>' endpoint with a group ID to retrieve information pertaining
    to the group.

    :param group_id: The group ID of the group to query.
    :param api_key: An optional API key to use if no WATCHMAN_API_KEY environment variable is set.
    :return: Returns the request response.
    """
    # construct query parameters
    query_params = {
        'api_key': os.getenv('WATCHMAN_API_KEY', api_key)
    }
    # make request
    url = api_urls.watchman['group'].format(group_id)
    req = requests.get(url, query_params)
    # return results or error
    if req.status_code != status.HTTP_200_OK:
        raise Exception(f'request returned status code {req.status_code}')
    return req


@app.task
def get_watchman_computers(group_id=None, api_key=str()):
    """
    Queries the Watchman Monitoring '/computers' endpoint with a group ID to retrieve a list of all monitored
    computers along with any warnings that these computers currently have.

    :param group_id: The group ID of computers to query.
    :param api_key: An optional API key to use if no WATCHMAN_API_KEY environment variable is set.
    :return: Returns the request response.
    """
    # construct query parameters
    query_params = {
        'api_key': os.getenv('WATCHMAN_API_KEY', api_key),
        'expand[]': 'plugin_results',
    }
    if group_id is not None:
        query_params['group_id'] = group_id
    # make request
    url = api_urls.watchman['computers']
    req = requests.get(url, query_params)
    # return results or error
    if req.status_code != status.HTTP_200_OK:
        raise Exception(f'request returned status code {req.status_code}')
    return req
