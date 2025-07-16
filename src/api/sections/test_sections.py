import json
import allure
from faker import Faker
import pytest
from config.config import url_base, headers
from helper.rest_client import RestClient
from helper.validate_response import ValidateResponse
from utils.influxdb_connection import InfluxDBConnection
from utils.logger import get_logger

LOGGER = get_logger(__name__, "DEBUG")


@allure.story("Sections")
@allure.parent_suite("Sections")
class TestSections:
    @classmethod
    def setup_class(cls) -> None:
        """Setup before all tests"""
        # arrange
        LOGGER.info("Test Section Setup Class")
        # set RestClient in the setup
        cls.rest_client = RestClient()
        # use the validation library
        cls.validate = ValidateResponse()
        # use random generator with faker
        cls.faker = Faker()
        # use influxdb_client
        cls.influxdb_client = InfluxDBConnection()

    def setup_method(self) -> None:
        self.response = None

    def teardown_method(self) -> None:
        self.influxdb_client.store_data_influxdb(self.response, "sections")

    @pytest.mark.acceptance
    @pytest.mark.smoke
    @allure.title("Test Create Section")
    @allure.tag("smoke", "acceptance")
    @allure.label("owner", "Joanna Yujra")
    def test_create_section(self, test_log_name: None, create_project: str) -> None:
        """Test for create a Section

        Args:
            test_log_name (None): Fixture to log the start and ending of test case
            create_project (str): GID of the project
        """
        url_create_section = f"{url_base}projects/{create_project}/sections"
        LOGGER.debug(f"URL CREATE Section: {url_create_section}")
        # body to create the Section
        section_body = {
            "data": {
                "name": f"Auto Section {self.faker.word()}"
            }
        }
        # call POST endpoint (act)
        self.response = self.rest_client.send_request("POST",
                                                 url=url_create_section,
                                                 headers=headers,
                                                 body=section_body)
        LOGGER.debug(f"RESPONSE: {json.dumps(self.response, indent=4)}")
        # assertion
        self.validate.validate_response(self.response, "create_section")

    @pytest.mark.acceptance
    @allure.title("Test Get Section")
    @allure.tag("acceptance")
    @allure.label("owner", "Joanna Yujra")
    def test_get_section(self, create_section: str, test_log_name: None) -> None:
        """Test for get a Section

        Args:
            create_section (str): Section GID
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for GET Section
        url_get_section = f"{url_base}sections/{create_section}"
        LOGGER.debug(f"URL GET Section: {url_get_section}")
        # call GET endpoint (act)
        self.response = self.rest_client.send_request("GET",
                                                 url=url_get_section,
                                                 headers=headers)
        LOGGER.debug(f"RESPONSE: {json.dumps(self.response, indent=4)}")
        # assertion
        self.validate.validate_response(self.response, "get_section")

    @pytest.mark.acceptance
    @allure.title("Test Update Section")
    @allure.tag("acceptance")
    @allure.label("owner", "Joanna Yujra")
    def test_update_section(self, create_section: str, test_log_name: None) -> None:
        """Test for update a Section

        Args:
            create_section (str): Contains GID of the Section and GID of the Project
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for UPDATE the Section
        url_update_section = f"{url_base}sections/{create_section}"
        LOGGER.debug(f"URL UPDATE Section: {url_update_section}")
        # body to update the Section
        update_section_body = {
            "data": {
                "name": f"Auto Updated {self.faker.word()}"
            }
        }
        # call PUT endpoint (act)
        self.response = self.rest_client.send_request("PUT",
                                                 url=url_update_section,
                                                 headers=headers,
                                                 body=update_section_body)
        LOGGER.debug(f"RESPONSE: {json.dumps(self.response, indent=4)}")
        # assertion
        self.validate.validate_response(self.response, "update_section")

    @pytest.mark.acceptance
    @allure.title("Test Delete Section")
    @allure.tag("acceptance")
    @allure.label("owner", "Joanna Yujra")
    def test_delete_section(self, create_section: str, test_log_name: None) -> None:
        """Test for delete a Section

        Args:
            create_section (str): Contains GID of the Section and GID of the Project
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for DELETE Section
        url_delete_section = f"{url_base}sections/{create_section}"
        LOGGER.debug(f"URL DELETE Section: {url_delete_section}")
        # call DELETE endpoint (act)
        self.response = self.rest_client.send_request("DELETE",
                                                 url=url_delete_section,
                                                 headers=headers)
        LOGGER.debug(f"RESPONSE: {json.dumps(self.response, indent=4)}")
        # assertion
        self.validate.validate_response(self.response, "delete_section")

    @pytest.mark.functional
    @allure.title("Test verify error message when updating a section with different string section GID")
    @allure.tag("functional", "negative")
    @allure.label("owner", "Joanna Yujra")
    @pytest.mark.parametrize("section_gid", ["InvalidGID", "!#$%&/()=?¡"])
    def test_update_section_using_different_string_section_gid_negative(
        self, test_log_name: None, section_gid: str
    ) -> None:
        """Test for update a section using different string inputs for section GID

        Args:
            test_log_name (None): Fixture to log the start and ending of test case
            section_gid (str): list of possible string section GIDs
        """
        # url for UPDATE the Section
        url_update_section = f"{url_base}sections/{section_gid}"
        LOGGER.debug(f"URL UPDATE Section: {url_update_section}")
        # body to update the Section
        update_section_body = {
            "data": {
                "name": f"Auto Error Updated {self.faker.word()}"
            }
        }
        # call PUT endpoint (act)
        self.response = self.rest_client.send_request("PUT",
                                                 url=url_update_section,
                                                 headers=headers,
                                                 body=update_section_body)
        LOGGER.debug(f"RESPONSE: {json.dumps(self.response, indent=4)}")
        # assertion
        self.validate.validate_response(self.response, "update_section_with_string_section_gid")

    @classmethod
    def teardown_class(cls) -> None:
        """Close influx connection after all tests"""
        cls.influxdb_client.close()
