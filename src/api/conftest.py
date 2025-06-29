import logging
import os
import requests
import pytest
from utils.logger import get_logger
from dotenv import load_dotenv

LOGGER = get_logger(__name__, logging.DEBUG)


# Arrange
@pytest.fixture(scope="class")
def first_entry():
    LOGGER.warning("==> first entry fixture")
    # with scope class it will be executed once for the whole class
    return "a"


# Arrange calls the other fixture
@pytest.fixture
def order(first_entry):
    LOGGER.warning("==> order fixture")
    return first_entry


# fixture for headers
@pytest.fixture(scope="class")
def get_api_data():
    LOGGER.debug("get headers, url base and workspace gid")
    api_data = {}
    load_dotenv()
    api_token = os.getenv("TOKEN_ASANA")
    url_base = os.getenv("URL_BASE")
    workspace_gid = os.getenv("WORKSPACE_GID")

    headers = {"Authorization": f"Bearer {api_token}"}

    api_data["headers"] = headers
    api_data["url_base"] = url_base
    api_data["workspace_gid"] = workspace_gid

    return api_data


# Fixture to create projects as preconditions
@pytest.fixture
def create_project(get_api_data):
    # body
    project_body = {"data": {"name": "Test project from fixture", "workspace": f"{get_api_data['workspace_gid']}"}}
    # call to endpoint
    response = requests.post(
        url=f"{get_api_data['url_base']}projects", headers=get_api_data["headers"], json=project_body
    )
    LOGGER.debug(response.json())
    # get gid project
    project_gid = response.json()["data"]["gid"]
    # return gid project
    return project_gid
    # get secrets using dotenv


# Fixture to log the current test
@pytest.fixture
def test_log_name(request):
    LOGGER.info(f"Start test: '{request.node.name}'")

    def end():
        LOGGER.info(f"End test: '{request.node.name}'")

    request.addfinalizer(end)

    # LOGGER.info(f"API token asana: {api_token}")
    # # project body
    # project_body = {
    #     "name": "Test Project from fixture",
    # }
    # # call endpoint using requests
    # response = requests.post(
    #     url=f"{url_base}projects", headers=headers, json=project_body
    # )
    # LOGGER.debug(json.dumps(response.json(), indent=4))

    # # get id project
    # project_id = response.json()["id"]
    # # once the test ends yield call to delete the project
    # yield project_id
    # delete_project(project_id)
    # LOGGER.warning("==> order fixture")
    # return first_entry
