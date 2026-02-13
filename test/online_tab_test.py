import random
import time
import allure
import pytest
from base.base_test import BaseTest



#  перенос камер в списке


@allure.feature("Online Tab Functionality")
class TestOnlineTab(BaseTest):

    @pytest.mark.smoke
    def test_transposition_cameras(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.online_tab.click_button_public_cameras()
        self.online_tab.transposition_cameras()

    @pytest.mark.smoke
    def test_exit_personal_account(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.online_tab.click_button_exit()

    @pytest.mark.smoke
    def test_open_new_window(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.online_tab.open_new_window()
        self.online_tab.make_screenshot("Подтверждение открытия второго окна")

    @pytest.mark.smoke
    def test_online_verification(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.online_tab.main()

    @pytest.mark.smoke
    def test_execute_negative_camera_add(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.online_tab.execute_negative_camera_add()

    @pytest.mark.smoke
    def test_click_random_inactive_camera(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.online_tab.click_random_inactive_camera()

    @pytest.mark.smoke
    def test_attempting_delete_camera(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.online_tab.click_random_inactive_camera()
        self.online_tab.attempting_delete_camera()

    @pytest.mark.smoke
    def test_edit_camera_name(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.online_tab.click_random_inactive_camera()
        self.online_tab.edit_camera_name()


