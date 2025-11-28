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
from selenium.common.exceptions import StaleElementReferenceException

# Настройка Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)


class ArchiveTab(BasePage):
    PAGE_URL = Links.ARCHIVE_TAB

    TAB_ARCHIVE = ("xpath", "//a[text()='Архив']") # вкладка Архив
    FIELD_CALENDAR = ("xpath", "//div[text()='Календарь']") # меню Календарь - текст
    BUTTON_SELECT_DATE_OPENING_CALENDAR = ("xpath", "//img[@alt='Выберите дату']") # кнопка Открыть календарь для выбора даты в блоке Скачать видеоархив
    BUTTON_OPENING_CALENDAR_MONTH_AGO = ("xpath", "//a[@title='<Пред']") # кнопка перейти на предыдущий месяц в календаре Открытой даты в блоке Скачать видеоархив
    SELECT_DAY_OPENING_CALENDAR = ("xpath", "//td[@data-handler='selectDay']") # ячейка день в календаре Открытой даты в блоке Скачать видеоархив
    FIELD_INPUT_DATE = ("xpath", "//input[@id='download-date']") # поле ввода даты в блоке Скачать видеоархив
    BUTTON_UPLOAD = ("xpath", "//input[@value='Загрузить']")  # кнопка Загрузить в блоке Скачать видеоархив
    BUTTON_SELECT_TIME_OPENING_CALENDAR = ("xpath", "//img[@alt='Выберите время']")  # кнопка Открыть календарь для выбора времени в блоке Скачать видеоархив
    BUTTON_SELECT_DURATION_OPENING_CALENDAR = ("xpath", "//img[@alt='Выберите время']")  # кнопка Открыть календарь для выбора длительности в блоке Скачать видеоархив
    HANDLE_SLIDER_SELECT_TIME_CLOCK = ("xpath", "(//a[contains(@class, 'slider-handle')])[1]")  # ручка слайдера часы в календаре для выбора времени в блоке Скачать видео
    HANDLE_SLIDER_SELECT_TIME_MINUTES = ("xpath", "(//a[contains(@class, 'slider-handle')])[2]")  # ручка слайдера минуты в календаре для выбора времени в блоке Скачать видео
    HANDLE_SLIDER_SELECT_DURATION_MINUTES = ("xpath", "(//a[contains(@class, 'slider-handle')])[3]")  # ручка слайдера длительности в календаре для выбора длительности в блоке Скачать видео
    BUTTON_ANON_SELECT_TIME = ("xpath", "//button[text()='Сейчас']")  # кнопка Сейчас в календаре для выбора времени/длительности в блоке Скачать видео
    BUTTON_CLOSE_SELECT_TIME = ("xpath", "//button[text()='Закрыть']")  # кнопка Закрыть в календаре для выбора времени/длительности в блоке Скачать видео
    MESSAGE_DOWNLOAD_ARCHIVE_FRAGMENT = ("xpath", "//div[@role='dialog']")  # сообщение о выбранном для скачивания фрагмента видеоархива в блоке Скачать видео
    MESSAGE_NO_VIDEO_RECORDING = ("xpath", "//div[@role='dialog' or @text()='Для данного интервала времени нет видеозаписей.']")  # сообщение об отсутствии видеозаписи в блоке Скачать видео
    BUTTON_OK_MESSAGE = ("xpath", "//span[text()='Ок']")  # кнопка Ок в сообщение о выбранном для скачивания фрагмента видеоархива в блоке Скачать видео
    BUTTON_CANCEL_MESSAGE = ("xpath", "//span[text()='Отменить']")  # кнопка Отменить в сообщение о выбранном для скачивания фрагмента видеоархива в блоке Скачать видео
    HEADING_C = ("xpath", "//th[@class='heading-c']") # заголовок месяца и года в блоке Календарь
    BUTTON_HEADING_l = ("xpath", "//th[@class='heading-l prev']") # кнопка открыть предыдущий месяц в блоке Календарь
    BUTTON_HEADING_R = ("xpath", "//th[@class='heading-r off']") # дизаблена кнопка Открыть будущий месяц после текущего месяца в блоке Календарь
    BUTTON_HEADING_R_NEXT = ("xpath", "//th[@class='heading-r next']") # кнопка открытия следующего месяца до текущего месяца в блоке Календарь
    DATE_CALENDAR_WITH_RECORDING = ("xpath", "//td//div[contains(@class, 'item day')]")  # дата с записями в блоке календарь
    SEGMENT_RECORDING = ("xpath", "//div[@class='time item  constant']")  # отрезок записи в блоке Календарь
    PLAY_VIDEO_WINDOW = ("xpath", "//video[@preload='auto']") # трансляция видеозаписи в блоке Экран
    ACTIVE_CAMERAS_INSIDE_LIST = ("xpath", "//li[@rel='channel'][not(contains(@class, 'device_disconnect'))]") # активные камеры внутри списка дерева
    CHECKBOX_AUTOPLAY = ("xpath", "//input[@type='checkbox']") # чек-бокс автовоспроизведения
    NAME_CAMERAS_RECORDING_FRAGMENT_VIDEO = ("xpath", "//div[@class='dashboard']")  # наименование камеры воспроизведения записи фрагмента
    DATE_RECORDING_FRAGMENT_VIDEO = ("xpath", "//input[@id='download-date']")  # дата записи фрагмента
    TIME_RECORDING_FRAGMENT_VIDEO = ("xpath", "//input[@id='download-time']")  # время записи фрагмента
    DURATION_RECORDING_FRAGMENT_VIDEO = ("xpath", "//input[@id='download-duration']")  # время записи фрагмента

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

    # ОТКРЫТИЕ КАЛЕНДАРЯ - ЗОНА СКАЧИВАНИЯ ВИДЕОАРХИВА
    @allure.step("Checking opening calendar")
    def click_checking_opening_calendar(self):
        self.wait.until(EC.element_to_be_clickable(self.BUTTON_SELECT_DATE_OPENING_CALENDAR)).click()
        # проверка, что календарь открыт
        assert self.wait.until(EC.visibility_of_element_located(self.BUTTON_SELECT_DATE_OPENING_CALENDAR)).is_displayed()

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

    # ВЫБОР ДАТЫ, ВРЕМЯ И ДЛИТЕЛЬНОСТЬ ДЛЯ ЗАГРУЗКИ ФРАГМЕНТА ВИДЕОАРХИВА
    allure.step("Select the date, time, and duration to download the snippet")
    def select_date_time_duration_download_snippet(self):
        try:
            # Выбор случайной даты в календаре
            calendar_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_SELECT_DATE_OPENING_CALENDAR))
            calendar_button.click()
            # Получаем список активных дней
            select_day_elements = self.wait.until(EC.visibility_of_all_elements_located(self.SELECT_DAY_OPENING_CALENDAR))
            # Фильтруем только активные/валидные дни
            valid_days = []
            for day in select_day_elements:
                # Проверка, что день не отключён
                if "disabled" not in day.get_attribute("class") and day.text.strip().isdigit():
                    valid_days.append(day)
            random_day = random.choice(select_day_elements)
            random_day.click()
            time.sleep(5)

            # Работа со временем
            time_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_SELECT_TIME_OPENING_CALENDAR))
            time_button.click()

            # Слайдер часов
            hour_slider = self.wait.until(EC.element_to_be_clickable(self.HANDLE_SLIDER_SELECT_TIME_CLOCK))
            target_hour = random.randint(0, 23)
            time.sleep(0.1)

            # Двигаем слайдер влево или вправо
            for _ in range(abs(target_hour - 0)):
                ActionChains(self.driver).click_and_hold(hour_slider).move_by_offset(10, 0).release().perform()
                time.sleep(0.2)

            # Слайдер минут
            minute_slider = self.wait.until(EC.element_to_be_clickable(self.HANDLE_SLIDER_SELECT_TIME_MINUTES))
            target_minute = random.randint(0, 59)

            for _ in range(abs(target_minute - 0)):
                ActionChains(self.driver).click_and_hold(minute_slider).move_by_offset(7, 0).release().perform()
                time.sleep(0.2)

            # Нажимаем кнопку "Закрыть"
            close_time_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_CLOSE_SELECT_TIME))
            close_time_button.click()
            time.sleep(1.5)

            # Заполняем поле времени вручную (рандомно)
            time_field = self.wait.until(EC.presence_of_element_located(self.TIME_RECORDING_FRAGMENT_VIDEO))
            random_hour = f"{random.randint(0, 23):02d}"
            random_minute = f"{random.randint(0, 59):02d}"
            random_time_str = f"{random_hour}:{random_minute}"
            time_field.clear()
            time_field.send_keys(random_time_str)

            # Заполняем поле длительности вручную (рандомно от 2 до 30 минут)
            duration_field = self.wait.until(EC.presence_of_element_located(self.DURATION_RECORDING_FRAGMENT_VIDEO))
            random_duration_minutes = random.randint(2, 30)
            random_duration_str = f"{random_duration_minutes:02d}:00"
            duration_field.clear()
            duration_field.send_keys(random_duration_str)

            # 4. Нажимаем кнопку "Загрузить"
            upload_button = self.wait.until(EC.presence_of_element_located(self.BUTTON_UPLOAD))
            upload_button.click()

            # Ждем появления сообщения
            message = self.wait.until(EC.presence_of_element_located(self.MESSAGE_DOWNLOAD_ARCHIVE_FRAGMENT))
            print("Сообщение:", message.text)

            # Проверяем текст сообщения и нажимаем соответствующую кнопку
            if "Для данного интервала времени нет видеозаписей." in message.text:
                ok_button = self.wait.until(EC.element_to_be_clickable(self.MESSAGE_NO_VIDEO_RECORDING))
                ok_button.click()
            else:

                close_message_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_CANCEL_MESSAGE))
                close_message_button.click()

        finally:
            self.driver.quit()

    # ПОЛУЧЕНИЕ СПИСКА КАМЕР. ВЫБОР ИЗ СПИСКА АКТИВНЫЕ КАМЕРЫ. РАНДОМНО НАЖАТЬ НА АКТИВНУЮ КАМЕРУ.
    allure.step("Active cameras inside list")
    def active_cameras_inside_list(self):
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
                        random_camera.click()
                        print("Случайная активная камера выбрана и нажата.")
                        break  # Успешно кликнули — выходим из цикла
                    except StaleElementReferenceException:
                        print(f"StaleElementReferenceException на попытке {attempt + 1}, пробуем снова...")
                        time.sleep(1)
                        continue
                else:
                    print("Не удалось кликнуть по элементу после нескольких попыток.")
                    assert False, "Не удалось кликнуть по активной камере из-за StaleElementReferenceException."

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            assert False, f"Ошибка в методе active_cameras_inside_list: {e}"

        finally:
            pass

    # ПРОВЕРКА ВОСПРОИЗВЕДЕНИЯ В ОДНОМ РАНДОМНОМ ДНЕ РАНДОМНО ОДИН ФРАГМЕНТ ЗАПИСИ
    allure.step("Viewing fragment from camera")
    def viewing_fragment_from_camera(self):

        try:
            day_elements = self.wait.until(EC.visibility_of_all_elements_located(self.DATE_CALENDAR_WITH_RECORDING))

            # Фильтруем только активные/валидные дни
            valid_days = []
            for day in day_elements:
                if "disabled" not in day.get_attribute("class") and day.text.strip().isdigit():
                    valid_days.append(day)

            # Выводим список валидных дней один раз
            print("Валидные дни:", [d.text for d in valid_days])

            # Проверка, что есть хотя бы один валидный день
            assert len(valid_days) > 0, "Нет доступных дней для выбора."
            print("Есть доступные дни для выбора.")

            random_valid_day = random.choice(valid_days)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", random_valid_day)
            time.sleep(1.5)
            print(f"Кликаем на день: {random_valid_day.text}")
            random_valid_day.click()
            time.sleep(1.5)

            records = self.wait.until(EC.visibility_of_all_elements_located(self.SEGMENT_RECORDING))

            # Проверка, что записи найдены
            assert len(records) > 0, "Записи не найдены!"
            print(f"Найдено записей: {len(records)}")

            random_record = random.choice(records)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", random_record)
            random_record.click()
            time.sleep(5)

            # Ждём, пока обновятся поля под видео
            try:

                camera_name = self.wait.until(EC.presence_of_element_located(self.NAME_CAMERAS_RECORDING_FRAGMENT_VIDEO)).text
                date_elem = self.wait.until(EC.presence_of_element_located(self.DATE_RECORDING_FRAGMENT_VIDEO))
                time_elem = self.wait.until(EC.presence_of_element_located(self.TIME_RECORDING_FRAGMENT_VIDEO))
                duration_elem = self.wait.until(EC.presence_of_element_located(self.DURATION_RECORDING_FRAGMENT_VIDEO))

                # Извлечение данных из полей
                date_from_field = date_elem.text or date_elem.get_attribute("value") or "неизвестно"
                time_from_field = time_elem.text or time_elem.get_attribute("value") or "неизвестно"
                duration_from_field = duration_elem.text or duration_elem.get_attribute("value") or "неизвестно"

                # Проверки, что данные из полей получены
                assert camera_name, "Название камеры не найдено."
                assert date_from_field != "неизвестно", "Дата не найдена."
                assert time_from_field != "неизвестно", "Время не найдено."
                assert duration_from_field != "неизвестно", "Длительность не найдена."

                # Вывод информации
                print("=" * 50)
                print(f"Камера: {camera_name}")
                print(f"Дата (из поля): {date_from_field}")
                print(f"Время (из поля): {time_from_field}")
                print(f"Длительность (из поля): {duration_from_field}")
                print("=" * 50)
            except TimeoutException:
                assert False, "Не удалось получить данные из полей под видео."

            # Пробуем получить video_element
            try:
                video_element = self.wait.until(EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                print("Видео найдено и готово к воспроизведению.")
                # Проверка, что видео действительно присутствует
                assert video_element, "Видеоэлемент не найден."
            except TimeoutException:
                assert False, "Видео не загрузилось вовремя."

            # Ждём, пока появится длительность
            duration = None
            for _ in range(20):
                try:
                    duration = self.driver.execute_script("return document.getElementsByTagName('video')[0].duration",
                                                     video_element)
                    if duration and duration > 0:
                        print(f"Длительность видео: {duration:.2f} секунд")
                        break
                except Exception as e:
                    print(f"Ошибка получения длительности: {e}")

                time.sleep(1)

            # Проверка, что длительность определена
            assert duration and duration > 0, "Не удалось определить длительность видео"

            # Ждём окончания воспроизведения
            start_time = time.time()
            while True:
                try:
                    current_time = self.driver.execute_script("return document.getElementsByTagName('video')[0].currentTime",
                                                         video_element)
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

    # ПРОВЕРКА ВОСПРОИЗВЕДЕНИЯ В ОДНОМ РАНДОМНОМ ДНЕ ЧЕТЫРЕ РАНДОМНЫХ ФРАГМЕНТОВ ЗАПИСИ
    allure.step(("Viewing four fragments one days recording"))
    def viewing_four_fragments_one_days_recording(self):
        try:
            day_elements = self.wait.until(EC.visibility_of_all_elements_located(self.DATE_CALENDAR_WITH_RECORDING))

            valid_days = []
            for day in day_elements:
                if "disabled" not in day.get_attribute("class") and day.text.strip().isdigit():
                    valid_days.append(day)

            print("Валидные дни:", [d.text for d in valid_days])
            assert len(valid_days) > 0, "Нет доступных дней для выбора."
            print("Есть доступные дни для выбора.")

            random_valid_day = random.choice(valid_days)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", random_valid_day)
            time.sleep(1.5)
            print(f"Кликаем на день: {random_valid_day.text}")
            random_valid_day.click()
            time.sleep(1.5)

            # Проверка наличия записей
            records = self.wait.until(EC.visibility_of_all_elements_located(self.SEGMENT_RECORDING))
            assert len(records) > 0, "Записи не найдены!"
            print(f"Найдено записей: {len(records)}")

            # Выбираем 4 случайные записи
            selected_records = random.sample(records, min(4, len(records)))
            print(f"Выбрано записей для просмотра: {len(selected_records)}")

            # Проходим по каждой выбранной записи
            for i, record in enumerate(selected_records):
                print(f"\n--- Просмотр записи #{i + 1} ---")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", record)
                time.sleep(1)
                record.click()
                time.sleep(3)  # Ждём загрузки

                # Ждём обновления информации под видео
                try:
                    camera_name = self.wait.until(EC.presence_of_element_located(self.NAME_CAMERAS_RECORDING_FRAGMENT_VIDEO)).text
                    date_elem = self.wait.until(EC.presence_of_element_located(self.DATE_RECORDING_FRAGMENT_VIDEO))
                    time_elem = self.wait.until(EC.presence_of_element_located(self.TIME_RECORDING_FRAGMENT_VIDEO))
                    duration_elem = self.wait.until(EC.presence_of_element_located(self.DURATION_RECORDING_FRAGMENT_VIDEO))

                    # Извлечение данных
                    date_from_field = date_elem.text or date_elem.get_attribute("value") or "неизвестно"
                    time_from_field = time_elem.text or time_elem.get_attribute("value") or "неизвестно"
                    duration_from_field = duration_elem.text or duration_elem.get_attribute("value") or "неизвестно"

                    print("=" * 60)
                    print(f"Камера: {camera_name}")
                    print(f"Дата: {date_from_field}")
                    print(f"Время: {time_from_field}")
                    print(f"Длительность: {duration_from_field}")
                    print("=" * 60)

                    # Проверка, что поля не пусты
                    assert camera_name, "Название камеры не найдено."
                    assert date_from_field != "неизвестно", "Дата не найдена."
                    assert time_from_field != "неизвестно", "Время не найдено."
                    assert duration_from_field != "неизвестно", "Длительность не найдена."

                except TimeoutException:
                    print("Не удалось получить данные из полей под видео.")
                    assert False, "Не удалось получить информацию о записи."

                # Ждём видеоэлемент
                try:
                    video_element = self.wait.until(EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                    print("Видео найдено и готово к воспроизведению.")

                    # Ждём, пока появится длительность
                    duration = None
                    for _ in range(20):
                        try:
                            duration = self.driver.execute_script("return arguments[0].duration;", video_element)
                            if duration and duration > 0:
                                print(f"Длительность видео: {duration:.2f} секунд")
                                break
                        except Exception as e:
                            print(f"Ошибка получения длительности: {e}")
                        time.sleep(1)

                    assert duration and duration > 0, "Не удалось определить длительность видео"

                    # Ждём окончания воспроизведения
                    start_time = time.time()
                    while True:
                        try:
                            current_time = self.driver.execute_script("return arguments[0].currentTime;", video_element)
                            if current_time >= duration - 1:
                                print("Видео полностью воспроизведено.")
                                break
                        except Exception as e:
                            print(f"Ошибка получения текущего времени: {e}")
                        time.sleep(1)

                    end_time = time.time()
                    watch_time = end_time - start_time
                    print(f"Время просмотра: {watch_time:.2f} секунд")

                except TimeoutException:
                    print("Видео не загрузилось, пропускаем...")
                    assert False, "Видео не загрузилось, невозможно проверить."

        finally:
            self.driver.quit()

    # ПРОВЕРКА ВОСПРОИЗВЕДЕНИЯ В КАЖДОМ ВАЛИДНОМ ДНЕ ОДИН РАНДОМНЫЙ ФРАГМЕНТ ЗАПИСИ
    allure.step("View one fragment record on each valid day")
    def view_one_fragment_record_on_each_valid_day(self):
        try:
            day_elements = self.wait.until(EC.visibility_of_all_elements_located(self.DATE_CALENDAR_WITH_RECORDING))

            valid_days = []
            for day in day_elements:
                if "disabled" not in day.get_attribute("class") and day.text.strip().isdigit():
                    valid_days.append(day)

            print("Валидные дни:", [d.text for d in valid_days])
            assert len(valid_days) > 0, "Нет доступных дней для выбора."
            print("Есть доступные дни для выбора.")

            # Проходим по каждому валидному дню
            for idx, day in enumerate(valid_days):
                print(f"\n--- Обработка дня #{idx + 1}: {day.text} ---")

                # Кликаем на день
                self.driver.execute_script("arguments[0].scrollIntoView(true);", day)
                time.sleep(1.5)
                day.click()
                time.sleep(2)

                # Ждём загрузки записей
                records = self.wait.until(EC.visibility_of_all_elements_located(self.SEGMENT_RECORDING))
                assert len(records) > 0, f"Записи не найдены для дня {day.text}!"
                print(f"Найдено записей: {len(records)}")

                # Выбираем случайную запись
                random_record = random.choice(records)
                print(f"Выбрана случайная запись: индекс {records.index(random_record)}")

                # Кликаем на запись
                self.driver.execute_script("arguments[0].scrollIntoView(true);", random_record)
                time.sleep(1)
                random_record.click()
                time.sleep(3)

                # Ждём обновления информации под видео
                try:
                    camera_name = self.wait.until(EC.presence_of_element_located(self.NAME_CAMERAS_RECORDING_FRAGMENT_VIDEO)).text
                    date_elem = self.wait.until(EC.presence_of_element_located(self.DATE_RECORDING_FRAGMENT_VIDEO))
                    time_elem = self.wait.until(EC.presence_of_element_located(self.TIME_RECORDING_FRAGMENT_VIDEO))
                    duration_elem = self.wait.until(EC.presence_of_element_located(self.DURATION_RECORDING_FRAGMENT_VIDEO))

                    # Извлечение данных
                    date_from_field = date_elem.text or date_elem.get_attribute("value") or "неизвестно"
                    time_from_field = time_elem.text or time_elem.get_attribute("value") or "неизвестно"
                    duration_from_field = duration_elem.text or duration_elem.get_attribute("value") or "неизвестно"

                    print("=" * 60)
                    print(f"Камера: {camera_name}")
                    print(f"Дата: {date_from_field}")
                    print(f"Время: {time_from_field}")
                    print(f"Длительность: {duration_from_field}")
                    print("=" * 60)

                    # Проверка, что поля не пусты
                    assert camera_name, "Название камеры не найдено."
                    assert date_from_field != "неизвестно", "Дата не найдена."
                    assert time_from_field != "неизвестно", "Время не найдено."
                    assert duration_from_field != "неизвестно", "Длительность не найдена."

                except TimeoutException:
                    print("Не удалось получить данные из полей под видео.")
                    assert False, "Не удалось получить информацию о записи."

                # Ждём видеоэлемент
                try:
                    video_element = self.wait.until(EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                    print("Видео найдено и готово к воспроизведению.")

                    # Ждём, пока появится длительность
                    duration = None
                    for _ in range(20):
                        try:
                            duration = self.driver.execute_script("return arguments[0].duration;", video_element)
                            if duration and duration > 0:
                                print(f"Длительность видео: {duration:.2f} секунд")
                                break
                        except Exception as e:
                            print(f"Ошибка получения длительности: {e}")
                        time.sleep(1)

                    assert duration and duration > 0, "Не удалось определить длительность видео"

                    # Ждём окончания воспроизведения
                    start_time = time.time()
                    while True:
                        try:
                            current_time = self.driver.execute_script("return arguments[0].currentTime;", video_element)
                            if current_time >= duration - 1:
                                print("Видео полностью воспроизведено.")
                                break
                        except Exception as e:
                            print(f"Ошибка получения текущего времени: {e}")
                        time.sleep(1)

                    end_time = time.time()
                    watch_time = end_time - start_time
                    print(f"Время просмотра: {watch_time:.2f} секунд")

                except TimeoutException:
                    print("Видео не загрузилось, пропускаем...")
                    assert False, "Видео не загрузилось, невозможно проверить."

        finally:
            self.driver.quit()

    # ПРОВЕРКА АВТОВОСПРОИЗВЕДЕНИЯ РАНДОМНО ЧЕТЫРЕХ ФРАГМЕНТОВ ЗАПИСИ
    allure.step("Checking auto-playback fragments from camera")
    def checking_autoplayback_fragments_from_camera(self):
        try:

            day_elements = self.wait.until(EC.visibility_of_all_elements_located(self.DATE_CALENDAR_WITH_RECORDING))

            valid_days = []
            for day in day_elements:
                if "disabled" not in day.get_attribute("class") and day.text.strip().isdigit():
                    valid_days.append(day)

            # Выводим список валидных дней один раз
            print("Валидные дни:", [d.text for d in valid_days])

            # Проверка, что есть хотя бы один валидный день
            assert len(valid_days) > 0, "Нет доступных дней для выбора."
            print("Есть доступные дни для выбора.")

            random_valid_day = random.choice(valid_days)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", random_valid_day)
            time.sleep(1.5)
            print(f"Кликаем на день: {random_valid_day.text}")
            random_valid_day.click()
            time.sleep(1.5)

            # Проверка, что чекбокс "Автовоспроизведение" существует
            autoplay_checkbox = self.wait.until(EC.element_to_be_clickable(self.CHECKBOX_AUTOPLAY))
            assert autoplay_checkbox is not None, "Чекбокс 'Автовоспроизведение' не найден."

            # Активация автовоспроизведения
            if not autoplay_checkbox.is_selected():
                autoplay_checkbox.click()
                time.sleep(1)
                # Проверка, что чекбокс стал активным
                assert autoplay_checkbox.is_selected(), "Не удалось активировать автовоспроизведение."

            # Проверка наличия записей
            records = self.wait.until(EC.visibility_of_all_elements_located(self.SEGMENT_RECORDING))
            assert len(records) > 0, "Записи не найдены!"
            print(f"Найдено записей: {len(records)}")

            # Начальная запись
            start_record = random.choice(records)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", start_record)
            start_record.click()
            time.sleep(5)

            # Список следующих 3 записей
            start_index = records.index(start_record)
            next_records = records[start_index + 1:start_index + 4]

            # Воспроизводим начальную и следующие 3
            all_records_to_watch = [start_record] + next_records

            for record in all_records_to_watch:
                record.click()
                time.sleep(2)

                #  Ждём, пока обновятся поля под видео
                try:

                    camera_name = self.wait.until(EC.presence_of_element_located(self.NAME_CAMERAS_RECORDING_FRAGMENT_VIDEO)).text
                    date_elem = self.wait.until(EC.presence_of_element_located(self.DATE_RECORDING_FRAGMENT_VIDEO))
                    time_elem = self.wait.until(EC.presence_of_element_located(self.TIME_RECORDING_FRAGMENT_VIDEO))
                    duration_elem = self.wait.until(EC.presence_of_element_located(self.DURATION_RECORDING_FRAGMENT_VIDEO))

                    #  Извлечение данных из полей
                    date_from_field = date_elem.text or date_elem.get_attribute("value") or "неизвестно"
                    time_from_field = time_elem.text or time_elem.get_attribute("value") or "неизвестно"
                    duration_from_field = duration_elem.text or duration_elem.get_attribute("value") or "неизвестно"

                    # Вывод информации
                    print("=" * 50)
                    print(f"Камера: {camera_name}")
                    print(f"Дата (из поля): {date_from_field}")
                    print(f"Время (из поля): {time_from_field}")
                    print(f"Длительность (из поля): {duration_from_field}")
                    print("=" * 50)

                    # Проверка, что поля не пусты
                    assert camera_name, "Название камеры не найдено."
                    assert date_from_field != "неизвестно", "Дата не найдена."
                    assert time_from_field != "неизвестно", "Время не найдено."
                    assert duration_from_field != "неизвестно", "Длительность не найдена."


                except TimeoutException:
                    print("Не удалось получить данные из полей под видео.")
                    assert False, "Не удалось получить информацию о записи."

                # Ожидаем видеоэлемент
                try:
                    video_element = self.wait.until(EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                    print("Видео найдено и готово к воспроизведению.")

                    # Проверка, что видео действительно загружено
                    assert video_element, "Видеоэлемент не найден."

                    # Ждём, пока появится длительность
                    duration = None
                    for _ in range(20):
                        try:
                            duration = self.driver.execute_script("return arguments[0].duration;", video_element)
                            if duration and duration > 0:
                                print(f"Длительность видео: {duration:.2f} секунд")
                                break
                        except Exception as e:
                            print(f"Ошибка получения длительности: {e}")
                        time.sleep(1)

                    assert duration and duration > 0, "Не удалось определить длительность видео"

                    # Ждём окончания воспроизведения
                    start_time = time.time()
                    while True:
                        try:
                            current_time = self.driver.execute_script("return arguments[0].currentTime;", video_element)
                            if current_time >= duration - 1:  # погрешность
                                print("Видео полностью воспроизведено.")
                                break
                        except Exception as e:
                            print(f"Ошибка получения текущего времени: {e}")
                        time.sleep(1)

                    end_time = time.time()
                    watch_time = end_time - start_time
                    print(f"Время просмотра: {watch_time:.2f} секунд")

                except TimeoutException:
                    print("Видео не загрузилось, пропускаем...")
                    assert False, "Видео не загрузилось, невозможно проверить автовоспроизведение."

        finally:
            self.driver.quit()
