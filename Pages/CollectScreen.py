import logging
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from Pages.BasePage import BaseClass
from Utilities import email_utill
from Utilities.LogUtil import Logger
from Pages.LoginPage import LoginClass
from Utilities.EmailUtil import EmailReader

log = Logger(__name__, logging.INFO)


class CollectScreenClass(BaseClass):
    def __init__(self, driver):
        super().__init__(driver)
        self.search = self.Search(self)
        self.reminder_type = self.ReminderType(self)
        self.summary_dues = self.SummaryDues(self)
        self.bulk_message = self.BulkMsg(self)
        # self.reminder_validation=self.ReminderValidation(self)

    def Login(self):
        login = LoginClass(self.driver)
        login.fill_loginForm("mitendra.kumar@credflow.in", "ironman@12")
        self.wait_Until_element_visible("Header_xpath")

    @staticmethod
    def email_reader():
        read_email = EmailReader("credftest@gmail.com", "exxo roos pemw lgxr")
        return read_email

    def collect_screen(self):
        self.click("collect_tab_xpath")
        self.rating_pop_up()
        time.sleep(5)

    class BulkMsg:
        def __init__(self, parent):
            self.parent = parent

        def send_bulk_msg(self):
            self.parent.click("send_bulk_msg_xpath")
            time.sleep(2)

        def comm_radio_bttn(self, comm_mode):
            mode = self.parent.get_web_ele("mode_of_comm_xpath", comm_mode)
            if not mode.is_selected():
                mode.click()
                time.sleep(5)

        def click_to_send(self):
            self.parent.click(("button_xpath", "Send"))

        def select_company_for_bulk_msg(self, is_checked=0):
            checkbox = self.parent.get_web_ele("checkbox_bulk_reminder_xpath")
            send_button = self.parent.get_web_ele("button_xpath", "Send")
            if is_checked == 0:
                assert not checkbox.is_selected(), "Checkbox should not be selected"
                assert not send_button.is_enabled(), "Send button should be disabled"
                log.logger.info(f"{checkbox} is not selected so {send_button} is disabled")
            elif is_checked == 1:
                checkbox.click()
                assert send_button.is_enabled()
                numb_of_selected_comp = send_button.find_element(By.XPATH, "./following-sibling::span").text
                log.logger.info(f"Number of selected companies: {numb_of_selected_comp}")
                return numb_of_selected_comp

    def export(self):
        self.click("Export_xpath")

    def rating_pop_up(self):
        self.click("feedback_xpath")
        time.sleep(2)

    def page_filter(self, navigation):
        pagination = navigation.title() + " Page"
        if navigation.title() == "Next":
            if self.is_clickable("pagination_xpath", pagination):
                self.click("pagination_xpath", pagination)
                log.logger.info(f"clicking in {pagination} button")
            else:
                log.logger.info(f"{pagination} button in not clickable")
                assert False
        elif navigation.title() == "Previous":
            if self.is_clickable("pagination_xpath", pagination):
                self.click("pagination_xpath", pagination)
                log.logger.info(f"clicking in {pagination} button")
            else:
                log.logger.info(f"{pagination} button in not clickable")
                assert False

    def detailed_summary(self):
        self.click("Detailed_summary_xpath")

    def aging_summary(self):
        self.click("Aging_summary_xpath")

    def priority(self, comp_name, priority):
        drp_ele = self.get_web_ele("priority_xpath", comp_name)
        drp = Select(drp_ele)
        option = drp.options
        for ops in option:
            if ops.text == priority:
                ops.click()
                log.logger.info(f"selecting priority {ops.text}")
                break

    def reminder_setup(self, email, phone):
        self.clearFields("email1_xpath")
        self.input_text("email1_xpath", email)
        time.sleep(5)
        self.clearFields("phone1_xpath")
        self.input_text("phone1_xpath", phone)
        time.sleep(5)
        self.click("advance_setting_xpath")
        time.sleep(5)
        self.click("payment_terms_xpath")
        self.click("select_payment_term_xpath")
        self.click("accountManager_name_xpath")
        email_check_box = self.get_web_ele("mode_of_comm_xpath", "Email")
        if not email_check_box.is_selected():
            self.click("mode_of_comm_xpath", "Email")
        time.sleep(5)
        self.click("get_back_from_advance_settings_xpath")
        self.click("button_xpath", "Submit form")

    def set_reminder(self, company_name, email, phone):
        self.click("Task_AutoReminder_setup_xpath", company_name)
        self.reminder_setup(email, phone)

    def add_task(self, company_name, amount, date, email, phone):

        self.click("Task_AddTask_setup_xpath", company_name)
        # amount promise to pay
        self.input_text("promise_to_pay_xpath", amount)
        # select date
        self.click("calendar_xpath")
        time.sleep(2)
        log.logger.info(date)
        date_elements = self.get_ele_from_list("date_xpath", int(date))
        for date_ele in date_elements:
            if date_ele.is_enabled():
                log.logger.info(date_ele)
                date_ele.click()
                break

        self.click("Add_task_details_xpath")
        self.input_text("Add_task_details_xpath", "payment reminder")

        if self.is_element_present("Add_contact_details_xpath"):
            self.click("Add_contact_details_xpath")
            self.reminder_setup(email, phone)
            log.logger.info(f"Added contact details: {email}, {phone}")

        self.click("button_xpath", "Submit", [2])
        # self.driver.find_element(By.XPATH,"(//*[text()='Submit']/parent::button)[2]").click()

    class SummaryDues:
        def __init__(self, parent):
            self.parent = parent

        def nudge_data(self, nudge_name, resultant_nudge):
            result = {f"{nudge_name}": [], f"{resultant_nudge}": []}
            self.parent.click("Nudge_data_xpath", nudge_name)
            amount = self.parent.get_text("Nudge_data_xpath", nudge_name)
            debtors = self.parent.get_text("Nudge_data_xpath", resultant_nudge)
            result[f"{nudge_name}"] = amount
            result[f"{resultant_nudge}"] = debtors
            return result

    class Search:
        def __init__(self, parent):
            self.parent = parent

        def search_company(self, comp_name):
            search_field = self.parent.get_web_ele("search_for_company_xpath")
            search_field.send_keys(comp_name)
            search_field.send_keys(Keys.ENTER)
            log.logger.info("pressing the Enter keyboard button")
            company_name = self.parent.get_text("company_name_xpath")
            log.logger.info(f"list of search companies {company_name}")

            return company_name

        def default_filter_value(self, filter_name):
            default_value = self.parent.get_text("default_value_of_filter_xpath", filter_name)
            return default_value

        def overdue_grouping_frequency(self, day_freq):
            self.parent.click("filter_xpath", "Overdue grouping frequency")
            frequency = f"{str(day_freq)} days"
            self.parent.click("select_from_list_xpath", frequency)

        def filter_via_priority(self, priority):
            self.parent.click("filter_xpath", "Filter via Priority")
            self.parent.click("select_from_list_xpath", priority)

        def filter_via_account_manager(self, name):
            self.parent.click("filter_xpath", "Filter via Account Manager")
            self.parent.click("select_from_list_xpath", name)

        def filter_via_groups(self, group_name, checkBox_name):
            self.parent.click("filter_via_groups_xpath")
            if group_name == "Filter via Manager Groups":
                self.parent.click("select_filter_via_group_xpath=", group_name)
                self.parent.click("select_filter_via_group_xpath=", checkBox_name)
            elif group_name == "Filter via Tally Groups":
                self.parent.click("select_filter_via_group_xpath=", group_name)
                self.parent.click("select_filter_via_group_xpath=", checkBox_name)

    class ReminderType:
        def __init__(self, parent):
            self.parent = parent

        def whatsapp(self, company_name):
            self.parent.click("whatsApp_Reminder_xpath", company_name)

        def send_email(self, company_name):
            result = {"preview_content": [], "preview_table": []}
            overdue_amount = self.parent.get_text("overdue_amount_xpath", company_name)
            log.logger.info(overdue_amount)
            self.parent.click("Email_Reminder_xpath", company_name)
            time.sleep(5)
            self.parent.click("show_preview_xpath")
            time.sleep(5)
            preview_text = self.parent.get_text("preview_amount_xpath")
            preview_content = self.parent.get_text("preview_text_xpath")
            result["preview_content"].append(preview_content)
            log.logger.info(f"preview table data : {result['preview_table']}")
            total_row = len(self.parent.get_ele_from_list("table_row_xpath"))
            total_col = len(self.parent.get_ele_from_list("table_header_xpath"))
            # Table Header
            header = []
            for i in range(1, total_col + 1):
                header_data = self.parent.driver.find_element(By.XPATH, f"//tr/th[{i}]").text
                header.append(header_data)

            table_data = []
            for i in range(1, total_row):
                row_data = []
                for j in range(1, total_col + 1):
                    data = self.parent.driver.find_element(By.XPATH, f"//tr[{i}]/td[{j}]").text
                    row_data.append(data)
                table_data.append(row_data)
            result["preview_table"].append((header, table_data))
            log.logger.info(f"preview table data : {result['preview_table']}")
            self.parent.click("back_from_preview_xpath")
            time.sleep(2)
            self.parent.click("button_xpath", "Send Mail")
            time.sleep(2)
            return result

        def get_email_data(self, sender, to, subject, is_seen=0, extract_links=False, extract_text=False,
                           extract_table=False, check_attachments=False):
            email_reader = self.parent.email_reader()
            EmailData = email_reader.read_emails(sender, to, subject, is_seen, extract_links,
                                                 extract_text, extract_table, check_attachments)
            log.logger.info(f"Email data is: {EmailData}")
            return EmailData

        def ivr(self, company_name):
            self.parent.click("IVR_Reminder_xpath", company_name)

        def sms(self, company_name):
            self.parent.click("sms_Reminder_xpath", company_name)
