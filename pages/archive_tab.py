import re
import time
import random
import allure
from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



class ArchiveTab(BasePage):

    PAGE_URL = Links.ARCHIVE_TAB

    TAB_ARCHIVE = ("xpath", "//a[text()='Архив']")
    FIELD_CALENDAR = ("xpath", "//div[text()='Календарь']")
    OPENING_CALENDAR = ("xpath", "//img[@alt='Выберите дату']")
    OPENING_CALENDAR_MONTH_AGO =("xpath", "//a[@title='<Пред']")
    CLICK_SELECTED_DATE = ("xpath", "//a[text()='13']")
    FIELD_INPUT_DATE = ("xpath", "//input[@id='download-date']")
    HEADING_C = ("xpath", "//th[@class='heading-c']")
    HEADING_l = ("xpath", "//th[@class='heading-l prev']")
    HEADING_R = ("xpath", "//th[@class='heading-r off']")
    HEADING_R_NEXT = ("xpath", "//th[@class='heading-r next']")

    @allure.step("Go to archive tab")
    def click_go_to_archive_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.TAB_ARCHIVE)).click()

    @allure.step("Is Opened Archive Tab")
    def is_opened_archive_tab(self):
        current_url = self.PAGE_URL
        assert current_url == Links.ARCHIVE_TAB, "Ошибка в URL, открыта не та страница"

    @allure.step("Go to one month ago calendar")
    def click_go_to_one_month_ago_calendar(self):
        self.wait.until(EC.element_to_be_clickable(self.HEADING_l)).click()

    @allure.step("Go to one month advance calendar")
    def click_go_to_one_month_advance_calendar(self):
        self.wait.until(EC.element_to_be_clickable(self.HEADING_R_NEXT)).click()

    @allure.step("Checking opening calendar")
    def click_checking_opening_calendar(self):
        self.wait.until(EC.element_to_be_clickable(self.OPENING_CALENDAR)).click()
        assert self.wait.until(EC.visibility_of_element_located(self.OPENING_CALENDAR)).is_displayed()

    def selected_date_displayed_field(self):
        self.wait.until(EC.element_to_be_clickable(self.OPENING_CALENDAR_MONTH_AGO)).click()
        self.wait.until(EC.element_to_be_clickable(self.CLICK_SELECTED_DATE)).click()
        selected_date = self.wait.until(EC.visibility_of_element_located(self.FIELD_INPUT_DATE)).get_attribute("value")
        assert re.match(r"\d{2}\.\d{2}\.\d{4}", selected_date)





