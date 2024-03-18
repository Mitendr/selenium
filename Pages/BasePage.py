import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.LogUtil import Logger
from Utilities import confreader

log = Logger(__name__, logging.INFO)


class BaseClass:
    def __init__(self, driver):
        self.driver = driver

    def click(self, locator):
        if str(locator).endswith("xpath"):
            self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator)).click()
        elif str(locator).endswith("Name"):
            self.driver.find_element(By.CLASS_NAME, confreader.read_config("Locators", locator)).click()
        elif str(locator).endswith("id"):
            self.driver.find_element(By.ID, confreader.read_config("Locators", locator)).click()

        log.logger.info("clicking on the element" + str(locator))

    def click_with_Index(self, locator, Index):
        if str(locator).endswith("xpath"):
            self.driver.find_elements(By.XPATH, confreader.read_config("Locators", locator))[Index].click()
        elif str(locator).endswith("Name"):
            self.driver.find_elements(By.CLASS_NAME, confreader.read_config("Locators", locator))[Index].click()
        elif str(locator).endswith("id"):
            self.driver.find_elements(By.ID, confreader.read_config("Locators", locator))[Index].click()

        log.logger.info("clicking on the element" + str(locator) + "with Index" + str[Index])

    def input_text(self, locator, text):
        if str(locator).endswith("xpath"):
            self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator)).send_keys(text)
        elif str(locator).endswith("Name"):
            self.driver.find_element(By.CLASS_NAME, confreader.read_config("Locators", locator)).send_keys(text)
        elif str(locator).endswith("id"):
            self.driver.find_element(By.ID, confreader.read_config("Locators", locator)).send_keys(text)

        log.logger.info("entering text in " + str(locator) + str(text))

    def get_text(self, locator):
        if str(locator).endswith("xpath"):
            text = self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator)).text
            return text
        elif str(locator).endswith("Name"):
            text = self.driver.find_element(By.CLASS_NAME, confreader.read_config("Locators", locator)).text
            return text
        elif str(locator).endswith("id"):
            text = self.driver.find_element(By.ID, confreader.read_config("Locators", locator)).text
            return text

        log.logger.info("getting attribute value from " + str(locator))

    def get_ele_from_list(self, locator):
        if str(locator).endswith("xpath"):
            elements = self.driver.find_elements(By.XPATH, confreader.read_config("Locators", locator))

        elif str(locator).endswith("Name"):
            elements = self.driver.find_elements(By.CLASS_NAME, confreader.read_config("Locators", locator))

        elif str(locator).endswith("id"):
            elements = self.driver.find_elements(By.ID, confreader.read_config("Locators", locator))
        log.logger.info("Getting all elements from the list of elements " + str(locator))
        return elements

    def get_web_ele(self, locator):
        if str(locator).endswith("xpath"):
            element = self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator))

        elif str(locator).endswith("Name"):
            element = self.driver.find_element(By.CLASS_NAME, confreader.read_config("Locators", locator))

        elif str(locator).endswith("id"):
            element = self.driver.find_element(By.ID, confreader.read_config("Locators", locator))
        log.logger.info("getting web element " + str(locator))
        return element

    def is_clickable(self, locator):
        if str(locator).endswith("xpath"):
            self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator)).is_enabled()

        elif str(locator).endswith("Name"):
            self.driver.find_element(By.CLASS_NAME, confreader.read_config("Locators", locator)).is_enabled()

        elif str(locator).endswith("id"):
            self.driver.find_element(By.ID, confreader.read_config("Locators", locator)).is_enabled()

        log.logger.info("checking if element is enabled for click" + str(locator))

    def wait_Until_element_visible(self, locator):
        wait = WebDriverWait(self.driver, 20)
        if str(locator).endswith("xpath"):
            wait.until(EC.visibility_of_element_located((By.XPATH, confreader.read_config("Locators", locator))))
        elif str(locator).endswith("Name"):
            wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, confreader.read_config("Locators", locator))))
        elif str(locator).endswith("id"):
            wait.until(EC.visibility_of_element_located((By.ID, confreader.read_config("Locators", locator))))

    def get_atrr(self, locator, attribute):
        if str(locator).endswith("xpath"):
            attr = self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator)).get_attribute(
                attribute)
        elif str(locator).endswith("Name"):
            attr = self.driver.find_element(By.CLASS_NAME,
                                            confreader.read_config("Locators", locator)).get_attribute(
                attribute)
        elif str(locator).endswith("id"):
            attr = self.driver.find_element(By.ID, confreader.read_config("Locators", locator)).get_attribute(
                attribute)

        log.logger.info(f"getting attribute {attribute} from  " + str(locator))
        return attr

    def capture_screenshot(self, screenshot_name):
        self.driver.save_screenshot(screenshot_name)

    def clearFields(self, locator):
        if str(locator).endswith("xpath"):
            self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator)).clear()
        elif str(locator).endswith("Name"):
            self.driver.find_element(By.CLASS_NAME, confreader.read_config("Locators", locator)).clear()
        elif str(locator).endswith("id"):
            self.driver.find_element(By.ID, confreader.read_config("Locators", locator)).clear()

        log.logger.info("clearing text from input fields" + str(locator))
