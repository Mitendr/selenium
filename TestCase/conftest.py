import time

import certifi
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import ssl
from dotenv import load_dotenv
import os

load_dotenv()

# SELENIUM_URL = os.getenv('SELENIUM_URL', 'http://localhost:4444/wd/hub')
SELENIUM_URL = os.getenv('SELENIUM_URL')
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')

client = WebClient(token=SLACK_TOKEN, ssl=False)
ssl_context = ssl.create_default_context(cafile=certifi.where())
client = WebClient(token=SLACK_TOKEN, ssl=ssl_context)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


def send_slack_message(message, attachment_path=None):
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        client = WebClient(token=SLACK_TOKEN, ssl=ssl_context)

        response = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=message
        )
        assert response["ok"]
        print("File sent successfully!")
        if attachment_path:
            client.files_upload(
                channels=SLACK_CHANNEL,
                file=attachment_path,
                title="Screenshot.png"
            )
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e.response['error']}")
    except Exception as e:
        print(f"Unexpected error: {e}")


#
# @pytest.fixture(scope="function")
# def selenium_driver(request):
#     chrome_options = Options()
#     chrome_options.add_argument("--disable-notifications")
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--no-sandbox')
#
#     driver = webdriver.Remote(
#         command_executor=SELENIUM_URL,
#         options=chrome_options
#     )
#
#     driver.get("https://app.credflow.in/login")
#     driver.maximize_window()
#     driver.implicitly_wait(20)
#
#     request.cls.driver = driver
#     yield driver
#     driver.quit()


@pytest.fixture(scope="function")
def selenium_driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://app.credflow.in/login")
    driver.maximize_window()
    driver.implicitly_wait(20)
    request.cls.driver = driver
    yield driver
    driver.quit()


def extract_error_message(longrepr):
    try:
        if hasattr(longrepr, 'reprcrash'):
            return longrepr.reprcrash.message
        elif isinstance(longrepr, str):
            return longrepr
        else:
            return str(longrepr)
    except Exception as e:
        return f"Error extracting message: {e}"


@pytest.fixture()
def log_on_failure(request, selenium_driver):
    yield
    item = request.node
    driver = selenium_driver
    if item.rep_call.failed:
        screenshot_path = f"/tmp/screenshot_{int(time.time())}.png"
        driver.save_screenshot(screenshot_path)
        allure.attach(driver.get_screenshot_as_png(), name="screenshot", attachment_type=AttachmentType.PNG)
        test_name = item.name
        error_message = extract_error_message(item.rep_call.longrepr)
        message = f"Test: {test_name}\nBug: Sanity BUG\nError: {error_message}"
        send_slack_message(message, screenshot_path)
        os.remove(screenshot_path)
