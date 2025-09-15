import random
import allure
from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys


class AuthorizationPersonalAccount(BasePage):
    PAGE_URL = Links.HOST_PAGE

    LOGIN_FIELD = ("xpath", "//input[@class='input']")  # поле для ввода login
    PASSWORD_FIELD = ("xpath", "//input[@class='input password']")  # поле для ввода password
    LINK_FORGOT_PASSWORD = ("xpath", "//a[text()='Забыли пароль?']")  # ссылка восстановление пароля
    BUTTON_CANCEL_FORGOT_PASSWORD = ("xpath", "//input[@value='Отменить']")  # отменить восстановление пароля
    EYE_BUTTON = ("xpath", "//div[@title='Показать пароль']")  # кнопка глаз
    CHECKBOX_REMEMBER_ME = ("xpath", "//input[@type='checkbox']")  # чек-бокс Запомнить меня
    ENTER_BUTTON = ("xpath", "//*[@id='login']")  # кнопка Войти
    INFORMATION_INCORRECT_DATA = ("xpath", "//div[@class='closable notification s error']")
    CLOSE_INFORMATION_INCORRECT_DATA = ("xpath", "//a[@class='close']")

    @allure.step("Click Link Forgot Password")
    def click_link_forgot_password(self):
        self.wait.until(EC.element_to_be_clickable(self.LINK_FORGOT_PASSWORD)).click()

    @allure.step("Click Button Cancel Forgot Password")
    def click_button_cancel_forgot_password(self):
        self.wait.until(EC.element_to_be_clickable(self.BUTTON_CANCEL_FORGOT_PASSWORD)).click()

    @allure.step("Enter login")
    def enter_login(self, login):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_FIELD)).send_keys(login)

    def enter_wrong_password(self, wrong_password):
        with allure.step(f"enter_wrong_password '{wrong_password}"):
            first_password_field = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD))
            first_password_field.send_keys(wrong_password)
            self.password = wrong_password

    @allure.step("Close information incorrect data")
    def close_information_incorrect_data(self):
        self.wait.until(EC.element_to_be_clickable(self.CLOSE_INFORMATION_INCORRECT_DATA)).click()

    @allure.step("Delete wrong password")
    def delete_wrong_password(self):
        delete_wrong_password = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD))
        delete_wrong_password.send_keys(Keys.CONTROL + "A")
        delete_wrong_password.send_keys(Keys.BACKSPACE)

    @allure.step("Enter password")
    def enter_password(self, password):
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD)).send_keys(password)

    @allure.step("Click Eye Button")
    def click_eye_button(self):
        self.wait.until(EC.element_to_be_clickable(self.EYE_BUTTON)).click()

    @allure.step("Checkbox Remember Me")
    def checkbox_remember_me(self):
        self.wait.until(EC.element_to_be_clickable(self.CHECKBOX_REMEMBER_ME)).click()

    @allure.step("Click enter button")
    def click_enter_button(self):
        self.wait.until(EC.element_to_be_clickable(self.ENTER_BUTTON)).click()
