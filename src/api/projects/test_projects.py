import json
import logging
import requests
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestProjects:
    def test_create_project(self, get_api_data, test_log_name):
        project_body = {
            "data": {
                "name": "Auto New Project from Test",
                "workspace": f"{get_api_data['workspace_gid']}"
            }
        }
        response = requests.post(
            url=f"{get_api_data['url_base']}projects", headers=get_api_data["headers"], json=project_body
        )
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        assert response.status_code == 201

    def test_get_project(self, get_api_data, create_project, test_log_name):
        url_get_project = f"{get_api_data['url_base']}projects/{create_project}"
        response = requests.get(url=url_get_project, headers=get_api_data["headers"])
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        assert response.status_code == 200

    def test_update_project(self, get_api_data, create_project, test_log_name):
        url_update_project = f"{get_api_data['url_base']}projects/{create_project}"
        update_project_body = {
            "data": {
                "name": "Auto Updated Name",
                "color": "light-green",
                "default_view": "calendar",
                "notes": "These is an auto updated project.",
            }
        }
        response = requests.put(url=url_update_project, headers=get_api_data["headers"], json=update_project_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        assert response.status_code == 200

    def test_delete_project(self, get_api_data, create_project, test_log_name):
        url_delete_project = f"{get_api_data['url_base']}projects/{create_project}"
        response = requests.delete(url=url_delete_project, headers=get_api_data["headers"])
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        assert response.status_code == 200
