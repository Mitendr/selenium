import logging
import time
from Pages.BasePage import BaseClass
from Utilities import email_utill
from Utilities.LogUtil import Logger
from Pages.LoginPage import LoginClass

log = Logger(__name__, logging.INFO)


class DashBoardClass(BaseClass):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = self.Header(self)
        self.KYC = self.KYC_GetStarted(self)
        self.businessOverview = self.BusinessOverview(self)
        self.cashflow = self.CashFlow(self)

    def Login(self):
        login = LoginClass(self.driver)
        login.fill_loginForm("mitendra.kumar@credflow.in", "ironman@12")
        self.wait_Until_element_visible("Header_xpath")

    class Header:
        def __init__(self, parent):
            self.parent = parent

        def companies_list(self):
            self.parent.click("Header_xpath", "[1]")
            time.sleep(5)
            elements = self.parent.get_ele_from_list("companies_list_xpath")
            org_list = []
            for el in elements:
                org_list.append(el.text)
            lst_of_companies = ['J D Polymers34 - (from 1-Apr-2019)', 'Testing', 'Dairy Products Pvt Ltd 3',
                                'Dairy Product ERP', 'Dairy Product Farms Pvt. Ltd. ERP 9',
                                'J D Polymers34 - (from 1-Apr-2017)']
            if org_list == lst_of_companies:
                assert True
            else:
                assert False

        def set_contactDetails(self):
            assert self.parent.is_clickable("Header_xpath", "[2]")

        def tally_sync_time(self):
            self.parent.hover("Header_xpath", "[3]")
            time.sleep(5)

        def help(self):
            self.parent.hover("Header_xpath", "[4]")
            time.sleep(5)

        def user_permission(self):
            self.parent.hover("Header_xpath", "[5]")
            time.sleep(5)

        def setting(self):
            self.parent.hover("Header_xpath", "[6]")
            time.sleep(5)

        def user(self):
            self.parent.click("Header_xpath", "[7]")
            time.sleep(5)

    class KYC_GetStarted:
        def __init__(self, parent):
            self.parent = parent

        def kyc_msg(self):
            kyc_message = ("Hello ,Before you may use payments, your KYC must be completed, Please complete the "
                           "application with the required documents.")
            msg_elements = self.parent.get_ele_from_list("KYC_MSG_xpath")
            msg = ""
            for ele in msg_elements:
                msg = msg + ele.text
            assert msg == kyc_message

        def kyc_button(self):
            self.parent.click("Get_started_Button_xpath")

    class BusinessOverview:
        def __init__(self, parent):
            self.parent = parent

        def new_invoices_due(self):
            locator = self.parent.form_dynamic_locator("Nudges_data_xpath", "New Invoices Due")
            web_ele = self.parent.get_web_ele(locator)
            total_number_of_invoices_gettingDueToday = web_ele.text
            log.logger.info(f"total_number_of_invoices_gettingDueToday is '{total_number_of_invoices_gettingDueToday}'")
            self.click_nudgeArrow("New Invoices Due")
            time.sleep(5)
            self.parent.navigate_back()
            time.sleep(2)
            self.parent.hover("Nudge_Info_xpath", "New Invoices Due")
            time.sleep(2)
            self.parent.hover("BusinessOverviewMsg_xpath")

        def task_due_today(self):
            locator = self.parent.form_dynamic_locator("Nudges_data_xpath", "Task Due Today")
            total_number_of_taskDueToday = self.parent.get_web_ele(locator).text
            log.logger.info(f"total_number_of_invoices_gettingDueToday is '{total_number_of_taskDueToday}'")

        def bad_debtors(self):
            locator = self.parent.form_dynamic_locator("Nudges_data_xpath", "Bad Debtors")
            total_number_of_BadDebtors = self.parent.get_web_ele(locator).text
            log.logger.info(f"total_number_of_invoices_gettingDueToday is '{total_number_of_BadDebtors}'")

        def reminders_sent_this_month(self):
            locator = self.parent.form_dynamic_locator("Nudges_data_xpath", "Reminders Sent (This Month)")
            total_number_of_remindersSent = self.parent.get_web_ele(locator).text
            log.logger.info(f"total_number_of_invoices_gettingDueToday is '{total_number_of_remindersSent}'")

        def click_nudgeArrow(self, dynamic_value):
            self.parent.click("Nudge_arrow_xpath", dynamic_value)

    class CashFlow:
        def __init__(self, parent):
            self.parent = parent

        def receivables(self):
            receivable_amount = self.parent.get_text("Cash_flow_amount_xpath", "Receivables")
            log.logger.info(f"receivable amount is {receivable_amount}")

        def payables(self):
            receivable_amount = self.parent.get_text("Cash_flow_amount_xpath", "Payables")
            log.logger.info(f"receivable amount is {receivable_amount}")

        def currentInventory(self):
            receivable_amount = self.parent.get_text("Cash_flow_amount_xpath", "Current Inventory")
            log.logger.info(f"receivable amount is {receivable_amount}")

        def cashAndBankBal(self):
            receivable_amount = self.parent.get_text("Cash_flow_amount_xpath", "Cash & Bank Bal")
            log.logger.info(f"receivable amount is {receivable_amount}")

        def receivable_trend(self, duration):
            self.parent.click("Receivable_amt_drp_xpath")
            if duration == "Past 6 Months":
                self.parent.click("filter_option_xpath","Past 6 Months")
            elif duration == "Past 12 Months":
                self.parent.click("filter_option_xpath","Past 12 Months")

        def projected_collection(self):
            pass

        def agingSummary(self):
            pass

        def top_customers(self):
            pass
