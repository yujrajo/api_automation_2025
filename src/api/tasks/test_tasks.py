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
        cls.faker= Faker()

    # Remove get_api_data fixture and import variables from config.py
    # add marker with test type
    @pytest.mark.acceptance
    @pytest.mark.smoke
    @allure.title("Test Create Task")
    @allure.tag("smoke","acceptance")
    @allure.label("owner","Joanna Yujra")
    def test_create_task(self, test_log_name: None) -> None:
        """Test for create a Task

        Args:
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # body to create the Task
        task_body = {
            "data": {
                "name": f"Auto Task {self.faker.name()}",
                "workspace": workspace_gid,
                "notes": "These is an auto created task.",
            }
        }
        # call POST endpoint (act)
        response = requests.post(url=f"{url_base}tasks", headers=headers, json=task_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        self.task_list.append(response.json()["data"]["gid"])
        # assertion
        assert response.status_code == 201

    @pytest.mark.acceptance
    @allure.title("Test Get Task")
    @allure.tag("acceptance")
    @allure.label("owner","Joanna Yujra")
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
        response = requests.get(url=url_get_task, headers=headers)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # assertion
        assert response.status_code == 200

    @pytest.mark.acceptance
    @allure.title("Test Update Task")
    @allure.tag("acceptance")
    @allure.label("owner","Joanna Yujra")
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
                "name": "Auto Updated Task",
                "notes": "These is an auto updated task.",
            }
        }
        # call PUT endpoint (act)
        response = requests.put(url=url_update_task, headers=headers, json=update_task_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # assertion
        assert response.status_code == 200

    @pytest.mark.acceptance
    @allure.title("Test Delete Task")
    @allure.tag("acceptance")
    @allure.label("owner","Joanna Yujra")
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
        response = self.rest_client.send_request("DELETE", url=url_delete_task, headers=headers)
        # we dont need loggers
        # LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response, indent=4)}")
        # LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # assertion
        # assert response.status_code == 200
        self.validate.validate_response(response, "delete_task")

    def test_add_task_to_a_project(self,create_project:str,create_task:str):
        url_add_task_to_project = f"{url_base}tasks/{create_task}"
        LOGGER.debug(f"URL ADD Task to Project: {url_add_task_to_project}")
        task_body = {
            "data": {
                "name": "Test task on Project",
                "workspace": workspace_gid,
                "projects":[
                    create_project
                ]
            }
        }
        # call to endpoint
        response = requests.post(
            url=f"{url_add_task_to_project}", headers=headers, json=task_body
        )
        LOGGER.debug(response.json())
        # assert response.status_code == 200


    def test_add_task_to_a_project_section(self,create_section:dict,create_task:str):
        url_add_task_to_project = f"{url_base}tasks/{create_task}/addProject"
        LOGGER.debug(f"URL ADD Task to Project: {url_add_task_to_project}")
        add_task_to_project_body = {
            "data": {
                "name": "Test task on section",
                "workspace": workspace_gid,
                "projects":[
                    create_section["project_gid"]
                ]
            }
        }
        # call to endpoint
        response = requests.post(
            url=f"{url_add_task_to_project}", headers=headers, json=add_task_to_project_body
        )
        LOGGER.debug(response.json())
        # get gid task
        # add task to projects section
        url_add_task_to_project_section = f"{url_base}tasks/{create_task}/addProject"
        LOGGER.debug(f"URL ADD Task to Project Section: {url_add_task_to_project}")
        url_add_task_to_project_section = {
            "data": {
                "project": create_section["project_gid"],
                "section": create_section["section_gid"],
            }
        }
        response = requests.post(url=f"{url_add_task_to_project}", headers=headers, json=url_add_task_to_project_section)
        assert response.status_code == 200


    def test_insert_a_task_before_other_task_on_a_section(self,create_task_on_section:dict, create_task:str):
        # url for INSERT a Task on a Project before another task
        url_insert_task = f"{url_base}tasks/{create_task}/addProject"
        LOGGER.debug(f"URL DELETE Task: {url_insert_task}")
        insert_task_body = {
            "data": {
                "project": create_task_on_section["project_gid"],
                "insert_before": create_task_on_section["task_gid"],
            }
        }
        # call POST endpoint (act)
        response = requests.post(url=f"{url_insert_task}", headers=headers, json=insert_task_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # self.task_list.append(response.json()["data"]["gid"])
        # assertion
        assert response.status_code == 200


    @classmethod
    def teardown_class(cls) -> None:
        """Clean up after all tests"""
        # Clean up Tasks
        LOGGER.info("Test Task Teardown Class")
        for task_gid in cls.task_list:
            url_delete_task = f"{url_base}tasks/{task_gid}"
            LOGGER.debug(f"=> Delete Task Fixture: {url_delete_task}")
            response = requests.delete(url=url_delete_task, headers=headers)
            LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
            if response.status_code == 200:
                LOGGER.debug(f"=> Task with GID {task_gid} deleted")
