import allure
from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC

class OnlineTab(BasePage):

    PAGE_URL = Links.ONLINE_TAB

    BUTTON_EXIT = ("xpath", "//input[@value='Выйти']") # кнопка Выйти

    @allure.step("Is Opened Online Tab")
    def is_opened_online_tab(self):
        current_url = self.PAGE_URL
        assert current_url == Links.ONLINE_TAB, "Ошибка в URL, открыта не та страница"



    # @allure.step("Click button exit")
    # def click_button_exit(self):
    #     self.wait.until(EC.element_to_be_clickable(self.BUTTON_EXIT)).click()