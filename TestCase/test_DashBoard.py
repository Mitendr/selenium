import time

import pytest

from TestCase.BaseTest import BaseTest
from Pages.DashBoard import DashBoardClass


# added comment

@pytest.mark.skip(reason="Skipping test_DashBoard for now")
class Test_DashBoard(BaseTest):

    def test_my_Companies(self):
        Dashboard = DashBoardClass(self.driver)
        Dashboard.Login()
        Dashboard.header.companies_list()
        time.sleep(10)
        Dashboard.header.tally_sync_time()
        Dashboard.header.help()
        Dashboard.header.user_permission()
        Dashboard.header.setting()
        Dashboard.header.user()

        Dashboard.KYC.kyc_msg()
        time.sleep(5)
        Dashboard.businessOverview.new_invoices_due()
        time.sleep(5)
        Dashboard.businessOverview.task_due_today()
        Dashboard.businessOverview.bad_debtors()
        Dashboard.businessOverview.reminders_sent_this_month()
        time.sleep(5)
        Dashboard.cashflow.receivables()
        Dashboard.cashflow.payables()
        Dashboard.cashflow.currentInventory()
        Dashboard.cashflow.cashAndBankBal()
