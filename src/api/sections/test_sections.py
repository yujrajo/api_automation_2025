import json
import allure
from faker import Faker
import pytest
import requests
from config.config import url_base, headers, workspace_gid
from helper.rest_client import RestClient
from helper.validate_response import ValidateResponse
from utils.logger import get_logger

LOGGER = get_logger(__name__, "DEBUG")


class TestSections:
    @classmethod
    def setup_class(cls) -> None:
        """Setup before all tests"""
        # arrange
        LOGGER.info("Test Section Setup Class")
        cls.section_list = []
        # set RestClient in the setup
        cls.rest_client = RestClient()
        # use the validation library
        cls.validate = ValidateResponse()
        # use random generator with faker
        cls.faker= Faker()

    # Remove get_api_data fixture and import variables from config.py
    # add marker with test type
    @pytest.mark.acceptance
    @pytest.mark.smoke
    @allure.title("Test Create Section")
    @allure.tag("smoke","acceptance")
    @allure.label("owner","Joanna Yujra")
    def test_create_section(self, test_log_name: None, create_project:str) -> None:
        """Test for create a Section

        Args:
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # body to create the Section
        section_body = {
            "data": {
                "name": f"Auto Section {self.faker.name()}"
            }
        }
        # call POST endpoint (act)
        response = requests.post(url=f"{url_base}projects/{create_project}/sections", headers=headers, json=section_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        self.section_list.append(response.json()["data"]["gid"])
        # assertion
        assert response.status_code == 201

    @pytest.mark.acceptance
    @allure.title("Test Get Section")
    @allure.tag("acceptance")
    @allure.label("owner","Joanna Yujra")
    def test_get_section(self, create_section: dict, test_log_name: None) -> None:
        """Test for get a Section

        Args:
            create_section (dict): Contains GID of the Section and GID of the Project
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for GET Section
        url_get_section = f"{url_base}sections/{create_section["section_gid"]}"
        LOGGER.debug(f"URL GET Section: {url_get_section}")
        # call GET endpoint (act)
        response = requests.get(url=url_get_section, headers=headers)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # assertion
        assert response.status_code == 200

    @pytest.mark.acceptance
    @allure.title("Test Update Section")
    @allure.tag("acceptance")
    @allure.label("owner","Joanna Yujra")
    def test_update_section(self, create_section: dict, test_log_name: None) -> None:
        """Test for update a Section

        Args:
            create_section (dict): Contains GID of the Section and GID of the Project
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for UPDATE the Section
        url_update_section = f"{url_base}sections/{create_section["section_gid"]}"
        LOGGER.debug(f"URL UPDATE Section: {url_update_section}")
        # body to update the Section
        update_section_body = {
            "data": {
                "name": "Auto Updated Section"
            }
        }
        # call PUT endpoint (act)
        response = requests.put(url=url_update_section, headers=headers, json=update_section_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # assertion
        assert response.status_code == 200

    @pytest.mark.acceptance
    @allure.title("Test Delete Section")
    @allure.tag("acceptance")
    @allure.label("owner","Joanna Yujra")
    def test_delete_section(self, create_section: dict, test_log_name: None) -> None:
        """Test for delete a Section

        Args:
            create_section (dict): Contains GID of the Section and GID of the Project
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for DELETE Section
        url_delete_section = f"{url_base}sections/{create_section["section_gid"]}"
        LOGGER.debug(f"URL DELETE Section: {url_delete_section}")

        # call DELETE endpoint (act)
        response = self.rest_client.send_request("DELETE", url=url_delete_section, headers=headers)
        # we dont need loggers
        # LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response, indent=4)}")
        # LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # assertion
        # assert response.status_code == 200
        self.validate.validate_response(response, "delete_section")

    @pytest.mark.functional
    @allure.title("Test verify error message when updating a section with different string section GID")
    @allure.tag("functional","negative")
    @allure.label("owner","Joanna Yujra")
    @pytest.mark.parametrize("section_gid", ["InvalidGID","!#$%&/()=?¡"])
    def test_update_section_using_different_string_section_gid_negative(self, test_log_name: None, section_gid:str) -> None:
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
                "name": "Auto Error Updated Section"
            }
        }
        # call PUT endpoint (act)
        response = requests.put(url=url_update_section, headers=headers, json=update_section_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # assertion
        assert response.status_code == 400

    @classmethod
    def teardown_class(cls) -> None:
        """Clean up after all tests"""
        # Clean up Sections
        LOGGER.info("Test Section Teardown Class")
        for section_gid in cls.section_list:
            url_delete_section = f"{url_base}sections/{section_gid}"
            LOGGER.debug(f"=> Delete Section Fixture: {url_delete_section}")
            response = requests.delete(url=url_delete_section, headers=headers)
            LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
            if response.status_code == 200:
                LOGGER.debug(f"=> Section with GID {section_gid} deleted")
