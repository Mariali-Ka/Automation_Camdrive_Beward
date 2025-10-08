import allure
from selenium.webdriver import ActionChains
from allure_commons.types import AttachmentType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10, poll_frequency=1)



    # открываем страницу
    @allure.step('Open a browser')
    def open(self):
        with allure.step(f"Open {self.PAGE_URL} page"):
            self.driver.get(self.PAGE_URL)  # будет прописан для каждой страницы индивидуально

    # Проверяем, что страница открылась
    def is_opened(self):
        with allure.step(f"Page {self.PAGE_URL} is opened"):
            self.wait.until(EC.url_to_be(self.PAGE_URL))

    # Подтвержение скриншотом
    def make_screenshot(self, screenshot_name):
        allure.attach(
            body=self.driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=AttachmentType.PNG
        )

    @allure.step('Find visible elements')
    def element_is_visible(self, locator, timeout=5):
            self.go_to_element(self.element_is_present(locator))
            return self.wait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    @allure.step('Find visible elements')
    def elements_are_visible(self, locator, timeout=5):
            return self.wait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))

    @allure.step('Find a present element')
    def element_is_present(self, locator, timeout=5):
            return self.wait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Find present elements')
    def elements_are_present(self, locator, timeout=5):
            return self.wait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))

    @allure.step('Find a not visible element')
    def element_is_not_visible(self, locator, timeout=5):
            return self.wait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

    @allure.step('Find clickable elements')
    def element_is_clickable(self, locator, timeout=5):
            return self.wait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    @allure.step('Go to specified element')
    def go_to_element(self, element):
            self.driver.execute_script("arguments[0].scrollIntoView();", element)

    @allure.step('Double click')
    def action_double_click(self, element):
            action = ActionChains(self.driver)
            action.double_click(element)
            action.perform()

    @allure.step('Right click')
    def action_right_click(self, element):
            action = ActionChains(self.driver)
            action.context_click(element)
            action.perform()

    @allure.step('Drag and drop by offset')
    def action_drag_and_drop_by_offset(self, element, x_coords, y_coords):
            action = ActionChains(self.driver)
            action.drag_and_drop_by_offset(element, x_coords, y_coords)
            action.perform()

    @allure.step('Drag and drop element to element')
    def action_drag_and_drop_to_element(self, what, where):
            action = ActionChains(self.driver)
            action.drag_and_drop(what, where)
            action.perform()

    @allure.step('Move cursor to element')
    def action_move_to_element(self, element):
            action = ActionChains(self.driver)
            action.move_to_element(element)
            action.perform()

    @allure.step('Remove footer')
    def remove_footer(self):
            self.driver.execute_script("document.getElementsByTagName('footer')[0].remove();")
            self.driver.execute_script("document.getElementsById('close-fixedban').remove();")

    # @allure.step('Open new window')
    # def open_new_window(self):
    #     self.driver.new_window("tab")
    #     self.driver.get("https://x.camdrive.com/")