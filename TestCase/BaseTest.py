import pytest
from selenium import webdriver
from Pages.LoginPage import LoginClass

@pytest.mark.usefixtures("selenium_driver")
class BaseTest:
    @pytest.fixture(autouse=True)
    def class_setup(self, selenium_driver):
        self.login = LoginClass(self.driver)
        self.login.fill_loginForm("mitendra.kumar@credflow.in", "ironman@12")
        self.login.wait_Until_element_visible("Header_xpath")

