import requests


# ----------------------------------------------------------------------------------------------------------------------
# Generic function to http requests
def request_call(url, status_code):
    response = None
    try:
        response = requests.get(url)
        if response.status_code == status_code:
            return response
        else:
            raise requests.exceptions.RequestException("the status code does not matched, check your url")
    except requests.exceptions.RequestException as e:
        return e
