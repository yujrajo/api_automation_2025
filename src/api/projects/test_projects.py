import json
import allure
from faker import Faker
import pytest
from config.config import url_base, headers, workspace_gid
from helper.rest_client import RestClient
from helper.validate_response import ValidateResponse
from utils.influxdb_connection import InfluxDBConnection
from utils.logger import get_logger

LOGGER = get_logger(__name__, "DEBUG")


@allure.story("Projects")
@allure.parent_suite("Projects")
class TestProjects:
    @classmethod
    def setup_class(cls) -> None:
        """Setup before all tests"""
        # arrange
        LOGGER.info("Test Project Setup Class")
        cls.project_list = []
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
        self.influxdb_client.store_data_influxdb(self.response, "projects")

    @pytest.mark.acceptance
    @pytest.mark.smoke
    @allure.title("Test Create Project")
    @allure.tag("smoke", "acceptance")
    @allure.label("owner", "Joanna Yujra")
    def test_create_project(self, test_log_name: None) -> None:
        """Test for create a project

        Args:
            test_log_name (None): Fixture to log the start and ending of test case
        """
        url_create_project = f"{url_base}projects"
        LOGGER.debug(f"URL CREATE Project: {url_create_project}")
        # body to create the project
        project_body = {
            "data": {
                "name": f"Auto New {self.faker.company()}",
                "workspace": workspace_gid
            }
        }
        # call POST endpoint (act)
        self.response = self.rest_client.send_request("POST",
                                                 url=url_create_project,
                                                 headers=headers,
                                                 body=project_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(self.response, indent=4)}")
        self.project_list.append(self.response["body"]["data"]["gid"])
        # assertion
        self.validate.validate_response(self.response, "create_project")


    @pytest.mark.acceptance
    @allure.title("Test Get Project")
    @allure.tag("acceptance")
    @allure.label("owner", "Joanna Yujra")
    def test_get_project(self, create_project: str, test_log_name: None) -> None:
        """Test for get a project

        Args:
            create_project (str): GID of the project
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for GET project
        url_get_project = f"{url_base}projects/{create_project}"
        LOGGER.debug(f"URL GET Project: {url_get_project}")
        # call GET endpoint (act)
        self.response = self.rest_client.send_request("GET",
                                                 url=url_get_project,
                                                 headers=headers)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(self.response, indent=4)}")
        # assertion
        self.validate.validate_response(self.response, "get_project")

    @pytest.mark.acceptance
    @allure.title("Test Update Project")
    @allure.tag("acceptance")
    @allure.label("owner", "Joanna Yujra")
    def test_update_project(self, create_project: str, test_log_name: None) -> None:
        """Test for update a project

        Args:
            create_project (str): GID of the project
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for UPDATE the project
        url_update_project = f"{url_base}projects/{create_project}"
        LOGGER.debug(f"URL UPDATE Project: {url_update_project}")
        # body to update the project
        update_project_body = {
            "data": {
                "name": f"Auto Updated {self.faker.company()}",
                "color": "light-green",
                "default_view": "calendar",
                "notes": "These is an auto updated project.",
            }
        }
        # call PUT endpoint (act)
        self.response = self.rest_client.send_request("PUT",
                                                 url=url_update_project,
                                                 headers=headers,
                                                 body=update_project_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(self.response, indent=4)}")
        # assertion
        self.validate.validate_response(self.response, "update_project")

    @pytest.mark.acceptance
    @allure.title("Test Delete Project")
    @allure.tag("acceptance")
    @allure.label("owner", "Joanna Yujra")
    def test_delete_project(self, create_project: str, test_log_name: None) -> None:
        """Test for delete a project

        Args:
            create_project (str): GID of the project
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for DELETE project
        url_delete_project = f"{url_base}projects/{create_project}"
        LOGGER.debug(f"URL DELETE Project: {url_delete_project}")
        # call DELETE endpoint (act)
        self.response = self.rest_client.send_request("DELETE",
                                                 url=url_delete_project,
                                                 headers=headers)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(self.response, indent=4)}")
        # assertion
        self.validate.validate_response(self.response, "delete_project")

    @pytest.mark.functional
    @allure.title("Test validate error message when trying to create project without body")
    @allure.tag("functional", "negative")
    @allure.label("owner", "Joanna Yujra")
    def test_create_project_without_body_negative(self, test_log_name: str) -> None:
        """Test for create a project without body

        Args:
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for CREATE project
        url_create_project = f"{url_base}projects"
        LOGGER.debug(f"URL CREATE Project: {url_create_project}")
        # call POST endpoint (act)
        self.response = self.rest_client.send_request("POST",
                                                 url=url_create_project,
                                                 headers=headers)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(self.response, indent=4)}")
        # assertion
        self.validate.validate_response(self.response, "create_project_without_body")

    @pytest.mark.functional
    @allure.title("Test create project with different special characters names")
    @allure.tag("functional")
    @allure.label("owner", "Joanna Yujra")
    @pytest.mark.parametrize(
        "name_project", ["1234567890", "!#$%&/()=?¡*¨[]_:;,.-+´¿'|`^~¬°", "<script>alert('test');</script>"]
    )
    def test_create_project_using_different_project_name_data(self, test_log_name: None, name_project: str) -> None:
        """Test for create a project using different inputs in project name

        Args:
            test_log_name (None): Fixture to log the start and ending of test case
            name_project (str): _description_
        """
        # url for CREATE project
        url_create_project = f"{url_base}projects"
        LOGGER.debug(f"URL CREATE Project: {url_create_project}")
        # body to create the project
        project_body = {
            "data": {
                "name": f"{name_project}",
                "workspace": workspace_gid
            }
        }
        # call POST endpoint (act)
        self.response = self.rest_client.send_request("POST",
                                                 url=url_create_project,
                                                 headers=headers,
                                                 body=project_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(self.response, indent=4)}")
        self.project_list.append(self.response["body"]["data"]["gid"])
        # assertion
        self.validate.validate_response(self.response, "create_project")

    @classmethod
    def teardown_class(cls) -> None:
        """Clean up after all tests"""
        # Clean up projects
        LOGGER.info("Test Project Teardown Class")
        for project_gid in cls.project_list:
            url_delete_project = f"{url_base}projects/{project_gid}"
            LOGGER.debug(f"=> Delete Project Fixture: {url_delete_project}")
            response = cls.rest_client.send_request("DELETE",
                                                    url=url_delete_project,
                                                    headers=headers)
            LOGGER.debug(f"=> STATUS CODE: {response['status_code']}")
            if response["status_code"] == 200:
                LOGGER.debug(f"=> Project with GID {project_gid} deleted")

        cls.influxdb_client.close()
