import pytest


@pytest.mark.usefixtures("selenium_driver")
class BaseTest:
    pass
