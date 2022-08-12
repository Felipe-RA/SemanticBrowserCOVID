from tokenize import String
import requests
import json

def get_api_json(api_url: String):

    """
    A simple method to do a GET request from an API

    Returns the response as a JSON
    """

    try:
        response = requests.get(api_url)
        print("API latency time: ", response.elapsed.total_seconds(),"secs")

    except requests.exceptions.Timeout:
        print("Request timed out. Maybe be a connection error")
    except requests.exceptions.TooManyRedirects:
        print("The url used in your request has a problem. ")
    except requests.exceptions.RequestException as e:
        print("Some catastrophic error ocurred, ending operations...")
        raise SystemExit(e)

    return response.json()
