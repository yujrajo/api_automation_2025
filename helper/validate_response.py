import json
import jsonschema
from utils.logger import get_logger


LOGGER = get_logger(__name__, "DEBUG")

# it is only used to do validations so it is a helper
class ValidateResponse:
    def validate_response(self, actual_response,file_name) -> None:
        # we declare the expected response to verified actual-expected
        # if we have acces to the database we can create the expected response from the data in DB
        # import a json with expected
        # expected_response={}
        expected_response=self.read_input_data(f"src/api/input_json/{file_name}.json")

        self.validate_value(actual_response["body"], expected_response["body"],"body")
        self.validate_value(actual_response["status_code"], expected_response["status_code"],"status_code")
        self.validate_value(actual_response["headers"], expected_response["headers"],"headers")

    def validate_value(self, actual_value,expected_value,key_compare):
        if key_compare=="status_code":
            assert actual_value== expected_value, f"Expected Status Code: {expected_value} but received {actual_value}"
        elif key_compare=="headers":
            assert actual_value.keys() <= expected_value.keys(), f"Expected Headers: {expected_value} but received {actual_value}"
            # assert actual_value.items() <= expected_value.items(), f"Expected Headers: {expected_value} but received {actual_value}"
        elif key_compare=="body":
            schema = False
            try:
                jsonschema.validate(instance=actual_value, schema=expected_value)
                schema=True
                LOGGER.debug("Schema is valid")
            # it does not stop the execution because we are only loggin the error, now we move this to the validator
            except jsonschema.exceptions.ValidationError as e:
                LOGGER.debug(f"JSON Validator Error: {e}")
            assert schema, f"Expected body schema: {expected_value} but received {actual_value}"

    def read_input_data(self,file_name):
        LOGGER.debug(f"Reading input data from {file_name}")
        with open(file_name, encoding="utf-8") as f:
            data= json.load(f)
        LOGGER.debug(f"Content data {data}")
        return data

    # TODO me quede en el 16/06 1:20:00
