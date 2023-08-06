import json

# ----------------------------------------------------------------------------------------------------------------------
# Obtaining a list of universities and related data on them
import requests
from requests_utils import request_call


def get_universities(url):
    result = request_call(url, 200)
    if isinstance(result, requests.exceptions.RequestException):
        return result
    content = result.content
    print(result)
    my_json = content.decode('utf8').replace("'", '"')
    # Load the JSON to a Python list
    universities_list = json.loads(my_json)
    return universities_list

# universities_url = 'http://universities.hipolabs.com/search?country=Israel'
# universities = get_universities(universities_url)
# print(universities)
