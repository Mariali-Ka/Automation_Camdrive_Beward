import random
import time
import allure
import pytest
from base.base_test import BaseTest


# авторизация и выход с ЛК
class TestAuthorization:

     @allure.feature("Profile Functionality")
     class TestExitPersonalAccount(BaseTest):

        @allure.title("Exit personal account")
        @allure.severity("Critical")
        @pytest.mark.smoke
        def test_exit_personal_account(self):
           self.host_page.open()
           self.host_page.enter_login(self.login.LOGIN)
           self.host_page.enter_password(self.login.PASSWORD)
           self.host_page.click_enter_button()
           self.online_tab.open()
           self.online_tab.click_button_exit()