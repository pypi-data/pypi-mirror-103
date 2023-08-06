import requests
from pyparliment import baseURL
import json
from shapely.geometry import shape


def all_by_id(id_number):
    pass


def synopsis_by_id(id_number):
    pass


def representation_by_id(id_number):
    pass


def geometry_by_id(id_number):

    end_point = "Location/Constituency/"

    url = baseURL + end_point + str(id_number) + "/Geometry"

    response = requests.request("GET", url)

    json_response = json.loads(json.loads(response.text)["value"])

    if json_response["type"] == "Polygon":
        area = shape(json_response)
    elif json_response["type"] == "MultiPolygon":
        area = shape(json_response)
    else:
        area = 0

    return area
