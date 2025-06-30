from utils.logger import get_logger

LOGGER = get_logger(__name__, "DEBUG")


class TestExample:

    def test_one(self, first_entry):
        LOGGER.info(f"Test one: {first_entry}")

    def test_two(self, order):
        LOGGER.info(f"Test two: {order}")

    def test_three(self):
        LOGGER.info("Test three")
