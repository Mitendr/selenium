import time

from Pages.BasePage import BaseClass


class LoginClass(BaseClass):
    def __init__(self, driver):
        super().__init__(driver)

    def fill_loginForm(self, user_name, password):
        if user_name is not None:
            self.input_text("email_xpath", user_name)
        if password is not None:
            self.input_text("userpass_xpath", password)
        self.click("loginBttn_xpath")

    def validateErrorMsg(self, user_name, password):
        if user_name is None and password is None:
            assert self.get_text("EmailErrorMsg_xpath") == "Please input your email!"
            assert self.get_text("ErrorMsg2_xpath") == "Please input your Password!"

        elif user_name is None:
            assert self.get_text("EmailErrorMsg_xpath") == "Please input your email!"
        elif password is None:
            assert self.get_text("EmailErrorMsg_xpath") == "Please input your Password!"
        elif len(str(password)) < 6:
            assert self.get_text("EmailErrorMsg_xpath") == "password must be at least 6 characters"

        else:

            self.wait_Until_element_visible("toastErrMsg_xpath")
            assert self.get_text("toastErrMsg_xpath") == "Invalid email or password"
