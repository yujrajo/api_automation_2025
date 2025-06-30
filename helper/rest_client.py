import requests
from utils.logger import get_logger


LOGGER = get_logger(__name__, "DEBUG")

# it is only used to do api calls and it is not use everywhere like the logger, so it is a helper
class RestClient:
    def __init__(self) -> None:
        self.session = requests.Session()

    def send_request(self, method_name, url, headers, body=None):
        response_updated = {}
        methods = {
            "GET": self.session.get,
            "POST": self.session.post,
            "PUT": self.session.put,
            "DELETE": self.session.delete,
        }
        try:
            response = methods[method_name](url=url, headers=headers, json=body)
            # if an error status code is returned that stops the execution
            # with this I can make the execution to continue
            response.raise_for_status()
            # if no error status code were caught execute:
            # for example in Todoist the delete retunrs an empty body that cannot be converted to json
            # so we create the "message": "No body content"
            response_updated["body"] = response.json() if response.text else {"message": "No body content"}
            response_updated["status_code"] = response.status_code
            response_updated["headers"] = dict(response.headers)
            # LOGGER.debug(f"=> RESPONSE: {response_updated}")

        except requests.exceptions.HTTPError as e:
            LOGGER.error(f"HTTP Error: {e}")
            response_updated["body"] = response.json() if response.text else {"message": "HTTP Error"}
            response_updated["status_code"] = response.status_code
            response_updated["headers"] = dict(response.headers)
            # LOGGER.debug(f"=> RESPONSE: {response_updated}")
        except requests.exceptions.ConnectionError as e:
            LOGGER.error(f"Connection Error: {e}")
            response_updated["body"] = response.json() if response.text else {"message": "Connection Error"}
            response_updated["status_code"] = response.status_code
            response_updated["headers"] = {}
            # LOGGER.debug(f"=> RESPONSE: {response_updated}")
        except requests.exceptions.RequestException as e:
            LOGGER.error(f"Request Exception: {e}")
            response_updated["body"] = response.json() if response.text else {"message": "Request Failed"}
            response_updated["status_code"] = response.status_code
            response_updated["headers"] = {}
            # LOGGER.debug(f"=> RESPONSE: {response_updated}")
        # add headers, response empty,  request headers. Things that I need
        return response_updated
