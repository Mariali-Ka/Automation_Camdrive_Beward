import time

import allure
import pytest
from base.base_test import BaseTest

@allure.feature("Archive Tab Functionality")
class TestArchiveTab(BaseTest):

    @pytest.mark.smoke
    def test_go_to_archive_tab(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.archive_tab.click_go_to_archive_tab()


    @pytest.mark.smoke
    def test_turn_over_calendar(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.archive_tab.click_go_to_archive_tab()
        self.archive_tab.click_go_to_one_month_ago_calendar()
        self.archive_tab.click_go_to_one_month_advance_calendar()
        self.archive_tab.is_opened_archive_tab()

    @pytest.mark.smoke
    def test_opening_calendar(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.archive_tab.click_go_to_archive_tab()
        self.archive_tab.click_checking_opening_calendar()

    @pytest.mark.smoke
    def test_selected_date_displayed_field(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.archive_tab.click_go_to_archive_tab()
        self.archive_tab.click_checking_opening_calendar()
        self.archive_tab.selected_date_displayed_field()

    @pytest.mark.smoke
    def test_select_date_time_duration_download_snippet(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.archive_tab.click_go_to_archive_tab()
        self.archive_tab.select_date_time_duration_download_snippet()

    @pytest.mark.smoke
    def test_viewing_fragment_from_camera(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.archive_tab.click_go_to_archive_tab()
        self.archive_tab.active_cameras_inside_list()
        self.archive_tab.viewing_fragment_from_camera()

    @pytest.mark.smoke
    def test_viewing_four_fragments_one_days_recording(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.archive_tab.click_go_to_archive_tab()
        self.archive_tab.active_cameras_inside_list()
        self.archive_tab.viewing_four_fragments_one_days_recording()

    @pytest.mark.smoke
    def test_view_one_fragment_record_on_each_valid_day(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.archive_tab.click_go_to_archive_tab()
        self.archive_tab.active_cameras_inside_list()
        self.archive_tab.view_one_fragment_record_on_each_valid_day()

    @pytest.mark.smoke
    def test_checking_autoplayback_fragments_from_camera(self):
        self.authorization_page.open()
        self.authorization_page.enter_login(self.login.LOGIN)
        self.authorization_page.enter_password(self.login.PASSWORD)
        self.authorization_page.click_enter_button()
        self.archive_tab.click_go_to_archive_tab()
        self.archive_tab.active_cameras_inside_list()
        self.archive_tab.checking_autoplayback_fragments_from_camera()
     
