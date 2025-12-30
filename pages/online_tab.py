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
    BUTTON_ADD_CAMERA = ("xpath", "//div[@title='Добавить камеру']")  # кнопка добавить камеру в дерево
    BUTTON_REMOVE_CAMERA = ("xpath", "//div[@title='Удалить камеру']")  # кнопка удалить камеру в дерево
    BUTTON_RENAME_CAMERA = ("xpath", "//div[@title='Переименовать камеру']")  # кнопка переименовать камеру в дерево
    FIELD_INPUT_DEVICE_ACTIVATION_LOGIN = ("xpath", "//input[@name='device_activation_login']")  # поле Логин активации в форме добавления камеры
    FIELD_INPUT_DEVICE_ACTIVATION_PASSWORD = ("xpath", "//input[@name='device_activation_password']")  # поле Пароль активации в форме добавления камеры
    BUTTON_SHOW_PASSWORD_IN_FORM_ADD_CAMERA = ("xpath", "//div[@title='Показать пароль']")  # кнопка Показать пароль в форме добавление камеры
    BUTTON_ADD_IN_FORM_ADD_CAMERA = ("xpath", "//input[@value='Добавить']")  # кнопка Добавить в форме добавление камеры
    BUTTON_CLOSE_IN_FORM_ADD_CAMERA = ("xpath", "//input[@value='Закрыть']")  # кнопка Закрыть в форме добавление камеры
    SERVICE_MESSAGE_IN_FORM_ADD_CAMERA = ("xpath", "//div[@class='closable notification s error']")  # служебное сообщение в форме добавление камеры
    BUTTON_CLOSE_SERVICE_MESSAGE = ("xpath", "//a[@class='close']")  # кнопка закрыть служебное сообщение в форме добавление камеры
    INACTIVE_CAMERA_ITEM = ("xpath", "//li[@rel='channel' and contains(@class, 'device_disconnect')]") # НЕактивные камеры в дереве
    SCREEN_FORM_REMOVAL_CAMERA = ("xpath", "//div[@class='form-item']")  # экран форма удаления камеры
    BUTTON_RESEND_CODE = ("xpath", "//input[@name='repeat']")  # кнопка отправить код повторно
    SERVICE_MESSAGE_IN_FORM_DELETE_CAMERA = ("xpath", "//div[@class='closable notification s success']")  # служебное сообщение в форме удаления камеры
    BUTTON_CONFIRM = ("xpath", "//input[@id='confirm']")  # кнопка Подтвердить на экране форма удаления камеры
    BUTTON_CANCEL_DELETE_VIDEO_ARCHIVE = ("xpath", "(//button//span[@class='ui-button-text'])[3]")  # кнопка Отменить удаления видеоархива
    BUTTON_CLOSE_IN_FORM_DELETE_CAMERA = ("xpath", "//input[contains(@type, 'button')][contains(@value, 'Закрыть')]")  # кнопка Закрыть на экране форма удаления камеры
    DIALOG_BOX_IN_FORM_DELETE_CAMERA = ("xpath", "//div[@class='ui-dialog-content ui-widget-content']")  # диалоговое окно на экране форма удаления камеры
    FIELD_INPUT_VERIFICATION_CODE = ("xpath", "//input[@name='code']")  # поле ввода Код подтверждение



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

    # ПОЛУЧЕНИЕ СПИСКА КАМЕР И ПРОИЗВОЛЬНЫЙ КЛИК ПО АКТИВНОЙ КАМЕРЕ
    @allure.step("Click random active camera")
    def click_random_active_camera(self):
        """
        Ожидаем загрузки списка камер, находим активные,
        выбираем случайную и эмулируем клик по текстовой части.
        """
        # Ждём появления хотя бы одной камеры
        self.wait.until(
            lambda d: self.driver.find_elements(*self.LIST_DEVICES)
        )
        time.sleep(1.5)  # даём jsTree завершить инициализацию

        # Находим все активные камеры
        active_cameras = self.driver.find_elements(*self.ACTIVE_CAMERAS_INSIDE_LIST)

        assert active_cameras, "Не найдено ни одной неактивной камеры"

        # Выбираем случайную
        target_li = random.choice(active_cameras)
        a_element = target_li.find_element(By.TAG_NAME, "a")

        camera_name = a_element.text.strip()
        print(f"Выбрана камера: {camera_name}")

        # Прокручиваем к элементу
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
            a_element
        )
        time.sleep(0.5)

        # Кликаем через elementFromPoint — как вручную в DevTools
        success = self.driver.execute_script("""
            const a = arguments[0];
            const rect = a.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0) return false;
            const x = rect.left + rect.width * 0.8;  // клик по тексту, а не по иконке
            const y = rect.top + rect.height / 2;
            const el = document.elementFromPoint(x, y);
            if (el) {
                el.click();
                return true;
            }
            return false;
        """, a_element)

        # Проверяем, что камера выделилась
        class_attr = a_element.get_attribute("class") or ""
        assert "jstree-clicked" in class_attr, f"Камера не выделилась. Классы: {class_attr}"

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

    # НЕГАТИВНАЯ ПРОВЕРКА ДОБАВЛЕНИЯ КАМЕРЫ
    @allure.step("Negative check adding camera")
    def execute_negative_camera_add(self):
        """
        Основной метод выполнения негативного сценария добавления камеры:
        - генерирует случайные строки,
        - выполняет последовательность действий,
        - проверяет URL,
        - закрывает драйвер в конце.
        """
        # Внутренняя функция для генерации строки
        def generate_random_string(length=10):
            """Генерирует случайную строку из букв и цифр."""
            letters_and_digits = string.ascii_letters + string.digits
            return ''.join(random.choice(letters_and_digits) for _ in range(length))

        try:
            # Нажать на кнопку Добавить камеру в дерево
            add_camera_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_ADD_CAMERA))
            add_camera_button.click()
            print("Кнопка 'Добавить камеру' нажата.")

            # В поле Логин активации ввести рандомный текст
            time.sleep(2)
            login_field = self.wait.until(EC.presence_of_element_located(self.FIELD_INPUT_DEVICE_ACTIVATION_LOGIN))
            random_login = generate_random_string()
            login_field.send_keys(random_login)
            time.sleep(2)
            print(f"В поле логина введено: {random_login}")

            # Нажать кнопку Добавить в форме добавления камеры
            add_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_ADD_IN_FORM_ADD_CAMERA))
            add_button.click()
            time.sleep(2)
            print("Кнопка 'Добавить' нажата.")

            # Служебное сообщение в форме добавление камеры
            service_message_element = self.wait.until(EC.presence_of_element_located(self.SERVICE_MESSAGE_IN_FORM_ADD_CAMERA))
            service_message_text = service_message_element.text
            print(f"Текст служебного сообщения: {service_message_text}")

            # Закрыть служебное сообщение в форме добавление камеры
            close_message_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_CLOSE_SERVICE_MESSAGE))
            close_message_button.click()
            time.sleep(2)
            print("Служебное сообщение закрыто.")

            # В поле пароль ввести рандомный пароль
            password_field = self.wait.until(EC.presence_of_element_located(self.FIELD_INPUT_DEVICE_ACTIVATION_PASSWORD))
            random_password = generate_random_string()
            password_field.send_keys(random_password)
            time.sleep(2)
            print(f"В поле пароля введено: {random_password}")

            # Нажать на кнопку Показать пароль в форме добавление камеры
            show_password_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_SHOW_PASSWORD_IN_FORM_ADD_CAMERA))
            show_password_button.click()
            time.sleep(2)
            print("Кнопка 'Показать пароль' нажата.")

            # Нажать на кнопку добавить в форме добавления камеры
            add_button_click_again = self.wait.until(EC.element_to_be_clickable(self.BUTTON_ADD_IN_FORM_ADD_CAMERA))
            add_button_click_again.click()
            time.sleep(2)
            print("Кнопка 'Добавить' нажата.")

            # Служебное сообщение в форме добавление камеры
            service_message_element_2 = self.wait.until(EC.presence_of_element_located(self.SERVICE_MESSAGE_IN_FORM_ADD_CAMERA))
            service_message_text_2 = service_message_element_2.text
            print(f"Текст служебного сообщения: {service_message_text_2}")

            # Закрыть служебное сообщение в форме добавление камеры
            close_form_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_CLOSE_IN_FORM_ADD_CAMERA))
            close_form_button.click()
            time.sleep(2)
            print("Форма добавления камеры закрыта.")

            # Проверка, что вернулись на экран Онлайн (https://x.camdrive.com/online)
            current_url = self.driver.current_url
            expected_url = self.PAGE_URL
            print("Текущий URL:", current_url)
            print("Ожидаемый URL:", expected_url)

            if current_url != expected_url:
                print(f"Ошибка в URL, ожидалось {expected_url}, получено {current_url}")

            else:
                print("Успешно вернулись на экран Онлайн.")

        except Exception as e:
            print(f"Произошла ошибка: {e}")

        finally:
            self.driver.quit()
            print("Браузер закрыт.")

    # ПОЛУЧЕНИЕ СПИСКА НЕАКТИВНЫХ КАМЕР И ПРОИЗВОЛЬНЫЙ КЛИК ПО НЕАКТИВНОЙ КАМЕРЕ
    @allure.step("Click random inactive cameras ")
    def click_random_inactive_camera(self):
        """
        Ожидаем загрузки списка камер, находим неактивные,
        выбираем случайную и эмулируем клик по текстовой части.
        """
        # Ждём появления хотя бы одной камеры
        self.wait.until(
            lambda d: self.driver.find_elements(*self.LIST_DEVICES)
        )
        time.sleep(1.5)  # даём jsTree завершить инициализацию

        # Находим все неактивные камеры
        inactive_cameras = self.driver.find_elements(*self.INACTIVE_CAMERA_ITEM)

        assert inactive_cameras, "Не найдено ни одной неактивной камеры"

        # Выбираем случайную
        target_li = random.choice(inactive_cameras)
        a_element = target_li.find_element(By.TAG_NAME, "a")

        camera_name = a_element.text.strip()
        print(f"Выбрана камера: {camera_name}")

        # Прокручиваем к элементу
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
            a_element
        )
        time.sleep(0.5)

        # Кликаем через elementFromPoint — как вручную в DevTools
        success = self.driver.execute_script("""
            const a = arguments[0];
            const rect = a.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0) return false;
            const x = rect.left + rect.width * 0.8;  // клик по тексту, а не по иконке
            const y = rect.top + rect.height / 2;
            const el = document.elementFromPoint(x, y);
            if (el) {
                el.click();
                return true;
            }
            return false;
        """, a_element)

        # Проверяем, что камера выделилась
        class_attr = a_element.get_attribute("class") or ""
        assert "jstree-clicked" in class_attr, f"Камера не выделилась. Классы: {class_attr}"

    # ПРОВЕРКА ПОПЫТКА УДАЛЕНИЯ КАМЕРЫ ИЗ СПИСКА В ДЕРЕВЕ
    @allure.step("Attempting to delete the camera ")
    def generate_random_code(self, length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    def attempting_delete_camera(self):

        try:

            # 1. Нажать на кнопку "Удалить камеру"
            remove_btn = self.wait.until(EC.element_to_be_clickable(self.BUTTON_REMOVE_CAMERA))
            remove_btn.click()

            # 2. Проверить, что появилась форма удаления камеры
            form = self.wait.until(EC.presence_of_element_located(self.SCREEN_FORM_REMOVAL_CAMERA))
            assert form.is_displayed(), "Форма удаления камеры не отображается"
            print(f"Текст формы удаления камеры:\n{form.text}")

            # 3. Ввести случайный код подтверждения
            code_field = self.wait.until(EC.presence_of_element_located(self.FIELD_INPUT_VERIFICATION_CODE))
            random_code = self.generate_random_code()
            code_field.send_keys(random_code)

            # 4. Нажать кнопку "Подтвердить"
            confirm_btn = self.wait.until(EC.element_to_be_clickable(self.BUTTON_CONFIRM))
            confirm_btn.click()

            # 5. Проверить диалоговое окно и вывести его текст
            dialog = self.wait.until(EC.presence_of_element_located(self.DIALOG_BOX_IN_FORM_DELETE_CAMERA))
            assert dialog.is_displayed(), "Диалоговое окно не появилось"
            print(f"Текст диалогового окна:\n{dialog.text}")

            # 6. Нажать "Отменить"
            cancel_btn = self.wait.until(EC.element_to_be_clickable(self.BUTTON_CANCEL_DELETE_VIDEO_ARCHIVE))
            cancel_btn.click()

            # 7. Нажать "Отправить код повторно"
            resend_btn = self.wait.until(EC.element_to_be_clickable(self.BUTTON_RESEND_CODE))
            resend_btn.click()

            # 8. Проверить служебное сообщение и вывести его текст
            service_msg = self.wait.until(EC.presence_of_element_located(self.SERVICE_MESSAGE_IN_FORM_DELETE_CAMERA))
            assert service_msg.is_displayed(), "Служебное сообщение не появилось"
            print(f"Служебное сообщение:\n{service_msg.text}")

            # 9. Нажать "Закрыть"
            close_btn = self.wait.until(EC.element_to_be_clickable(self.BUTTON_CLOSE_IN_FORM_DELETE_CAMERA))
            close_btn.click()

            # 10. Проверяем, что форма удаления закрылась
            self.wait.until(
                EC.invisibility_of_element_located(self.SCREEN_FORM_REMOVAL_CAMERA),
                message="Форма удаления камеры не исчезла после нажатия 'Закрыть'"
            )
            print("Форма удаления закрыта. Пользователь остался на странице онлайн.")

        except Exception as e:
            print(f"Произошла ошибка во время выполнения теста: {e}")
            raise









