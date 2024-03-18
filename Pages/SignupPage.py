import time

from Pages.BasePage import BaseClass
from Utilities import email_utill


class SignUpClass(BaseClass):
    def __init__(self, driver):
        super().__init__(driver)

    def fill_SignUpForm(self, name, email, phone, password, sw,referal=None):
        self.input_text("Name_xpath", name)
        self.input_text("inputEmail_xpath", email)
        self.input_text("inputPhone_xpath", phone)
        self.input_text("inputPass_xpath", password)
        self.input_text("referal_xpath", referal)
        self.click("accountingSWDrp_xpath")
        sw_list = self.get_ele_from_list("accSw_xpath")
        for item in sw_list:
            if item == sw:
                item.click()
                break
        TnC_checkBox=self.get_web_ele("TnC_xpath")
        if not TnC_checkBox.is_selected():
            TnC_checkBox.click()

        self.click("registerBttn_xpath")

