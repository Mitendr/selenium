import logging
import time
from Pages.BasePage import BaseClass
from Utilities import email_utill
from Utilities.LogUtil import Logger

log = Logger(__name__, logging.INFO)


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

    def verify_title_of_the_Page(self, actualTitle):
        title = self.driver.title
        assert title == actualTitle

    def forgetPassword(self, email_id):
        self.click("forgetPas_xpath")
        self.input_text("InputEmailToGetPass_xpath", email_id)
        self.click("resetPass_xpath")
        self.wait_Until_element_visible("resetPass_toastMsg_xpath")
        toast_msg = self.get_text("resetPass_toastMsg_xpath")
        assert toast_msg == "If your email exists in our database, a password reset link will be sent to your email"
        time.sleep(5)
        resetPassLink = email_utill.gmail_verify("credftest@gmail.com", "exxo roos pemw lgxr", "noreply@credflow.in",
                                                 "credftest@gmail.com", "Forgot Password")
        log.logger.info(f"getting verification link from email {email_id} and the link is {resetPassLink}")
        self.click(resetPassLink[0])

        time.sleep(10)




