import requests


def make_request(method: str, url: str, req_body: dict, headers: dict) -> dict:
    """
    Make a request to the API.

    :param method: The HTTP method to be used
    :param url: The URL to be validated
    :param req_body: Sample payload to be sent to the API
    :param headers: Headers to be sent with the request
    :return: The response from the API
    """
    print(
        f"Making a {method} request to {url} with headers {headers} and body {req_body}")
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, json=req_body, headers=headers)
    elif method == "PUT":
        response = requests.put(url, json=req_body, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    else:
        raise Exception("Invalid HTTP method")

    return {
        "status_code": response.status_code,
        "body": response.json() if response.headers.get("Content-Type").startswith("application/json") else response.text,
        "headers": dict(response.headers)
    }
