import time
import allure
from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



class OnlineTab(BasePage):

    PAGE_URL = Links.ONLINE_TAB

    BUTTON_MY_CAMERAS = ("xpath", "//li[contains(@rel, 'drive')]/ins[1]")
    BUTTON_PUBLIC_CAMERAS = ("xpath", "//li[contains(@rel, 'drive_public')]/ins")
    BUTTON_EXIT = ("xpath", "//input[@value='Выйти']")
    MY_CAMERA_ONE = ("xpath", "//li[contains(@rel, 'channel')][not(contains(@rel, 'public'))][1]")
    MY_CAMERA_TWO = ("xpath", "//li[contains(@rel, 'channel')][not(contains(@rel, 'public'))][2]")

    @allure.step("Is Opened Online Tab")
    def is_opened_online_tab(self):
        current_url = self.PAGE_URL
        assert current_url == Links.ONLINE_TAB, "Ошибка в URL, открыта не та страница"

    @allure.step("Click Button Public Cameras")
    def click_button_public_cameras(self):
        self.wait.until(EC.element_to_be_clickable(self.BUTTON_PUBLIC_CAMERAS)).click()


    @allure.step("Transposition cameras")
    def transposition_cameras(self):

        my_camera_one = self.wait.until(EC.visibility_of_element_located(self.MY_CAMERA_ONE))
        my_camera_two = self.wait.until(EC.visibility_of_element_located(self.MY_CAMERA_TWO))

        action = ActionChains(self.driver)
        action.click_and_hold(my_camera_one) \
            .move_to_element(my_camera_two) \
            .release() \
            .perform()
        time.sleep(5)

    # @allure.step("Click button exit")
    # def click_button_exit(self):
    #     self.wait.until(EC.element_to_be_clickable(self.BUTTON_EXIT)).click()