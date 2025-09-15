import random
import time
import allure
import pytest
from base.base_test import BaseTest


# авторизация и выход с ЛК


@allure.feature("Profile Functionality")
class TestAuthorizationPersonalAccount(BaseTest):

    @allure.title("Authorization personal account")
    @allure.severity("Critical")
    @pytest.mark.smoke
    def test_authorization_personal_account(self):
        self.authorization_page.open()
        self.authorization_page.click_link_forgot_password()
        self.authorization_page.click_button_cancel_forgot_password()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_wrong_password(f"Test {random.randint(1, 100)}")
        self.authorization_page.click_eye_button()
        self.authorization_page.click_enter_button()
        self.authorization_page.make_screenshot("Input Error")
        self.authorization_page.close_information_incorrect_data()
        self.authorization_page.delete_wrong_password()
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_eye_button()
        self.authorization_page.checkbox_remember_me()
        self.authorization_page.click_enter_button()
        self.online_tab.is_opened_online_tab()




