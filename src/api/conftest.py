import logging
import pytest
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

# Arrange
@pytest.fixture(scope='class')
def first_entry():
    LOGGER.warning("==> first entry fixture")
    # with scope class it will be executed once for the whole class
    return "a"

# Arrange llama al otro fixture
@pytest.fixture
def order(first_entry):
    LOGGER.warning("==> order fixture")
    return first_entry