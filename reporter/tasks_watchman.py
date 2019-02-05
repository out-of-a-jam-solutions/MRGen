# sheldon woodward
# jan 8, 2019

import math
import os
import requests

from celery import shared_task
from celery.task import chord
from rest_framework import status

from reporter import api_urls


@shared_task
def watchman_update_client(group_id, api_key=str()):
    """
    Starts the Watchman update tasks for a specific Watchman group. This is the main task to start the update process
    for Watchman information. Example:

        results = tasks.watchman_update_client(group_id)
        res = result_from_tuple(results.get())
        return response.Response(res.get())

    :param group_id: The group ID to use in requesting a list of computers.
    :param api_key: An optional API key to use if no WATCHMAN_API_KEY environment variable is set.
    :return: Returns an AsyncResult object tuple containing another AsyncResult with the results of
    queue_watchman_computers_requests(). Reference the above example to decode the results.
    """
    # get watchman group information about number of computers
    results_per_page = 100
    return (get_watchman_group.s(group_id, api_key) |
            determine_computer_request_num.s(results_per_page) |
            queue_watchman_computers_requests.s(results_per_page, group_id, api_key))()


@shared_task
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
    return req.json()


@shared_task
def determine_computer_request_num(json, per_page):
    """
    Determines the number of requests to make to retrieve all computers.

    :param json: A JSON formatted dictionary containing the results of a Watchman '/groups' request
    :param per_page: The number of computers that are displayed per page in a Watchman '/computers' request.
    :return: Returns an integer value with the number of requests that should be made to the Watchman computers API.
    """
    return math.ceil(json['visible_computer_count'] / per_page)


@shared_task
def queue_watchman_computers_requests(request_num, per_page, group_id, api_key=str()):
    """
    Creates a Celery chord of requests and concatenates the results into one JSON formatted dictionary.

    :param request_num: The number of requests to make to get all results from the Watchman '/computers' endpoint.
    :param per_page: The number of computers to include per page. Watchman limits this to 100.
    :param group_id: The group ID to use in requesting a list of computers.
    :param api_key: An optional API key to use if no WATCHMAN_API_KEY environment variable is set.
    :return: Returns a JSON formatted dictionary containing the concatenated results from the multiple requests.
    """
    # put the the multiple computer requests in a group
    computers_chord = chord(get_watchman_computers.s(page=page,
                                                     per_page=per_page,
                                                     group_id=group_id,
                                                     api_key=api_key)
                            for page in range(1, request_num + 1))
    return computers_chord(combine_watchman_computer_results.subtask())


@shared_task
def get_watchman_computers(page=None, per_page=None, group_id=None, api_key=str()):
    """
    Queries the Watchman Monitoring '/computers' endpoint with a group ID to retrieve a list of all monitored
    computers along with any warnings that these computers currently have.

    :param page: The page number for pagination.
    :param per_page: The number of computers per page, max of 100.
    :param group_id: The group ID of computers to query.
    :param api_key: An optional API key to use if no WATCHMAN_API_KEY environment variable is set.
    :return: Returns the request response.
    """
    # construct query parameters
    query_params = {
        'api_key': os.getenv('WATCHMAN_API_KEY', api_key),
        'expand[]': 'plugin_results',
    }
    if page is not None:
        query_params['page'] = page
    if per_page is not None:
        query_params['per_page'] = per_page
    if group_id is not None:
        query_params['group_id'] = group_id
    # make request
    url = api_urls.watchman['computers']
    req = requests.get(url, query_params)
    # return results or error
    if req.status_code != status.HTTP_200_OK:
        raise Exception(f'request returned status code {req.status_code}')
    return req.json()


@shared_task
def combine_watchman_computer_results(*results):
    """
    The callback task used in queue_watchman_computers_requests() to concatenate all the results from Watchman the
    '/computers' request.

    :param results: List of JSON formatted dictionary results to concatenate.
    :return: Returns a single JSON formatted dictionary of Watchman '/computers' endpoint results.
    """
    new_results = list()
    for r in results[0]:
        new_results += r
    return new_results
