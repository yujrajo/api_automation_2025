from utils.logger import get_logger

LOGGER = get_logger(__name__, "DEBUG")


class TestExample:
    @classmethod
    def setup_class(cls):
        """Setup class"""
        LOGGER.info("Setup class")
        API_KEY = "435793845793475932857"
        cls.header_api = {
            "Authorization": f"Bearer {API_KEY}"
        }
        LOGGER.info(f"Header API: {cls.header_api}")

    def setup_method(self) -> None:
        LOGGER.info("Setup method")

    def test_one(self):
        LOGGER.info("Test one")
        LOGGER.info(f"Header API: {self.header_api}")
        assert self.header_api

    def test_two(self):
        LOGGER.info("Test two")

    def test_three(self):
        LOGGER.info("Test three")

    def teardown_method(self):
        LOGGER.info("Teardown method")

    @classmethod
    def teardown_class(cls):
        LOGGER.info("Teardown class")
