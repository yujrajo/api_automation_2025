import json
import jsonschema
from utils.logger import get_logger


LOGGER = get_logger(__name__, "DEBUG")


class ValidateResponse:
    def validate_response(self, actual_response: dict, file_name: str) -> None:
        """Validates the response by comparing with a File containing the expected Response:
           Headers, Schema and Status Code

        Args:
            actual_response (dict): Response return by Server
            file_name (str): File containing expected Response
        """
        expected_response = self.read_input_data(f"src/api/input_json/{file_name}.json")

        self.validate_value(actual_response["body"], expected_response["body"], "body")
        self.validate_value(actual_response["status_code"], expected_response["status_code"], "status_code")
        self.validate_value(actual_response["headers"], expected_response["headers"], "headers")

    def validate_value(self, actual_value, expected_value, key_compare):
        """Validates different parts of the Response

        Args:
            actual_value (_type_): Actual Response field
            expected_value (_type_): Expected Response field
            key_compare (_type_): Compare one of the fields, status_code, headers, body
        """
        if key_compare == "status_code":
            assert actual_value == expected_value, f"Expected Status Code: {expected_value} but received {actual_value}"
        elif key_compare == "headers":
            assert actual_value.keys() <= expected_value.keys(), (
                f"Expected Headers: {expected_value} but received {actual_value}"
            )
        elif key_compare == "body":
            schema = False
            try:
                jsonschema.validate(instance=actual_value, schema=expected_value)
                schema = True
                LOGGER.debug("Schema is valid")
            except jsonschema.exceptions.ValidationError as e:
                LOGGER.debug(f"JSON Validator Error: {e}")
            assert schema, f"Expected body schema: {expected_value} but received {actual_value}"

    def read_input_data(self, file_name: str) -> dict:  # -> Any:
        """Reads a File and returns a dictionary with its content

        Args:
            file_name (str): File path

        Returns:
            dict: Content of the file
        """
        LOGGER.debug(f"Reading input data from {file_name}")
        with open(file_name, encoding="utf-8") as f:
            data = json.load(f)
        # LOGGER.debug(f"Content data {data}")
        return data
