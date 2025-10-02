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
    def test_forgot_password(self):
        self.authorization_page.open()
        self.authorization_page.click_link_forgot_password()
        self.authorization_page.click_button_cancel_forgot_password()

    @pytest.mark.smoke
    def test_negative_authorization_personal_account(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_wrong_password(f"Test {random.randint(1, 100)}")
        self.authorization_page.click_eye_button()
        self.authorization_page.click_enter_button()
        self.authorization_page.make_screenshot("Input Error")
        self.authorization_page.negative_authorization()


    @pytest.mark.smoke
    def test_authorization_personal_account(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_wrong_password(f"Test {random.randint(1, 100)}")
        time.sleep(1)
        self.authorization_page.click_eye_button()
        time.sleep(1)
        self.authorization_page.delete_wrong_password()
        time.sleep(1)
        self.authorization_page.showing_enter_password(self.login.PASSWORD)
        self.authorization_page.checkbox_remember_me()
        time.sleep(1)
        self.authorization_page.click_enter_button()
        time.sleep(1)
        self.online_tab.is_opened_online_tab()
        time.sleep(1)


    # Лучше сделать самым последним проверку - таймаут 15 минут
    # def test_five_wrong_attempts(self):
    #     self.authorization_page.open()
    #     self.authorization_page.enter_login(self.login.LOGIN)
    #     self.authorization_page.enter_wrong_password(f"Test {random.randint(1, 100)}")
    #     self.authorization_page.five_wrong_attempts()
    #     self.authorization_page.make_screenshot("Error five wrong attempts")





