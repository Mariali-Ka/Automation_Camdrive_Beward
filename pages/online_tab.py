import time
import random
import allure
import datetime
from selenium.common import TimeoutException

from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException



class OnlineTab(BasePage):

    PAGE_URL = Links.ONLINE_TAB

    BUTTON_MY_CAMERAS = ("xpath", "//li[contains(@rel, 'drive')]/ins[1]") # кнопка открыть список Мои камеры
    BUTTON_PUBLIC_CAMERAS = ("xpath", "//li[contains(@rel, 'drive_public')]/ins") # кнопка открыть список общественные камеры
    LIST_DEVICES = ("xpath", "//li[contains(@rel, 'channel')]") # список камер
    BUTTON_EXIT = ("xpath", "//input[@value='Выйти']") # кнопка Выйти
    MY_CAMERA_ONE = ("xpath", "//li[contains(@rel, 'channel')][not(contains(@rel, 'public'))][1]") # 1-я камера в списке дерева
    MY_CAMERA_TWO = ("xpath", "//li[contains(@rel, 'channel')][not(contains(@rel, 'public'))][2]") # 2-я камера в списке дерева
    ACTIVE_CAMERAS_INSIDE_LIST = ("xpath", "//li[@rel='channel'][not(contains(@class, 'device_disconnect'))]")  # активные камеры в дереве
    BUTTON_CLOSE_SCREEN = ("xpath", "//img[@class='iePNG ch screen-close']") # кнопка закрытие экрана
    BUTTON_OPEN_FORMAT_1_1 = ("xpath", "//img[@class='iePNG ch screen-1x1']")  # открыть в формате 1:1
    BUTTON_OPEN_FORMAT_1_4 = ("xpath", "//img[@class='iePNG ch screen-1x4']")  # открыть в формате 1:4
    VIEW_SCREEN = ("xpath", "//div[contains(@class, 'screen')]")  # посмотреть экран (1-4)



    # ПРОВЕРКА, ЧТО ОТКРЫТА ВКЛАДКА ОНЛАЙН
    @allure.step("Is Opened Online Tab")
    def is_opened_online_tab(self):
        current_url = self.PAGE_URL
        assert current_url == Links.ONLINE_TAB, "Ошибка в URL, открыта не та страница"

    # НАЖАТЬ НА КНОПКУ ОБЩЕСТВЕННЫЕ  КАМЕРЫ
    @allure.step("Click Button Public Cameras")
    def click_button_public_cameras(self):
        try:
          self.wait.until(EC.element_to_be_clickable(self.BUTTON_PUBLIC_CAMERAS)).click()
        except TimeoutException:
            # Кнопка не появилась в течение времени ожидания — ничего не делаем
            pass




    # ПЕРЕТЯГИВАНИЕ КАМЕРЫ ИЗ СПИСКА В ДЕРЕВЕ НА ДРУГУЮ ПОЗИЦИЮ
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

    # НАЖАТЬ КНОПКУ ВЫХОД ИЗ ЛК
    @allure.step("Click button exit")
    def click_button_exit(self):
        self.wait.until(EC.element_to_be_clickable(self.BUTTON_EXIT)).click()

    # ОТКРЫТИЕ ЛК В ТОМ ЖЕ БРАУЗЕРЕ В СОСЕДНЕЙ ВКЛАДКЕ БЕЗ АВТОРИЗАЦИИ
    @allure.step("Open new window")
    def open_new_window(self):
        self.driver.switch_to.new_window("window")
        time.sleep(5)
        self.driver.get("https://x.camdrive.com/")
        time.sleep(5)

    # ПОЛУЧЕНИЕ СПИСКА КАМЕР И ПРОИЗВОЛЬНЫЙ КЛИК ПО КАМЕРЕ
    @allure.step("Click cameras random")
    def click_cameras_random(self):
        device_list = self.wait.until(EC.presence_of_all_elements_located(self.LIST_DEVICES))
        if device_list:
          random_element = random.choice(device_list)
          random_element.click()
        else:
            print("Не найден список устройств")

    # ПРОВЕРКА ОНЛАЙН-ТРАНСЛЯЦИИ
    @allure.step("Check online broadcast")
    def main(self):
        """
        Основная функция выполнения сценария:
        - закрывает все открытые экраны,
        - выбирает случайную активную камеру,
        - открывает случайный экран просмотра,
        - переключает форматы отображения,
        - делает скриншоты и завершает сессию драйвера.
        """

        def make_screenshot(description=""):
            """Создаёт скриншот с меткой времени и описанием."""
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"screenshot_{description}_{timestamp}.png"
            self.driver.save_screenshot(filename)
            print(f"Скриншот сохранен: {filename}")

        def close_all_opened_screens():
            """Закрывает все открытые экраны, если они есть."""
            all_close_buttons = self.wait.until(EC.presence_of_all_elements_located(self.BUTTON_CLOSE_SCREEN))
            if all_close_buttons and len(all_close_buttons) > 0:
                print(f"Найдено {len(all_close_buttons)} кнопок закрытия экрана.")
                make_screenshot("before_closing_all_screens")

                # Закрываем все экраны поочередно
                for i in range(len(all_close_buttons)):
                    try:
                        # Повторно ищем кнопки, так как DOM может измениться после каждого закрытия
                        close_button = self.wait.until(EC.presence_of_all_elements_located(self.BUTTON_CLOSE_SCREEN))
                        if close_button and len(close_button) > 0:
                            close_button[0].click()
                            print(f"Кнопка закрытия экрана нажата ({i + 1}/{len(all_close_buttons)})")
                            time.sleep(1)
                        else:
                            print("Кнопка закрытия экрана больше не найдена.")
                            break
                    except Exception as e:
                        print(f"Ошибка при закрытии экрана {i + 1}: {e}")
                        break
            else:
                print("Кнопки закрытия экрана не найдены.")



        # Закрываем все открытые экраны
        close_all_opened_screens()

        try:
            active_cameras = self.wait.until(EC.presence_of_all_elements_located(self.ACTIVE_CAMERAS_INSIDE_LIST))

            if not active_cameras:
                print("Активных камер не найдено.")
                assert False, "Активные камеры не найдены."
            else:
                # Рандомно выбираем один индекс, чтобы избежать stale при долгой задержке
                random_index = random.randint(0, len(active_cameras) - 1)
                print(f"Выбран индекс камеры: {random_index}")

                # Цикл для повторной попытки клика в случае StaleElementReferenceException
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        # Повторно локейтим элемент, чтобы избежать stale
                        random_camera = self.wait.until(EC.presence_of_all_elements_located(self.ACTIVE_CAMERAS_INSIDE_LIST))[
                            random_index]

                        # Получаем название камеры до клика
                        camera_title = random_camera.get_attribute("title") or random_camera.text
                        print(f"Выбрана активная камера: '{camera_title}'")

                        random_camera.click()
                        print("Рандомно выбрана и нажата активная камера.")
                        break
                    except StaleElementReferenceException:
                        print(f"StaleElementReferenceException на попытке {attempt + 1}, пробуем снова...")
                        time.sleep(1)
                        continue
                else:
                    print("Не удалось кликнуть по элементу после нескольких попыток.")
                    assert False, "Не удалось кликнуть по активной камере из-за StaleElementReferenceException."

                # экраны просмотра
                try:
                    screens = self.wait.until(EC.presence_of_all_elements_located(self.VIEW_SCREEN))

                    if not screens:
                        print("Элементы экрана просмотра не найдены.")
                    else:
                        # Выбираем рандомно экран
                        random_screen_index = random.randint(0, len(screens) - 1)

                        # Цикл для клика по экрану (на случай StaleElementReferenceException)
                        for attempt in range(max_attempts):
                            try:
                                random_screen = self.wait.until(EC.presence_of_all_elements_located(self.VIEW_SCREEN))[
                                    random_screen_index]

                                # Получаем название экрана до клика
                                screen_title = random_screen.get_attribute("title") or random_screen.text
                                print(f"Выбран экран просмотра: '{screen_title}' (индекс: {random_screen_index})")

                                random_screen.click()
                                print(f"Рандомно нажат экран просмотра.")
                                break
                            except StaleElementReferenceException:
                                print(
                                    f"StaleElementReferenceException при клике по экрану на попытке {attempt + 1}, пробуем снова...")
                                time.sleep(1)
                                continue
                        else:
                            print("Не удалось кликнуть по экрану просмотра после нескольких попыток.")

                        print("Ждём 20 секунд перед началом работы с форматами...")
                        time.sleep(20)

                        # Кнопка формата 1:1 (внутри выбранного экрана)
                        try:
                            format_1_1_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_OPEN_FORMAT_1_1))
                            format_1_1_button.click()
                            print("Кнопка 'Формат 1:1' (внутри выбранного экрана) нажата.")

                            # делаем скриншот
                            time.sleep(2)
                            make_screenshot("after_format_1_1")

                        except Exception as e:
                            print(f"Не удалось найти или нажать кнопку 'Формат 1:1': {e}")

                        time.sleep(3)

                        # Кнопка формата 1:4 (внутри выбранного экрана)
                        try:
                            format_1_4_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_OPEN_FORMAT_1_4))
                            format_1_4_button.click()
                            print("Кнопка 'Формат 1:4' (внутри выбранного экрана) нажата.")


                            time.sleep(2)
                            make_screenshot("after_format_1_4")

                        except Exception as e:
                            print(f"Не удалось найти или нажать кнопку 'Формат 1:4': {e}")

                except Exception as screen_error:
                    print(f"Произошла ошибка при работе с экранами просмотра: {screen_error}")

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            assert False, f"Ошибка в методе active_cameras_inside_list: {e}"

        finally:
            self.driver.quit()

    # Вызов основной функции
    if __name__ == "__main__":
        main()


