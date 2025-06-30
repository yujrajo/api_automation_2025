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


@allure.story("Tasks")
@allure.parent_suite("Tasks")
class TestTasks:
    @classmethod
    def setup_class(cls) -> None:
        """Setup before all tests"""
        # arrange
        LOGGER.info("Test Task Setup Class")
        cls.task_list = []
        # set RestClient in the setup
        cls.rest_client = RestClient()
        # use the validation library
        cls.validate = ValidateResponse()
        # use random generator with faker
        cls.faker = Faker()

    @pytest.mark.acceptance
    @pytest.mark.smoke
    @allure.title("Test Create Task")
    @allure.tag("smoke", "acceptance")
    @allure.label("owner", "Joanna Yujra")
    def test_create_task(self, test_log_name: None) -> None:
        """Test for create a Task

        Args:
            test_log_name (None): Fixture to log the start and ending of test case
        """
        url_create_task = f"{url_base}tasks"
        LOGGER.debug(f"URL CREATE Task: {url_create_task}")
        # body to create the Task
        task_body = {
            "data": {
                "name": f"Auto Task {self.faker.sentence()}",
                "workspace": workspace_gid,
                "notes": "These is an auto created task.",
            }
        }
        # call POST endpoint (act)
        response = self.rest_client.send_request("POST",
                                                 url=url_create_task,
                                                 headers=headers,
                                                 body=task_body)
        LOGGER.debug(f"RESPONSE: {json.dumps(response, indent=4)}")
        self.task_list.append(response["body"]["data"]["gid"])
        # assertion
        self.validate.validate_response(response, "create_task")

    @pytest.mark.acceptance
    @allure.title("Test Get Task")
    @allure.tag("acceptance")
    @allure.label("owner", "Joanna Yujra")
    def test_get_task(self, create_task: str, test_log_name: None) -> None:
        """Test for get a Task

        Args:
            create_task (str): GID of the Task
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for GET Task
        url_get_task = f"{url_base}tasks/{create_task}"
        LOGGER.debug(f"URL GET Task: {url_get_task}")
        # call GET endpoint (act)
        response = self.rest_client.send_request("GET",
                                                 url=url_get_task,
                                                 headers=headers)
        LOGGER.debug(f"RESPONSE: {json.dumps(response, indent=4)}")
        # assertion
        self.validate.validate_response(response, "get_task")

    @pytest.mark.acceptance
    @allure.title("Test Update Task")
    @allure.tag("acceptance")
    @allure.label("owner", "Joanna Yujra")
    def test_update_task(self, create_task: str, test_log_name: None) -> None:
        """Test for update a Task

        Args:
            create_task (str): GID of the Task
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for UPDATE the Task
        url_update_task = f"{url_base}tasks/{create_task}"
        LOGGER.debug(f"URL UPDATE Task: {url_update_task}")
        # body to update the Task
        update_task_body = {
            "data": {
                "name": f"Auto Updated {self.faker.sentence()}",
                "notes": "These is an auto updated task.",
            }
        }
        # call PUT endpoint (act)
        response = self.rest_client.send_request("PUT",
                                                 url=url_update_task,
                                                 headers=headers,
                                                 body=update_task_body)
        LOGGER.debug(f"RESPONSE: {json.dumps(response, indent=4)}")
        # assertion
        self.validate.validate_response(response, "update_task")

    @pytest.mark.acceptance
    @allure.title("Test Delete Task")
    @allure.tag("acceptance")
    @allure.label("owner", "Joanna Yujra")
    def test_delete_task(self, create_task: str, test_log_name: None) -> None:
        """Test for delete a Task

        Args:
            create_task (str): GID of the Task
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for DELETE Task
        url_delete_task = f"{url_base}tasks/{create_task}"
        LOGGER.debug(f"URL DELETE Task: {url_delete_task}")
        # call DELETE endpoint (act)
        response = self.rest_client.send_request("DELETE",
                                                 url=url_delete_task,
                                                 headers=headers)
        LOGGER.debug(f"RESPONSE: {json.dumps(response, indent=4)}")
        # assertion
        self.validate.validate_response(response, "delete_task")

    @pytest.mark.functional
    @allure.title("Test Create Task with a Project")
    @allure.tag("functional")
    @allure.label("owner", "Joanna Yujra")
    def test_create_task_with_a_project(self, create_project: str):
        # url for CREATE Task with a project
        url_create_task_with_project = f"{url_base}tasks"
        LOGGER.debug(f"URL ADD Task to Project: {url_create_task_with_project}")
        # body to for Task with a project
        task_body = {
            "data": {
                "name": f"Test task {self.faker.sentence()} on Project",
                "workspace": workspace_gid,
                "projects": [create_project]
            }
        }
        response = self.rest_client.send_request("POST",
                                                 url=url_create_task_with_project,
                                                 headers=headers,
                                                 body=task_body)
        LOGGER.debug(f"RESPONSE: {json.dumps(response, indent=4)}")
        self.task_list.append(response["body"]["data"]["gid"])
        # assertion
        self.validate.validate_response(response, "create_task")

    @pytest.mark.e2e
    @allure.title("Test Add a Task to a Project's section")
    @allure.tag("e2e")
    @allure.label("owner", "Joanna Yujra")
    def test_add_task_to_a_project_section(self, create_section: str, create_task: str, create_project):
        # url for ADD Task to the project section
        url_add_task_to_project = f"{url_base}tasks/{create_task}/addProject"
        LOGGER.debug(f"URL ADD Task to Project Section: {url_add_task_to_project}")
        # body to add Task to section
        add_task_to_project_section = {
            "data": {
                "project": create_project,
                "section": create_section,
            }
        }
        # call POST endpoint (act)
        response = self.rest_client.send_request("POST",
                                                 url=url_add_task_to_project,
                                                 headers=headers,
                                                 body=add_task_to_project_section)
        LOGGER.debug(f"RESPONSE: {json.dumps(response, indent=4)}")
        # assertion
        self.validate.validate_response(response, "add_task_to_project_section")

    @pytest.mark.e2e
    @allure.title("Test Insert a Task before another task on a Project's section")
    @allure.tag("e2e")
    @allure.label("owner", "Joanna Yujra")
    def test_insert_a_task_before_other_task_on_a_section(self, create_task_on_section: str, create_task: str, create_project:str):
        # url for INSERT a Task on a Project before another task
        url_insert_task = f"{url_base}tasks/{create_task}/addProject"
        LOGGER.debug(f"URL DELETE Task: {url_insert_task}")
        # body to insert Task into Projects Section
        insert_task_body = {
            "data": {
                "project": create_project,
                "insert_before": create_task_on_section,
            }
        }
        # call POST endpoint (act)
        response = self.rest_client.send_request("POST",
                                                 url=url_insert_task,
                                                 headers=headers,
                                                 body=insert_task_body)
        LOGGER.debug(f"RESPONSE: {json.dumps(response, indent=4)}")
        # assertion
        self.validate.validate_response(response, "insert_task_before_another")


    @classmethod
    def teardown_class(cls) -> None:
        """Clean up after all tests"""
        # Clean up Tasks
        LOGGER.info("Test Task Teardown Class")
        for task_gid in cls.task_list:
            url_delete_task = f"{url_base}tasks/{task_gid}"
            LOGGER.debug(f"Delete Task Fixture: {url_delete_task}")
            response = cls.rest_client.send_request("DELETE",
                                                    url=url_delete_task,
                                                    headers=headers)
            LOGGER.debug(f"=> STATUS CODE: {response['status_code']}")
            if response["status_code"] == 200:
                LOGGER.debug(f"=> Task with GID {task_gid} deleted")
