import logging
import time
from datetime import datetime
import pytest
import re
from Pages.CollectScreen import CollectScreenClass
from TestCase.BaseTest import BaseTest
from Utilities.LogUtil import Logger

log = Logger(__name__, logging.INFO)
curr_date = datetime.now().strftime("%d")


@staticmethod
def normalize_string(s):
    s = s.replace('\n', '').replace('\xa0', ' ').strip()
    s = re.sub(r'\s+', ' ', s)
    return s


class Test_CollectScreen(BaseTest):

    def test_send_bulkInvoices(self):
        collect = CollectScreenClass(self.driver)
        self.driver.refresh()
        collect.collect_screen()
        collect.bulk_message.send_bulk_msg()
        collect.bulk_message.comm_radio_bttn("Email")
        collect.bulk_message.select_company_for_bulk_msg(is_checked=0)
        num_of_selected_comp = collect.bulk_message.select_company_for_bulk_msg(is_checked=1)
        assert num_of_selected_comp == "Selected 4 items"
        collect.bulk_message.click_to_send()

    @pytest.mark.skip
    def test_export(self):
        collect = CollectScreenClass(self.driver)
        collect.collect_screen()

    @pytest.mark.skip
    def test_summary_of_dues(self):
        collect = CollectScreenClass(self.driver)
        collect.collect_screen()
        outstanding = collect.summary_dues.nudge_data("OUTSTANDING", "OUTSTANDING DEBTORS")
        overDue = collect.summary_dues.nudge_data("OVERDUE", "OUTSTANDING DEBTORS")
        advance_paid = collect.summary_dues.nudge_data("ADVANCE PAID", "ADVANCE PAID VENDORS")
        outstanding_in_branch = collect.summary_dues.nudge_data("OUTSTANDING IN BRANCH", "NO. OF BRANCHES")

        expected_outstanding = {"OUTSTANDING": "₹3,24,90,019", "OUTSTANDING DEBTORS": "25"}
        expected_overdue = {"OVERDUE": "₹3,24,90,019", "OUTSTANDING DEBTORS": "25"}
        expected_advance_paid = {"ADVANCE PAID": "₹1,10,83,748", "ADVANCE PAID VENDORS": "5"}
        expected_outstanding_in_branch = {"OUTSTANDING IN BRANCH": "₹0", "NO. OF BRANCHES": "0"}

        assert outstanding == expected_outstanding, f"Expected {expected_outstanding}, but got {outstanding}"
        assert overDue == expected_overdue, f"Expected {expected_overdue}, but got {overDue}"
        assert advance_paid == expected_advance_paid, f"Expected {expected_advance_paid}, but got {advance_paid}"
        assert outstanding_in_branch == expected_outstanding_in_branch, f"Expected {expected_outstanding_in_branch}, but got {outstanding_in_branch}"

    def test_search_for_comp(self):
        collect = CollectScreenClass(self.driver)
        collect.collect_screen()
        searched_comp = collect.search.search_company("Flexi Flow Polymers LLP")
        assert searched_comp == "Flexi Flow Polymers LLP", f"searched company and expected company is not same"
        time.sleep(10)

    def test_od_filter(self):
        collect = CollectScreenClass(self.driver)
        collect.collect_screen()
        default_filter_value = collect.search.default_filter_value("Overdue grouping frequency")
        assert default_filter_value == "15 days"
        collect.search.overdue_grouping_frequency(30)
        selected_filter_value = collect.search.default_filter_value("Overdue grouping frequency")
        assert selected_filter_value == "30 days"

    def test_priority_filter(self):
        collect = CollectScreenClass(self.driver)
        collect.collect_screen()
        collect.search.overdue_grouping_frequency(15)
        filter_options = {
            "All": "25",
            "Short Pmt": "0",
            "High Priority": "2",
            "Medium Priority": "2",
            "Low Priority": "0",
            "Bad Debt": "21"
        }

        for option, expected_data in filter_options.items():
            collect.search.filter_via_priority(option)
            outstanding_debtor = collect.summary_dues.nudge_data("OVERDUE", "OUTSTANDING DEBTORS")[
                "OUTSTANDING DEBTORS"]
            assert outstanding_debtor == expected_data

    @pytest.mark.skip
    def test_acc_manager_filter(self):
        collect = CollectScreenClass(self.driver)
        collect.collect_screen()
        collect.search.filter_via_priority("All")
        collect.search.filter_via_account_manager("Mitendra")
        selected_acc_manager = collect.search.default_filter_value("Filter via Account Manager")
        assert selected_acc_manager == "Mitendra"

    @pytest.mark.skip
    def test_filter_via_group(self):
        collect = CollectScreenClass(self.driver)
        collect.collect_screen()
        collect.search.filter_via_groups("Filter via Manager Groups", "Show All")
        time.sleep(5)

    def test_aging_summary_and_Pagination(self):
        collect = CollectScreenClass(self.driver)
        collect.collect_screen()
        collect.aging_summary()
        collect.page_filter("next")
        time.sleep(2)
        collect.priority("Santosh Plastic", "High")
        time.sleep(2)
        collect.page_filter("previous")
        time.sleep(2)
        collect.detailed_summary()

    def test_send_reminder_to_customer(self):
        collect = CollectScreenClass(self.driver)
        collect.collect_screen()
        collect.add_task("Flexi Flow Polymers LLP", 15000, curr_date, "credftest@gmail.com", "8287381094")
        collect.set_reminder("Flexi Flow Polymers LLP", "credftest@gmail.com", "8287381094")
        sent_data = collect.reminder_type.send_email("Flexi Flow Polymers LLP")

        received = collect.reminder_type.get_email_data("j1605@credflow.co", "credftest@gmail.com",
                                                        "[J D Polymers34 - (from 1-Apr-2019)] Pending Payment Reminder - Flexi Flow Polymers LLP",
                                                        extract_links=False, extract_text=True,
                                                        extract_table=True, check_attachments=False)

        sent_template = [normalize_string(s) for s in sent_data["preview_content"]]
        received_template = [normalize_string(s) for s in received["texts"]]
        assert sent_template == received_template, f"sent template is not equal to received_template"
        assert sent_data["preview_table"] == received["tables"], f"sent data and received data is not same"
