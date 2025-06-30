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
        cls.faker= Faker()

    # Remove get_api_data fixture and import variables from config.py
    # add marker with test type
    @pytest.mark.acceptance
    @pytest.mark.smoke
    @allure.title("Test Create Portfolio")
    @allure.tag("smoke","acceptance")
    @allure.label("owner","Joanna Yujra")
    def test_create_portfolio(self, test_log_name: None) -> None:
        """Test for create a Portfolio

        Args:
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # body to create the Portfolio
        portfolio_body = {
            "data": {
                "name": f"Auto Portfolio {self.faker.company()}",
                "workspace": workspace_gid
            }
        }
        # call POST endpoint (act)
        response = requests.post(url=f"{url_base}portfolios", headers=headers, json=portfolio_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        self.portfolio_list.append(response.json()["data"]["gid"])
        # assertion
        assert response.status_code == 201

    @pytest.mark.acceptance
    @allure.title("Test Get Portfolio")
    @allure.tag("acceptance")
    @allure.label("owner","Joanna Yujra")
    def test_get_portfolio(self, create_portfolio: str, test_log_name: None) -> None:
        """Test for get a Portfolio

        Args:
            create_portfolio (str): GID of the Portfolio
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for GET Portfolio
        url_get_portfolio = f"{url_base}portfolios/{create_portfolio}"
        LOGGER.debug(f"URL GET Portfolio: {url_get_portfolio}")
        # call GET endpoint (act)
        response = requests.get(url=url_get_portfolio, headers=headers)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # assertion
        assert response.status_code == 200

    @pytest.mark.acceptance
    @allure.title("Test Update Portfolio")
    @allure.tag("acceptance")
    @allure.label("owner","Joanna Yujra")
    def test_update_portfolio(self, create_portfolio: str, test_log_name: None) -> None:
        """Test for update a Portfolio

        Args:
            create_portfolio (str): GID of the Portfolio
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for UPDATE the Portfolio
        url_update_portfolio = f"{url_base}portfolios/{create_portfolio}"
        LOGGER.debug(f"URL UPDATE Portfolio: {url_update_portfolio}")
        # body to update the Portfolio
        update_portfolio_body = {
            "data": {
                "name": "Auto Updated Portfolio",
                "color": "light-blue"
            }
        }
        # call PUT endpoint (act)
        response = requests.put(url=url_update_portfolio, headers=headers, json=update_portfolio_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # assertion
        assert response.status_code == 200

    @pytest.mark.acceptance
    @allure.title("Test Delete Portfolio")
    @allure.tag("acceptance")
    @allure.label("owner","Joanna Yujra")
    def test_delete_portfolio(self, create_portfolio: str, test_log_name: None) -> None:
        """Test for delete a Portfolio

        Args:
            create_portfolio (str): GID of the Portfolio
            test_log_name (None): Fixture to log the start and ending of test case
        """
        # url for DELETE Portfolio
        url_delete_portfolio = f"{url_base}portfolios/{create_portfolio}"
        LOGGER.debug(f"URL DELETE Portfolio: {url_delete_portfolio}")

        # call DELETE endpoint (act)
        response = self.rest_client.send_request("DELETE", url=url_delete_portfolio, headers=headers)
        # we dont need loggers
        # LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response, indent=4)}")
        # LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # assertion
        # assert response.status_code == 200
        self.validate.validate_response(response, "delete_portfolio")

    @pytest.mark.functional
    @allure.title("Test verify error message when creating a portfolio with different empty names")
    @allure.tag("functional","negative")
    @allure.label("owner","Joanna Yujra")
    @pytest.mark.parametrize("name_portfolio", [""," ",None])
    def test_create_portfolio_using_different_empty_portfolio_name_negative(self, test_log_name: None, name_portfolio:str) -> None:
        """Test for create a portfolio using different empty inputs for portfolio name

        Args:
            test_log_name (None): Fixture to log the start and ending of test case
            name_portfolio (str): list of possible empty names
        """
        data={}
        if name_portfolio is not None:
            data["name"] = name_portfolio
        data["workspace"] = workspace_gid
        # body to create the portfolio
        portfolio_body = {
            "data": data
        }
        # call POST endpoint (act)
        response = requests.post(url=f"{url_base}portfolios", headers=headers, json=portfolio_body)
        LOGGER.debug(f"=> RESPONSE: {json.dumps(response.json(), indent=4)}")
        LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
        # self.portfolio_list.append(response.json()["data"]["gid"])
        # assertion
        assert response.status_code == 400

    @classmethod
    def teardown_class(cls) -> None:
        """Clean up after all tests"""
        # Clean up Portfolios
        LOGGER.info("Test Portfolio Teardown Class")
        for portfolio_gid in cls.portfolio_list:
            url_delete_portfolio = f"{url_base}portfolios/{portfolio_gid}"
            LOGGER.debug(f"=> Delete Portfolio Fixture: {url_delete_portfolio}")
            response = requests.delete(url=url_delete_portfolio, headers=headers)
            LOGGER.debug(f"=> STATUS CODE: {response.status_code}")
            if response.status_code == 200:
                LOGGER.debug(f"=> Portfolio with GID {portfolio_gid} deleted")
