import requests
import pytest
from utils.logger import get_logger
from config.config import url_base, headers, workspace_gid


LOGGER = get_logger(__name__, "DEBUG")


# # Arrange
# @pytest.fixture(scope="class")
# def first_entry():
#     LOGGER.warning("==> first entry fixture")
#     # with scope class it will be executed once for the whole class
#     return "a"


# # Arrange calls the other fixture
# @pytest.fixture
# def order(first_entry):
#     LOGGER.warning("==> order fixture")
#     return first_entry


# fixture for headers REPLACED BY CONFIG FILE
# @pytest.fixture(scope="class")
# def get_api_data():
#     LOGGER.debug("get headers, url base and workspace gid")
#     api_data = {}
#     load_dotenv()
#     api_token = os.getenv("TOKEN_ASANA")
#     url_base = os.getenv("URL_BASE")
#     workspace_gid = os.getenv("WORKSPACE_GID")

#     headers = {"Authorization": f"Bearer {api_token}"}

#     api_data["headers"] = headers
#     api_data["url_base"] = url_base
#     api_data["workspace_gid"] = workspace_gid

#     return api_data


# Fixture to create projects as preconditions
@pytest.fixture
def create_project():
    LOGGER.info("Create Project fixture")
    # body
    project_body = {
        "data": {
            "name": "Test project from fixture",
            "workspace": f"{workspace_gid}"
        }
    }
    # call to endpoint
    response = requests.post(
        url=f"{url_base}projects", headers=headers, json=project_body
    )
    LOGGER.debug(response.json())
    # get gid project
    project_gid = response.json()["data"]["gid"]
    # return gid project
    # return project_gid

    # now we use yield,
    # calls a normal function(not fixture) at the end of the test
    # we use it to delete the projects at the end of the test "clean-up"
    yield project_gid
    delete_project(project_gid)
    # get secrets using dotenv

# Fixture to create portfolios as preconditions
@pytest.fixture
def create_portfolio():
    LOGGER.info("Create Portfolio fixture")
    # body
    portfolio_body = {
        "data": {
            "name": "Test portfolio from fixture",
            "workspace": f"{workspace_gid}"
        }
    }
    # call to endpoint
    response = requests.post(
        url=f"{url_base}portfolios", headers=headers, json=portfolio_body
    )
    LOGGER.debug(response.json())
    # get gid portfolio
    portfolio_gid = response.json()["data"]["gid"]
    # return gid portfolio
    # return portfolio

    # now we use yield,
    # calls a normal function(not fixture) at the end of the test
    # we use it to delete the projects at the end of the test "clean-up"
    yield portfolio_gid
    delete_portfolio(portfolio_gid)
    # get secrets using dotenv

@pytest.fixture
def create_section(create_project:str):
    LOGGER.info("Create Section fixture")
    # body
    section_body = {
        "data": {
            "name": "Test section from fixture"
        }
    }
    # call to endpoint
    response = requests.post(
        url=f"{url_base}projects/{create_project}/sections", headers=headers, json=section_body
    )
    LOGGER.debug(response.json())
    # get gid portfolio
    section_gid = response.json()["data"]["gid"]
    # return gid portfolio
    # return portfolio

    # now we use yield,
    # calls a normal function(not fixture) at the end of the test
    # we use it to delete the projects at the end of the test "clean-up"
    yield {"section_gid":section_gid,"project_gid":create_project}
    # delete_section(section_gid)
    # get secrets using dotenv

@pytest.fixture
def create_task():
    LOGGER.info("Create Task fixture")
    # body
    task_body = {
        "data": {
            "name": "Test task from fixture",
            "workspace": workspace_gid
        }
    }
    # call to endpoint
    response = requests.post(
        url=f"{url_base}tasks", headers=headers, json=task_body
    )
    LOGGER.debug(response.json())
    # get gid task
    task_gid = response.json()["data"]["gid"]
    # return gid portfolio
    # return portfolio

    # now we use yield,
    # calls a normal function(not fixture) at the end of the test
    # we use it to delete the projects at the end of the test "clean-up"
    yield task_gid
    delete_task(task_gid)
    # get secrets using dotenv

@pytest.fixture
def create_task_on_section(create_section:dict):
    LOGGER.info("Create Task on Section fixture")
    # body
    task_body = {
        "data": {
            "name": "Test task on section from fixture",
            "workspace": workspace_gid,
            "projects":[
                create_section["project_gid"]
            ]
        }
    }
    # call to endpoint
    response = requests.post(
        url=f"{url_base}tasks", headers=headers, json=task_body
    )
    LOGGER.debug(response.json())
    # get gid task
    task_gid = response.json()["data"]["gid"]
    # add task to projects section
    url_add_task_to_project = f"{url_base}tasks/{task_gid}/addProject"
    LOGGER.debug(f"URL DELETE Task: {url_add_task_to_project}")
    add_task_to_project_body = {
        "data": {
            "project": create_section["project_gid"],
            "section": create_section["section_gid"],
        }
    }
    response = requests.post(url=f"{url_add_task_to_project}", headers=headers, json=add_task_to_project_body)
    # now we use yield,
    # calls a normal function(not fixture) at the end of the test
    # we use it to delete the projects at the end of the test "clean-up"
    yield {"project_gid":create_section["project_gid"],"section_gid":create_section["section_gid"], "task_gid":task_gid}
    delete_task(task_gid)
    # get secrets using dotenv

# Fixture to log the current test
@pytest.fixture
def test_log_name(request):
    LOGGER.info(f"Start test: '{request.node.name}'")

    def end():
        LOGGER.info(f"End test: '{request.node.name}'")

    request.addfinalizer(end)

def delete_project(project_gid):
    LOGGER.info("Delete Project fixture")
    # now we delete through API
    # if we have access to DB we can delete the resources here with an script
    url_delete_project = f"{url_base}projects/{project_gid}"
    LOGGER.debug(f"=> Delete Project Fixture: {url_delete_project}")
    response = requests.delete(url=url_delete_project, headers=headers)
    LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
    if response.status_code == 200:
        LOGGER.debug(f"=> Project with GID {project_gid} deleted")

def delete_portfolio(portfolio_gid):
    LOGGER.info("Delete Portfolio fixture")
    # now we delete through API
    # if we have access to DB we can delete the resources here with an script
    url_delete_portfolio = f"{url_base}portfolios/{portfolio_gid}"
    LOGGER.debug(f"=> Delete Portfolio Fixture: {url_delete_portfolio}")
    response = requests.delete(url=url_delete_portfolio, headers=headers)
    LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
    if response.status_code == 200:
        LOGGER.debug(f"=> Portfolio with GID {portfolio_gid} deleted")

def delete_task(task_gid):
    LOGGER.info("Delete Task fixture")
    # now we delete through API
    # if we have access to DB we can delete the resources here with an script
    url_delete_task = f"{url_base}tasks/{task_gid}"
    LOGGER.debug(f"=> Delete Task Fixture: {url_delete_task}")
    response = requests.delete(url=url_delete_task, headers=headers)
    LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
    if response.status_code == 200:
        LOGGER.debug(f"=> Task with GID {task_gid} deleted")

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
