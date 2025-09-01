import random
import allure
from base.base_page import BasePage
from locators.host_page_locator import ExitPersonalAccountLocator
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver import Keys

class ExitPersonalAccount(BasePage):

    PAGE_URL = Links.HOST_PAGE
    locators = ExitPersonalAccountLocator

    # LOGIN_FIELD = ("xpath", "//input[@class='input']")  # поле для ввода login
    # PASSWORD_FIELD = ("xpath", "//input[@class='input password']")  # поле для ввода password
    # ENTER_BUTTON = ("xpath", "//*[@id='login']")  # кнопка Войти


    @allure.step("Enter login")
    def enter_login(self, login):
        self.wait.until(EC.element_to_be_clickable(self.locators.LOGIN_FIELD)).send_keys(login)

    @allure.step("Enter password")
    def enter_password(self, password):
        self.wait.until(EC.element_to_be_clickable(self.locators.PASSWORD_FIELD)).send_keys(password)

    @allure.step("Click enter button")
    def click_enter_button(self):
        self.wait.until(EC.element_to_be_clickable(self.locators.ENTER_BUTTON)).click()
