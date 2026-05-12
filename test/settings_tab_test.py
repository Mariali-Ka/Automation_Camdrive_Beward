import random
import time
import allure
import pytest
from base.base_test import BaseTest


@allure.feature("Settings Tab Functionality")
class  TestSettingsTab(BaseTest):

    @pytest.mark.smoke
    def test_go_to_settings_tab(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.settings_tab.click_go_to_settings_tab()
