import time

import pytest

from TestCases.BaseTest import BaseTest
from Pages.LoginPage import LoginClass
from Utilities import dataProvider

@pytest.mark.skip
class Test_Login(BaseTest):

    @pytest.mark.parametrize("name,password", dataProvider.get_data("Login"))
    def test_01_InvalidLoginTest(self, name, password):
        Login = LoginClass(self.driver)
        Login.fill_loginForm(name, password)
        Login.validateErrorMsg(name, password)
        time.sleep(5)

    def test_02_validLogin(self):
        Login = LoginClass(self.driver)
        Login.fill_loginForm("mitendra.kumar@credflow.in","ironman@12")
        time.sleep(2)
        Login.verify_title_of_the_Page("Tally Mobile App for Android & IOS | Tally on Mobile | Credflow | Tally ERP "
                                       "Mobile App")

    def test_03_forget_password(self):
        Login = LoginClass(self.driver)
        Login.forgetPassword("credftest@gmail.com")
