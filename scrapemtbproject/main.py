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
            "displayFieldName": "<displayFieldName>",
            "fieldAliases": {
                "<fieldName1>": "<fieldAlias1>",
                "<fieldName2>": "<fieldAlias2>"
            },
            "geometryType": "<geometryType>",
            "hasZ": True,
            "hasM": False,
            "spatialReference": {'wkid': 3857},
            "fields": [
                {
                    "name": "diff",
                    "type": "STRING",
                    "alias": "Difficulty"
                },
                {
                    "name": "<field2>",
                    "type": "<field2Type>",
                    "alias": "<field2Alias>"
                }
            ],
            "features": []
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
