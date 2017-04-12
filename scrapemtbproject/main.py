# import modules
import requests
import json

# useful variables
urlRoot = 'https://www.mtbproject.com'


# ride object
class Ride:
    # initialize to load all dictionary key/value pairs as properties
    def __init__(self, properties):
        self.__dict__ = properties


# create mtb project feature set
class MtbProjectFeatureSet:
    def __init__(self):
        self.__dict__ = {
            "displayFieldName": "title",
            "hasZ": true,
            "hasM": true,
            "fieldAliases": {
                "OBJECTID": "OBJECTID",
                "id": "ID",
                "title": "Title",
                "diff": "Difficulty",
                "score": "Score",
                "summary": "Abstract",
                "surface": "Surface",
                "isComposite": "Composite",
                "isRace": "Race",
                "isSegment": "Segment",
                "length": "Length",
                "rideTrail": "Ride",
                "SHAPE_Length": "SHAPE_Length"
            },
            "geometryType": "esriGeometryPolyline",
            "spatialReference": {
                "wkid": 102100,
                "latestWkid": 3857,
                "vcsWkid": 115700,
                "latestVcsWkid": 115700
            },
            "fields": [
                {
                    "name": "OBJECTID",
                    "type": "esriFieldTypeOID",
                    "alias": "OBJECTID"
                },
                {
                    "name": "id",
                    "type": "esriFieldTypeSmallInteger",
                    "alias": "ID"
                },
                {
                    "name": "title",
                    "type": "esriFieldTypeString",
                    "alias": "Title",
                    "length": 100
                },
                {
                    "name": "diff",
                    "type": "esriFieldTypeString",
                    "alias": "Difficulty",
                    "length": 50
                },
                {
                    "name": "score",
                    "type": "esriFieldTypeSmallInteger",
                    "alias": "Score"
                },
                {
                    "name": "summary",
                    "type": "esriFieldTypeString",
                    "alias": "Abstract",
                    "length": 5000
                },
                {
                    "name": "surface",
                    "type": "esriFieldTypeString",
                    "alias": "Surface",
                    "length": 50
                },
                {
                    "name": "isComposite",
                    "type": "esriFieldTypeSmallInteger",
                    "alias": "Composite"
                },
                {
                    "name": "isRace",
                    "type": "esriFieldTypeSmallInteger",
                    "alias": "Race"
                },
                {
                    "name": "isSegment",
                    "type": "esriFieldTypeSmallInteger",
                    "alias": "Segment"
                },
                {
                    "name": "length",
                    "type": "esriFieldTypeDouble",
                    "alias": "Length"
                },
                {
                    "name": "rideTrail",
                    "type": "esriFieldTypeSmallInteger",
                    "alias": "Ride"
                },
                {
                    "name": "SHAPE_Length",
                    "type": "esriFieldTypeDouble",
                    "alias": "SHAPE_Length"
                }
            ],
            "features": [
            ]
        }


# create mtbproject scraper
class MtbProjectScraper:
    def __init__(self):

        # create session object instance
        self._session = requests.Session()

        # get the initial cookie to use for subsequent requests
        self._session.cookies = self._session.get(urlRoot).cookies

    def _get_data(self, centroid, geometry_type):
        """
        Get data, both points and lines, for trails within the extent.
        :param centroid: centroid for data retrieval
        :param geometry_type: points or lines 
        :return: JSON formatted data
        """
        # determine correct query parameter geometry
        if geometry_type == 'points':
            level = 'trailDots'
        elif geometry_type == 'lines':
            level = 'trail'
        else:
            raise Exception('either points or lines geometry must be specified')

        # construct the url string
        url = '{}/ajax/map-contents?x={}&y={}&level={}'.format(urlRoot, centroid[0], centroid[1], level)

        # use the local session to make the call and extract the response content
        data = json.loads(self._session.get(url).content.decode('utf-8'))

        # return the data
        return data

    def get_points(self, centroid):
        """
        Get trails point data falling within a bounding box.
        :param centroid: centroid for data retrieval
        :return: 
        """
        data = self._get_data(centroid, 'points')

        return data

    def get_lines(self, centroid):
        """
        Get trails line data falling within a bounding box.
        :param centroid: centroid for data retrieval 
        :return: 
        """
        data = self._get_data(centroid, 'lines')

        return data
