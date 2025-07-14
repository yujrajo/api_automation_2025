import requests
from utils.logger import get_logger


LOGGER = get_logger(__name__, "DEBUG")


class RestClient:
    def __init__(self) -> None:
        """Initiate requests session"""
        self.session = requests.Session()

    def send_request(self, method_name: str, url: str, headers: dict, body=None) -> dict:
        """Sends the Request method and returns a modified Response

        Args:
            method_name (str): HTTP method
            url (str): Target URL
            headers (dict): Cantains the headers for the request
            body (dict, optional): Dictionary with the Request Body. Defaults to None.

        Returns:
            dict: Updated Response
        """

        response_updated = {}
        methods = {
            "GET": self.session.get,
            "POST": self.session.post,
            "PUT": self.session.put,
            "DELETE": self.session.delete,
        }
        try:
            response = methods[method_name](url=url, headers=headers, json=body)
            response.raise_for_status()

            response_updated["body"] = response.json() if response.text else {"message": "No body content"}
            response_updated["status_code"] = response.status_code
            response_updated["headers"] = dict(response.headers)
            response_updated["time"] = response.elapsed.total_seconds()
            response_updated["request"] = response.request

        except requests.exceptions.HTTPError as e:
            LOGGER.error(f"HTTP Error: {e}")
            response_updated["body"] = response.json() if response.text else {"message": "HTTP Error"}
            response_updated["status_code"] = response.status_code
            response_updated["headers"] = dict(response.headers)

        except requests.exceptions.ConnectionError as e:
            LOGGER.error(f"Connection Error: {e}")
            response_updated["body"] = response.json() if response.text else {"message": "Connection Error"}
            response_updated["status_code"] = response.status_code
            response_updated["headers"] = {}

        except requests.exceptions.RequestException as e:
            LOGGER.error(f"Request Exception: {e}")
            response_updated["body"] = response.json() if response.text else {"message": "Request Failed"}
            response_updated["status_code"] = response.status_code
            response_updated["headers"] = {}

        return response_updated
