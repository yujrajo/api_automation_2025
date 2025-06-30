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
        cls.faker= Faker()

    # Remove get_api_data fixture and import variables from config.py
    # add marker with test type
    @pytest.mark.acceptance
    @pytest.mark.smoke
    @allure.title("Test Create Project")
    @allure.tag("smoke","acceptance")
    @allure.label("owner","Joanna Yujra")
    def test_create_project(self, test_log_name: None) -> None:
        """Test for create a project

        Args:
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # body to create the project
        project_body = {
            "data": {
                "name": f"Auto New {self.faker.company()}",
                "workspace": workspace_gid
            }
        }
        # call POST endpoint (act)
        response = requests.post(url=f"{url_base}projects", headers=headers, json=project_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        self.project_list.append(response.json()["data"]["gid"])
        # assertion
        assert response.status_code == 201

    @pytest.mark.acceptance
    @allure.title("Test Get Project")
    @allure.tag("acceptance")
    @allure.label("owner","Joanna Yujra")
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
        response = requests.get(url=url_get_project, headers=headers)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # assertion
        assert response.status_code == 200

    @pytest.mark.acceptance
    @allure.title("Test Update Project")
    @allure.tag("acceptance")
    @allure.label("owner","Joanna Yujra")
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
                "name": "Auto Updated Name",
                "color": "light-green",
                "default_view": "calendar",
                "notes": "These is an auto updated project.",
            }
        }
        # call PUT endpoint (act)
        response = requests.put(url=url_update_project, headers=headers, json=update_project_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # assertion
        assert response.status_code == 200

    @pytest.mark.acceptance
    @allure.title("Test Delete Project")
    @allure.tag("acceptance")
    @allure.label("owner","Joanna Yujra")
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
        response = self.rest_client.send_request("DELETE", url=url_delete_project, headers=headers)
        # we dont need loggers
        # LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response, indent=4)}")
        # LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # assertion
        # assert response.status_code == 200
        self.validate.validate_response(response, "delete_project")

    @pytest.mark.functional
    @allure.title("Test validate error message when trying to create project without body")
    @allure.tag("functional","negative")
    @allure.label("owner","Joanna Yujra")
    def test_create_project_without_body_negative(self, test_log_name: str) -> None:
        """Test for create a project without body

        Args:
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # call POST endpoint (act)
        response = self.rest_client.send_request("POST", url=f"{url_base}projects", headers=headers)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response['body'], indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response['status_code']}")
        # # assertion, we can add message to assertions
        # assert response["status_code"] == 400, f"Expected 400 but received {response["status_code"]}"
        # we now move this assertions to a library to validate the response, status cose, headers, body etc... 06_validations.md
        self.validate.validate_response(response, "create_project_without_body")
        # # validate the schema hardcoded
        # schema = {
        #     "type": "object",
        #     "properties": {
        #         "errors": {
        #             "type": "array",
        #             "items": {
        #                 "type": "object",
        #                 "properties": {
        #                     "message": {"type": "string"},
        #                     "help": {"type": "string"}
        #                 },
        #             },
        #         }
        #     },
        # }
        # try:
        #     jsonschema.validate(instance=response["body"], schema=schema)
        #     LOGGER.debug("Schema is valid")
        # # it does not stop the execution because we are only loggin the error, now we move this to the validator
        # except jsonschema.exceptions.ValidationError as e:
        #     LOGGER.debug(f"JSON Validator Error: {e}")

    # we call teardown class to delete all resources at the end of the execution
    # to do it we save in a list(setUpClass) all resources not deleted by create_job fixture
    # and only delete the resources from that list

    @pytest.mark.functional
    @allure.title("Test create project with different names")
    @allure.tag("functional")
    @allure.label("owner","Joanna Yujra")
    @pytest.mark.parametrize("name_project", ["1234567890","!#$%&/()=?¡*¨[]_:;,.-+´¿'|`^~¬°!","<script>alert('test');</script>"])
    def test_create_project_using_different_project_name_data(self, test_log_name: None, name_project:str) -> None:
        """Test for create a project using different inputs in project name

        Args:
            test_log_name (None): Fixture to log the start and ending of test case
            name_project (str): _description_
        """
        # body to create the project
        project_body = {
            "data": {
                "name": f"{name_project}",
                "workspace": workspace_gid
            }
        }
        # call POST endpoint (act)
        response = requests.post(url=f"{url_base}projects", headers=headers, json=project_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        self.project_list.append(response.json()["data"]["gid"])
        # assertion
        assert response.status_code == 201


    @classmethod
    def teardown_class(cls) -> None:
        """Clean up after all tests"""
        # Clean up projects
        LOGGER.info("Test Project Teardown Class")
        for project_gid in cls.project_list:
            url_delete_project = f"{url_base}projects/{project_gid}"
            LOGGER.debug(f"=> Delete Project Fixture: {url_delete_project}")
            response = requests.delete(url=url_delete_project, headers=headers)
            LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
            if response.status_code == 200:
                LOGGER.debug(f"=> Project with GID {project_gid} deleted")
