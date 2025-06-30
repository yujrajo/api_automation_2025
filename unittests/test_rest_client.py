import json
import unittest
from helper.rest_client import RestClient
from utils.logger import get_logger
from config.config import url_base,headers

LOGGER = get_logger(__name__, "DEBUG")

class TestRestClient(unittest.TestCase):

    def test_get_rest_client(self):
        LOGGER.info("Test Rest Client")
        rest_client=RestClient()
        response=rest_client.send_request("GET", url=url_base+"projects", headers=headers)
        LOGGER.info(json.dumps(response, indent=4))

    def test_get_rest_client_nonexistent_endpoint_negative(self):
        LOGGER.info("Test Rest Client Negative Nonexistent URL 'project'")
        rest_client=RestClient()
        response=rest_client.send_request("GET", url=url_base+"project", headers=headers)
        LOGGER.info(json.dumps(response, indent=4))
    # better negative test with nonexistent gid
    def test_get_rest_client_nonexistent_gid_negative(self):
        LOGGER.info("Test Rest Client Negative Nonexistent GID")
        rest_client=RestClient()
        response=rest_client.send_request("GET", url=url_base+"projects/12345", headers=headers)
        LOGGER.info(json.dumps(response, indent=4))

    def test_get_rest_client_call_create_project_without_body_negative(self):
        LOGGER.info("Test Rest Client Negative Create Project without body")
        rest_client=RestClient()
        response=rest_client.send_request("POST", url=url_base+"projects", headers=headers)
        LOGGER.info(json.dumps(response, indent=4))
