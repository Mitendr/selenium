import time

import pytest

from TestCases.BaseTest import BaseTest
from Pages.LoginPage import LoginClass
from Utilities import dataProvider


class Test_Login(BaseTest):

    @pytest.mark.parametrize("name,password", dataProvider.get_data("Login"))
    def test_01_LoginTest(self, name, password):
        Login = LoginClass(self.driver)
        Login.fill_loginForm(name, password)
        Login.validateErrorMsg(name, password)
        time.sleep(5)
