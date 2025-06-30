import json
import allure
from faker import Faker
import pytest
from config.config import url_base, headers
from helper.rest_client import RestClient
from helper.validate_response import ValidateResponse
from utils.logger import get_logger

LOGGER = get_logger(__name__, "DEBUG")


@allure.story("Portfolios")
@allure.parent_suite("Portfolios")
class TestPortfolios:
    @classmethod
    def setup_class(cls) -> None:
        """Setup before all tests"""
        # arrange
        LOGGER.info("Test Portfolio Setup Class")
        cls.portfolio_list = []
        # set RestClient in the setup
        cls.rest_client = RestClient()
        # use the validation library
        cls.validate = ValidateResponse()
        # use random generator with faker
        cls.faker = Faker()

    @pytest.mark.e2e
    @allure.title("Test add a Project to a Portfolio")
    @allure.tag("e2e")
    @allure.label("owner", "Joanna Yujra")
    def test_add_project_to_portfolio(self, create_portfolio: str, create_project: str, test_log_name: None) -> None:
        """Test add a Project to a Portfolio

        Args:
            create_portfolio(str): GID of the portfolio
            create_project (str): GID of the project
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for ADDING a project to a portfolio
        url_add_project = f"{url_base}portfolios/{create_portfolio}/addItem"
        LOGGER.debug(f"URL UPDATE Project: {url_add_project}")
        # body to update the project
        add_project_body = {
            "data": {
                "item": create_project,
            }
        }
        # call POST endpoint (act)
        response = self.rest_client.send_request("POST",
                                                 url=url_add_project,
                                                 headers=headers,
                                                 body=add_project_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response, indent=4)}")
        # assertion
        self.validate.validate_response(response, "add_project_to_portfolio")
