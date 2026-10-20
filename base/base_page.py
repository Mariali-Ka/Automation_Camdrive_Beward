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

    # Проверяем, что нет модальных окон
    def close_password_breach_modal(self):
        """Пытается закрыть модальное окно 'Смените пароль' от Chrome"""
        locators = [
            ("xpath", "//button[contains(., 'OK') or contains(., 'ОК')]"),
            ("xpath", "//div[@role='dialog']//button[contains(text(), 'OK')]"),
            ("xpath", "//*[contains(text(), 'Смените пароль')]/following::button[1]"),
            ("css selector", "button[class*='ok'], button:contains('OK'), .modal-button.ok")
        ]
        for by, locator in locators:
            try:
                el = self.driver.find_element(by, locator)
                el.click()
                print("✅ Модальное окно 'Смените пароль' закрыто.")
                return True
            except:
                continue
        print("❌ Модальное окно не найдено.")
        return False

    # Закрываем модальное окно с помощью Enter
    def press_enter_to_accept_modal(self):
        """Нажимает Enter — часто закрывает нативные модальные окна Chrome"""
        from selenium.webdriver.common.keys import Keys
        try:
            # Отправляем Enter в активное окно/фокус
            self.driver.switch_to.active_element.send_keys(Keys.ENTER)
            print("✅ Нажат Enter — модальное окно, возможно, закрыто.")
        except Exception as e:
            print(f"⚠️ Не удалось отправить Enter: {e}")
            # Альтернатива: глобальный send_keys к body
            try:
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)
                print("✅ Enter отправлен через body.")
            except:
                pass

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

    @allure.step('Execute js')
    def execute_js(self, script, *args):
        return self.driver.execute_script(script, *args)

    @allure.step('Wait until visible')
    def wait_until_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step('Wait until clickable')
    def wait_until_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

