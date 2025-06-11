import logging
import unittest
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class TestProject(unittest.TestCase):

    # fixture
    def setUp(self):
        LOGGER.info("Setup")

    def test_one(self):
        LOGGER.info("test one")

    def test_two(self):
        LOGGER.info("test two")

    def test_three(self):
        LOGGER.info("test three")

    # fixture
    def tearDown(self):
        LOGGER.info("tearDown")
