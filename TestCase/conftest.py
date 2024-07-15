import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os

SELENIUM_URL = os.getenv('SELENIUM_URL', 'http://localhost:4444/wd/hub')


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope="function")
def selenium_driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Remote(
        command_executor=SELENIUM_URL,
        options=chrome_options
    )

    driver.get("https://qa-app.credflow.in/login")
    driver.maximize_window()
    driver.implicitly_wait(20)

    request.cls.driver = driver
    yield driver
    driver.quit()


# @pytest.fixture(scope="function")
# def selenium_driver(request):
#     chrome_options = Options()
#     chrome_options.add_argument("--disable-notifications")
#
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.get("https://qa-app.credflow.in/login")
#     driver.maximize_window()
#     driver.implicitly_wait(20)
#     request.cls.driver = driver
#     yield driver
#     driver.quit()

@pytest.fixture()
def log_on_failure(request, selenium_driver):
    yield
    item = request.node
    driver = selenium_driver
    if item.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(), name="screenshot", attachment_type=AttachmentType.PNG)
