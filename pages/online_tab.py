import time
import random
import allure
from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



class OnlineTab(BasePage):

    PAGE_URL = Links.ONLINE_TAB

    BUTTON_MY_CAMERAS = ("xpath", "//li[contains(@rel, 'drive')]/ins[1]")
    BUTTON_PUBLIC_CAMERAS = ("xpath", "//li[contains(@rel, 'drive_public')]/ins")
    LIST_DEVICES = ("xpath", "//li[contains(@rel, 'channel')]")
    BUTTON_EXIT = ("xpath", "//input[@value='Выйти']")
    MY_CAMERA_ONE = ("xpath", "//li[contains(@rel, 'channel')][not(contains(@rel, 'public'))][1]")
    MY_CAMERA_TWO = ("xpath", "//li[contains(@rel, 'channel')][not(contains(@rel, 'public'))][2]")
    VIEW_SCREEN_1 = ("xpath", "//div[@id='screen_1']")
    VIEW_SCREEN_2 = ("xpath", "//div[@id='screen_2']")
    VIEW_SCREEN_3 = ("xpath", "//div[@id='screen_3']")
    VIEW_SCREEN_4 = ("xpath", "//div[@id='screen_4']")
    BUTTON_EXIT_VIEW_SCREEN_1 = ("xpath", "(//img[@title='Закрыть'])[1]")
    BUTTON_EXIT_VIEW_SCREEN_2 = ("xpath", "(//img[@title='Закрыть'])[2]")
    BUTTON_EXIT_VIEW_SCREEN_3 = ("xpath", "(//img[@title='Закрыть'])[3]")
    BUTTON_EXIT_VIEW_SCREEN_4 = ("xpath", "(//img[@title='Закрыть'])[4]")
    FORMAT_VIEW_SCREEN_1_1:1 = ("xpath", "(//img[@title='Формат 1:1'])[1]")
    FORMAT_VIEW_SCREEN_2_1:1 = ("xpath", "(//img[@title='Формат 1:1'])[2]")
    FORMAT_VIEW_SCREEN_3_1:1 = ("xpath", "(//img[@title='Формат 1:1'])[3]")
    FORMAT_VIEW_SCREEN_4_1:1 = ("xpath", "(//img[@title='Формат 1:1'])[4]")
    FORMAT_SCREEN_1_1:4 = ("xpath", "(//img[@title='Формат 1:4'])[1]")
    FORMAT_SCREEN_2_1:4 = ("xpath", "(//img[@title='Формат 1:4'])[2]")
    FORMAT_SCREEN_3_1:4 = ("xpath", "(//img[@title='Формат 1:4'])[3]")
    FORMAT_SCREEN_4_1:4 = ("xpath", "(//img[@title='Формат 1:4'])[4]")

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

    @allure.step("Click button exit")
    def click_button_exit(self):
        self.wait.until(EC.element_to_be_clickable(self.BUTTON_EXIT)).click()

    @allure.step("Open new window")
    def open_new_window(self):
        self.driver.switch_to.new_window("window")
        time.sleep(5)
        self.driver.get("https://x.camdrive.com/")
        time.sleep(5)

    @allure.step("Click cameras random")
    def click_cameras_random(self):
        device_list = self.wait.until(EC.presence_of_all_elements_located(self.LIST_DEVICES))
        if device_list:
          random_element = random.choice(device_list)
          random_element.click()
        else:
            print("Не найден список устройств")

    # @allure.step("Click view screen random")
    # def click_view_screen_random(self):


