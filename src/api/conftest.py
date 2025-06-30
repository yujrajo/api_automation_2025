import requests
import pytest
from utils.logger import get_logger
from config.config import url_base, headers, workspace_gid


LOGGER = get_logger(__name__, "DEBUG")

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
    yield project_gid
    delete_project(project_gid)


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
    yield portfolio_gid
    delete_portfolio(portfolio_gid)

# Fixture to create sections as preconditions
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
    # get gid section
    section_gid = response.json()["data"]["gid"]
    yield section_gid

# Fixture to create tasks as preconditions
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
    yield task_gid
    delete_task(task_gid)

# Fixture to create tasks within a section as preconditions
@pytest.fixture
def create_task_on_section(create_section:str, create_project:str):
    LOGGER.info("Create Task on Section fixture")
    # body
    task_body = {
        "data": {
            "name": "Test task on section from fixture",
            "workspace": workspace_gid,
            "projects":[
                create_project
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
            "project": create_project,
            "section": create_section,
        }
    }
    response = requests.post(url=f"{url_add_task_to_project}", headers=headers, json=add_task_to_project_body)
    yield task_gid
    delete_task(task_gid)

# Fixture to log the current test
@pytest.fixture
def test_log_name(request):
    LOGGER.info(f"Start test: '{request.node.name}'")

    def end():
        LOGGER.info(f"End test: '{request.node.name}'")

    request.addfinalizer(end)

# functions to delete resources
def delete_project(project_gid):
    LOGGER.info("Delete Project fixture")
    url_delete_project = f"{url_base}projects/{project_gid}"
    LOGGER.debug(f"=> Delete Project Fixture: {url_delete_project}")
    response = requests.delete(url=url_delete_project, headers=headers)
    LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
    if response.status_code == 200:
        LOGGER.debug(f"=> Project with GID {project_gid} deleted")

def delete_portfolio(portfolio_gid):
    LOGGER.info("Delete Portfolio fixture")
    url_delete_portfolio = f"{url_base}portfolios/{portfolio_gid}"
    LOGGER.debug(f"=> Delete Portfolio Fixture: {url_delete_portfolio}")
    response = requests.delete(url=url_delete_portfolio, headers=headers)
    LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
    if response.status_code == 200:
        LOGGER.debug(f"=> Portfolio with GID {portfolio_gid} deleted")

def delete_task(task_gid):
    LOGGER.info("Delete Task fixture")
    url_delete_task = f"{url_base}tasks/{task_gid}"
    LOGGER.debug(f"=> Delete Task Fixture: {url_delete_task}")
    response = requests.delete(url=url_delete_task, headers=headers)
    LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
    if response.status_code == 200:
        LOGGER.debug(f"=> Task with GID {task_gid} deleted")
