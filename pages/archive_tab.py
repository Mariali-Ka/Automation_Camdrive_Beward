import re
import time
import random
import calendar
from datetime import datetime
# from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import allure
from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Настройка Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)


class ArchiveTab(BasePage):
    PAGE_URL = Links.ARCHIVE_TAB

    TAB_ARCHIVE = ("xpath", "//a[text()='Архив']") # вкладка Архив
    FIELD_CALENDAR = ("xpath", "//div[text()='Календарь']") # меню Календарь - текст
    BUTTON_OPENING_CALENDAR = ("xpath", "//img[@alt='Выберите дату']") # кнопка Открыть дату в блоке Скачать видеоархив
    BUTTON_OPENING_CALENDAR_MONTH_AGO = ("xpath", "//a[@title='<Пред']") # кнопка перейти на предыдущий месяц в календаре Открытой даты в блоке Скачать видеоархив
    SELECT_DAY_OPENING_CALENDAR = ("xpath", "//td[@data-handler='selectDay']") # ячейка день в календаре Открытой даты в блоке Скачать видеоархив
    FIELD_INPUT_DATE = ("xpath", "//input[@id='download-date']") # поле ввода даты в блоке Скачать видеоархив
    HEADING_C = ("xpath", "//th[@class='heading-c']") # заголовок месяца и года в блоке Календарь
    BUTTON_HEADING_l = ("xpath", "//th[@class='heading-l prev']") # кнопка открыть предыдущий месяц в блоке Календарь
    BUTTON_HEADING_R = ("xpath", "//th[@class='heading-r off']") # дизабленная кнопка открыть будущий месяц после текущего месяца в блоке Календарь
    BUTTON_HEADING_R_NEXT = ("xpath", "//th[@class='heading-r next']") # кнопка открытия следующего месяца до текущего месяца в блоке Календарь
    DATE_CALENDAR_WITH_RECORDING = ("xpath", "//td//div[contains(@class, 'item day')]")  # дата с записями в блоке календарь
    SEGMENT_RECORDING = ("xpath", "//div[@class='time item  constant']")  # отрезок записи в блоке Календарь
    PLAY_VIDEO_WINDOW = ("xpath", "//video[@preload='auto']") # трансляция видеозаписи в блоке Экран
    ACTIVE_CAMERAS_INSIDE_LIST = ("xpath", "//li[contains(@class, 'access_camera')][not(contains(@class, 'device_disconnect'))]") # активные камеры внутри списка дерева

    # ОТКРЫВАЕМ ВКЛАДКУ АРХИВ
    @allure.step("Go to archive tab")
    def click_go_to_archive_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.TAB_ARCHIVE)).click()

    # ПРОВЕРКА, ЧТО ОТКРЫТА ВКЛАДКА АРХИВ
    @allure.step("Is Opened Archive Tab")
    def is_opened_archive_tab(self):
        current_url = self.PAGE_URL
        assert current_url == Links.ARCHIVE_TAB, "Ошибка в URL, открыта не та страница"

    # СМЕНА МЕСЯЦА В КАЛЕНДАРЕ
    @allure.step("Go to one month ago calendar")
    def click_go_to_one_month_ago_calendar(self):
        # Подтверждение исходного месяца
        month_header = self.wait.until(EC.presence_of_element_located(self.HEADING_C))
        current_month_text = month_header.text.strip()
        print(f"Исходный месяц: {current_month_text}")
        # Переход на предыдущий месяц
        self.wait.until(EC.element_to_be_clickable(self.BUTTON_HEADING_l)).click()
        self.wait.until(lambda driver: self.wait.until(
            EC.presence_of_element_located(self.HEADING_C)).text.strip() != current_month_text)
        # Проверка - действительно осуществлен переход, название месяца сменился
        new_month_header = self.wait.until(EC.presence_of_element_located(self.HEADING_C))
        new_month_text = new_month_header.text.strip()
        print(f"Новый месяц после нажатия: {new_month_text}")
        assert new_month_text != current_month_text, "Месяц не изменился после нажатия кнопки"

    # ПЕРЕХОД НА БУДУЩИЙ МЕСЯЦ
    @allure.step("Go to one month advance calendar")
    def click_go_to_one_month_advance_calendar(self):
        self.wait.until(EC.element_to_be_clickable(self.BUTTON_HEADING_R_NEXT)).click()

    # ОТКРЫТИЕ КАЛЕНДАРЯ на зоне- ЗОНА СКАЧИВАНИЯ ВИДЕОАРХИВА
    @allure.step("Checking opening calendar")
    def click_checking_opening_calendar(self):
        self.wait.until(EC.element_to_be_clickable(self.BUTTON_OPENING_CALENDAR)).click()
        # проверка, что календарь открыт
        assert self.wait.until(EC.visibility_of_element_located(self.BUTTON_OPENING_CALENDAR)).is_displayed()

    # ПРОВЕРКА ВВОДА В ПОЛЕ ДАТА - ЗОНА СКАЧИВАНИЯ ВИДЕОАРХИВА
    allure.step("Selected date displayed field")
    def selected_date_displayed_field(self):
        self.wait.until(EC.element_to_be_clickable(self.BUTTON_OPENING_CALENDAR_MONTH_AGO)).click()
        # Получаем список активных дней
        select_day_elements = self.wait.until(EC.visibility_of_all_elements_located(self.SELECT_DAY_OPENING_CALENDAR))
        # Фильтруем только активные/валидные дни
        valid_days = []
        for day in select_day_elements:
            # Проверка, что день не отключён
            if "disabled" not in day.get_attribute("class") and day.text.strip().isdigit():
                valid_days.append(day)
        # Выводим доступные даты
        print("Валидные дни:", [d.text for d in valid_days])
        # Рандомно устанавливаем дату
        random_valid_days = random.choice(select_day_elements)
        random_valid_days.click()
        time.sleep(5)
        # Проверяем, что дата установилась в поле
        selected_date = self.wait.until(EC.visibility_of_element_located(self.FIELD_INPUT_DATE)).get_attribute("value")
        # Проверяем формат даты
        assert re.match(r"\d{2}\.\d{2}\.\d{4}", selected_date)

    # ПОЛУЧЕНИЕ СПИСКА КАМЕР. ВЫБОР ИЗ СПИСКА АКТИВНЫЕ КАМЕРЫ. РАНДОМНО НАЖАТЬ НА АКТИВНУЮ КАМЕРУ.
    allure.step("Active cameras inside list")
    def active_cameras_inside_list(self):
        try:

            active_cameras = self.wait.until(EC.presence_of_all_elements_located(self.ACTIVE_CAMERAS_INSIDE_LIST))

            if not active_cameras:
                print("Активных камер не найдено.")
            else:
                # Рандомно выбираем одну активную камеру
                random_camera = random.choice(active_cameras)
                time.sleep(5)

                # Кликаем по ней
                random_camera.click()
                time.sleep(5)

                print("Случайная активная камера выбрана и нажата.")

        except Exception as e:
            print(f"Произошла ошибка: {e}")

        finally:
            pass



    # ПРОВЕРКА ВОСПРОИЗВЕДЕНИЯ ЗАПИСИ
    allure.step("Viewing from camera")
    def viewing_from_camera(self):

        day_elements = self.wait.until(EC.visibility_of_all_elements_located(self.DATE_CALENDAR_WITH_RECORDING))

        # Фильтруем только активные/валидные дни
        valid_days = []
        for day in day_elements:
            if "disabled" not in day.get_attribute("class") and day.text.strip().isdigit():
                valid_days.append(day)

        print("Валидные дни:", [d.text for d in valid_days])

        random_valid_days = random.choice(day_elements)
        random_valid_days.click()

        try:
            records = self.wait.until(EC.visibility_of_all_elements_located(self.SEGMENT_RECORDING))

            if not records:
                print("Записи не найдены!")
            else:
                print(f"Найдено записей: {len(records)}")

                random_record = random.choice(records)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", random_record)
                random_record.click()
                time.sleep(5)

                # Попробуем получить video_element
            try:
                video_element = self.wait.until(EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                print("Видео найдено и готово к воспроизведению.")
            except TimeoutException:
                raise Exception("Видео не загрузилось вовремя.")

            # Ждём, пока появится длительность
            duration = None
            for _ in range(20):
                try:
                    duration = self.driver.execute_script("return document.getElementsByTagName('video')[0].duration", video_element)
                    if duration and duration > 0:
                        print(f"Длительность видео: {duration:.2f} секунд")
                        break
                except Exception as e:
                    print(f"Ошибка получения длительности: {e}")

                time.sleep(1)

            if not duration or duration <= 0:
                raise Exception("Не удалось определить длительность видео")

            # 6. Ждём окончания воспроизведения
            start_time = time.time()
            while True:
                try:
                    current_time = self.driver.execute_script("return document.getElementsByTagName('video')[0].currentTime", video_element)
                    if current_time >= duration - 1:  # -1 секунда — погрешность
                        print("Видео полностью воспроизведено.")
                        break
                except Exception as e:
                    print(f"Ошибка получения текущего времени: {e}")

                time.sleep(1)

            end_time = time.time()
            watch_time = end_time - start_time

            print(f"Время просмотра: {watch_time:.2f} секунд")

        finally:
            self.driver.quit()
