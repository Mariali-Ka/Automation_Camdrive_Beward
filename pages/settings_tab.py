import time
import random
import allure
import datetime
import string
from selenium.common import TimeoutException

from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

class SettingsTab(BasePage):

    PAGE_URL = Links.SETTING_TARIFFS_TAB

    TAB_SETTINGS = ("xpath", "//a[text()='Настройки']")  # вкладка Настройки

    # ОТКРЫВАЕМ ВКЛАДКУ НАСТРОЙКИ
    @allure.step("Go to settings tab")
    def click_go_to_settings_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.TAB_SETTINGS)).click()