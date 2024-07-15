import logging
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.LogUtil import Logger
from Utilities import confreader

log = Logger(__name__, logging.INFO)


class BaseClass:
    def __init__(self, driver):
        self.driver = driver

    def click(self, locator, dynamic_locator=None, Index_val=None):
        if str(locator).endswith("xpath"):
            if dynamic_locator is not None or Index_val is not None:
                full_locator = self.form_dynamic_locator(locator, dynamic_locator,Index_val)
                self.driver.find_element(By.XPATH, full_locator).click()
            else:
                self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator)).click()
        elif str(locator).endswith("Name"):
            self.driver.find_element(By.CLASS_NAME, confreader.read_config("Locators", locator)).click()
        elif str(locator).endswith("id"):
            self.driver.find_element(By.ID, confreader.read_config("Locators", locator)).click()

        log.logger.info("clicking on the element " + str(locator))

    def click_with_Index(self, locator, Index):
        if str(locator).endswith("xpath"):
            self.driver.find_elements(By.XPATH, confreader.read_config("Locators", locator))[Index].click()
        elif str(locator).endswith("Name"):
            self.driver.find_elements(By.CLASS_NAME, confreader.read_config("Locators", locator))[Index].click()
        elif str(locator).endswith("id"):
            self.driver.find_elements(By.ID, confreader.read_config("Locators", locator))[Index].click()

        log.logger.info("clicking on the element " + str(locator) + "with Index" + str[Index])

    def input_text(self, locator, text, dynamic_locator=None, index_value=None):
        if str(locator).endswith("xpath"):
            if dynamic_locator is not None or index_value is not None:
                full_locator = self.form_dynamic_locator(locator, dynamic_locator, index_value)
                self.driver.find_element(By.XPATH, full_locator).send_keys(text)
            else:
                self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator)).send_keys(text)
        elif str(locator).endswith("Name"):
            self.driver.find_element(By.CLASS_NAME, confreader.read_config("Locators", locator)).send_keys(text)
        elif str(locator).endswith("id"):
            self.driver.find_element(By.ID, confreader.read_config("Locators", locator)).send_keys(text)

        log.logger.info("entering text in " + str(locator) + str(text))

    def get_text(self, locator, dynamic_value=None, index_value=None):
        if str(locator).endswith("xpath"):
            if dynamic_value is not None or index_value is not None:
                full_locator = self.form_dynamic_locator(locator, dynamic_value)
                text = self.driver.find_element(By.XPATH, full_locator).text
            else:
                text = self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator)).text
            return text
        elif str(locator).endswith("Name"):
            text = self.driver.find_element(By.CLASS_NAME, confreader.read_config("Locators", locator)).text
            return text
        elif str(locator).endswith("id"):
            text = self.driver.find_element(By.ID, confreader.read_config("Locators", locator)).text
            return text

        log.logger.info("getting attribute value from " + str(locator))

    def get_ele_from_list(self, locator, dynamic_value=None, index_val=None):
        elements = []
        if str(locator).endswith("xpath"):
            if dynamic_value is not None or index_val is not None:
                full_locator = self.form_dynamic_locator(locator, dynamic_value)
                elements = self.driver.find_elements(By.XPATH, full_locator)
            else:
                elements = self.driver.find_elements(By.XPATH, confreader.read_config("Locators", locator))

        elif str(locator).endswith("Name"):
            elements = self.driver.find_elements(By.CLASS_NAME, confreader.read_config("Locators", locator))

        elif str(locator).endswith("id"):
            elements = self.driver.find_elements(By.ID, confreader.read_config("Locators", locator))
        log.logger.info("Getting all elements from the list of elements " + str(locator))
        return elements

    def get_web_ele(self, locator, dynamic_value=None, index_val=None):
        if str(locator).endswith("xpath"):
            if dynamic_value is not None or index_val is not None:
                full_locator = self.form_dynamic_locator(locator, dynamic_value)
                element = self.driver.find_element(By.XPATH, full_locator)
            else:
                element = self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator))

        elif str(locator).endswith("Name"):
            element = self.driver.find_element(By.CLASS_NAME, confreader.read_config("Locators", locator))

        elif str(locator).endswith("id"):
            element = self.driver.find_element(By.ID, confreader.read_config("Locators", locator))

        else:
            element = self.driver.find_element(By.XPATH, locator)
        log.logger.info("getting web element " + str(locator))
        return element

    def is_clickable(self, locator, dynamic_value=None, index_val=None):
        element = None
        if str(locator).endswith("xpath"):
            if dynamic_value is not None or index_val is not None:
                full_locator = self.form_dynamic_locator(locator, dynamic_value, index_val)
                element = self.driver.find_element(By.XPATH, full_locator)
            else:
                element = self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator))
        elif str(locator).endswith("Name"):
            element = self.driver.find_element(By.CLASS_NAME, confreader.read_config("Locators", locator))
        elif str(locator).endswith("id"):
            element = self.driver.find_element(By.ID, confreader.read_config("Locators", locator))

        log.logger.info("Checking if element is enabled for click: " + str(locator))
        if element and element.is_enabled() and element.is_displayed():
            return True
        else:
            return False

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

    def form_dynamic_locator(self, static_path, dynamic_value, index_value=None):
        if str(static_path).endswith("xpath"):
            locator = confreader.read_config("Locators", static_path)
            if dynamic_value is not None:
                if "=''" in locator:
                    locator = locator.replace("=''", f"='{dynamic_value}'")
                else:
                    locator = locator.replace("{dynamic_value}", dynamic_value)
            if index_value is not None:
                if isinstance(index_value, list) and index_value:
                    index_value = index_value[0]
                if isinstance(index_value, int) and index_value > 0:
                    if locator.endswith("]"):
                        locator = locator[:locator.rfind('[')]
                    locator = f"{locator}[{index_value}]"

            return locator

    def hover(self, locator, dynamic_locator=None):
        if str(locator).endswith("xpath"):
            if dynamic_locator:
                full_locator = self.form_dynamic_locator(locator, dynamic_locator)
                element = self.driver.find_element(By.XPATH, full_locator)
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
            else:
                element = self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator))
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
        elif str(locator).endswith("id"):
            element = self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator))
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
        elif str(locator).endswith("Name"):
            element = self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator))
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
        else:
            actions = ActionChains(self.driver)
            actions.move_to_element(locator).perform()

        log.logger.info(f"Hovered over element with locator {locator}")

    def navigate_back(self):
        self.driver.back()

    def is_element_present(self, locator):
        if str(locator).endswith("xpath"):
            try:
                self.driver.find_element(By.XPATH, confreader.read_config("Locators", locator))
                return True
            except NoSuchElementException:
                return False



