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
from selenium.webdriver.common.by import By
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
    TIMELINE_CONTROLBAR = ("xpath", "//div[contains(@class, 'player-main-controlbar-seek-progress-left')][contains(@style, 'width')]")  # таймлайн плейера
    BUTTON_PAUSE_CONTROLBAR = ("xpath", "//div[@class='player-main-controlbar-play player-main-controlbar-pause']")  # кнопка pause в плеере
    BUTTON_PLAY_CONTROLBAR = ("xpath", "//div[@class='player-main-controlbar-play']")  # кнопка play в плеере
    LIST_DEVICES = ("xpath", "//li[contains(@rel, 'channel')]")  # список камер

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
        print("Функция запущена")
        print("Ожидание списка устройств...")
        try:
            self.wait.until(lambda d: self.driver.find_elements(*self.LIST_DEVICES))
            print("Список устройств найден.")
        except Exception as e:
            print(f"Ошибка ожидания списка устройств: {e}")
            raise

        time.sleep(1.5)

        print("Поиск активных камер...")
        try:
            active_cameras = self.driver.find_elements(*self.ACTIVE_CAMERAS_INSIDE_LIST)
            print(f"Найдено {len(active_cameras)} активных камер.")
        except Exception as e:
            print(f"Ошибка поиска активных камер: {e}")
            raise

        assert active_cameras, "Не найдено ни одной активной камеры"

        target_li = random.choice(active_cameras)
        a_element = target_li.find_element(By.TAG_NAME, "a")

        camera_name = a_element.text.strip()
        print(f"Выбрана камера: {camera_name}")

        print("Проверка видимости и кликабельности...")
        print("Is displayed?", a_element.is_displayed())
        print("Is enabled?", a_element.is_enabled())

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", a_element)
        time.sleep(0.5)

        print("Проверка кликабельности...")
        try:
            self.wait.until(EC.element_to_be_clickable(a_element))
            print("Элемент кликабелен.")
        except Exception as e:
            print(f"Элемент не кликабелен: {e}")
            self.driver.save_screenshot("not_clickable.png")
            raise

        print("Клик по элементу...")
        try:
            a_element.click()
            print("Клик выполнен успешно.")
        except Exception as e:
            print(f"Ошибка клика: {e}")
            self.driver.save_screenshot("click_failed.png")
            raise

        print("Проверка выделения...")
        class_attr = a_element.get_attribute("class") or ""
        print(f"Классы элемента: {class_attr}")
        assert "jstree-clicked" in class_attr, f"Камера не выделилась. Классы: {class_attr}"
        print("Камера успешно выделена.")

    # ПРОВЕРКА ВОСПРОИЗВЕДЕНИЯ В ОДНОМ РАНДОМНОМ ДНЕ РАНДОМНО ОДИН ФРАГМЕНТ ЗАПИСИ
    allure.step("Viewing fragment from camera")

    def viewing_fragment_from_camera(self):

        print("\n Начало просмотра фрагмента")

        # Шаг 1: Найти дни с записями
        day_elements = self.wait.until(EC.visibility_of_all_elements_located(self.DATE_CALENDAR_WITH_RECORDING))
        valid_days = []
        for day in day_elements:
            class_attr = day.get_attribute("class")
            if "disabled" not in class_attr and day.text.strip().isdigit():
                valid_days.append(day)

        assert len(valid_days) > 0, "Нет доступных дней для выбора."
        print(f"Найдено {len(valid_days)} валидных дней.")

        # Цикл перезапуска фрагмента
        restart_attempt = 0
        max_restart_attempts = 3 # Максимальное количество попыток перезапуска фрагмента

        while restart_attempt <= max_restart_attempts:
            restart_attempt += 1
            print(f"\n Попытка воспроизведения #{restart_attempt}")

            try:
                # Выбор дня и фрагмента (Эта логика выполняется при каждом запуске/перезапуске)
                random_valid_day = random.choice(valid_days)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", random_valid_day)
                time.sleep(1.5)
                print(f"Кликаю на день: {random_valid_day.text}")
                random_valid_day.click()
                time.sleep(2) # Обязательно надо подождать

                records = self.wait.until(EC.visibility_of_all_elements_located(self.SEGMENT_RECORDING))
                assert len(records) > 0, "Записи не найдены!"

                print(f"Найдено {len(records)} фрагментов. Выбираю случайный...")
                random_record = random.choice(records)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", random_record)
                random_record.click()
                time.sleep(5) # Обязательно надо подождать

                # Получения информации о видео
                camera_name_element = self.wait.until(EC.presence_of_element_located(self.NAME_CAMERAS_RECORDING_FRAGMENT_VIDEO))
                camera_name = camera_name_element.text

                date_elem = self.wait.until(EC.presence_of_element_located(self.DATE_RECORDING_FRAGMENT_VIDEO))
                time_elem = self.wait.until(EC.presence_of_element_located(self.TIME_RECORDING_FRAGMENT_VIDEO))
                duration_elem = self.wait.until(EC.presence_of_element_located(self.DURATION_RECORDING_FRAGMENT_VIDEO))

                date_from_field = date_elem.text or date_elem.get_attribute("value") or "неизвестно"
                time_from_field = time_elem.text or time_elem.get_attribute("value") or "неизвестно"
                duration_from_field = duration_elem.text or duration_elem.get_attribute("value") or "неизвестно"

                assert camera_name, "Название камеры не найдено."
                assert date_from_field != "неизвестно", "Дата не найдена."
                assert time_from_field != "неизвестно", "Время не найдено."
                assert duration_from_field != "неизвестно", "Длительность не найдена."

                print("=" * 70)
                print(f"Камера: {camera_name}")
                print(f"Дата (из поля): {date_from_field}")
                print(f"Время (из поля): {time_from_field}")
                print(f"Длительность (из поля): {duration_from_field}")
                print("=" * 70)

                # Получения видеоэлемента и длительности
                video_element = self.wait.until(EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                assert video_element is not None, "Видеоэлемент не найден после ожидания."

                duration = None
                for _ in range(20):
                    try:
                        duration = self.driver.execute_script("return arguments[0].duration;", video_element)
                        if duration and duration > 0:
                            print(f"Длительность видео: {duration:.2f} секунд")
                            break
                    except Exception as e:
                        print(f"Повторная попытка получения длительности: {e}")
                    time.sleep(1)

                assert duration and duration > 0, f"Не удалось определить длительность видео. Значение: {duration}"

                # Цикл мониторинга воспроизведения
                start_time = time.time()

                try:
                    timeline_element = self.wait.until(EC.presence_of_element_located(self.TIMELINE_CONTROLBAR))
                    initial_style = timeline_element.get_attribute("style")
                    print(f"Начальное значение таймлайна: {initial_style[:50]}...") # Обрезаем для читаемости
                except TimeoutException:
                    print("Элемент таймлайна не найден или стиль недоступен.")
                    timeline_element = None
                    initial_style = ""

                last_known_time = self.driver.execute_script("return arguments[0].currentTime;", video_element)
                print(f"Начальное время воспроизведения: {last_known_time:.2f}")

                # Ждём окончания воспроизведения с проверкой остановки
                no_change_count = 0
                max_no_change_count_for_recovery = 60
                actions = ActionChains(self.driver)
                stop_start_time = None
                failed_recovery_attempts = 0 # Счётчик неудачных попыток восстановления
                max_failed_recovery_attempts = 2 # Максимальное количество неудачных восстановлений перед перезапуском фрагмента

                while True:
                    try:
                        current_time = self.driver.execute_script("return arguments[0].currentTime;", video_element)
                        current_timeline_style = timeline_element.get_attribute("style") if timeline_element else ""
                        time_changed = abs(current_time - last_known_time) > 0.1
                        timeline_changed = current_timeline_style != initial_style if timeline_element else False

                        if time_changed or timeline_changed:
                            if time_changed:
                                last_known_time = current_time
                            if timeline_changed and timeline_element:
                                initial_style = current_timeline_style
                            no_change_count = 0
                            failed_recovery_attempts = 0 # Сбрасываем счётчик неудач, если воспроизведение идёт

                            if stop_start_time is not None:
                                elapsed_while_stopped = int(time.time() - stop_start_time)
                                print(f"Воспроизведение возобновилось после остановки (~{elapsed_while_stopped} сек).")
                                stop_start_time = None

                            if current_time >= duration - 1:
                                print("Видео полностью воспроизведено.")
                                print(f" Попытка #{restart_attempt} УСПЕШНО завершена")
                                return

                        else:
                            no_change_count += 1
                            if stop_start_time is None:
                                stop_start_time = time.time()

                            if no_change_count == max_no_change_count_for_recovery:
                                elapsed_while_stopped = int(time.time() - stop_start_time)
                                print(f"Воспроизведение, кажется, остановилось более чем на {elapsed_while_stopped} секунд (~{no_change_count} проверок).")

                            if no_change_count >= max_no_change_count_for_recovery:
                                print("Пытаюсь восстановить воспроизведение через паузу/плей...")
                                # АЛГОРИТМ ВОССТАНОВЛЕНИЯ
                                actions.move_to_element(video_element).perform()
                                time.sleep(1)

                                print("Нажимаю паузу...")
                                try:
                                    pause_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_PAUSE_CONTROLBAR))
                                    pause_button.click()
                                except Exception as e_pause:
                                    print(f"Кнопка паузы не найдена или ошибка: {e_pause}")

                                time.sleep(2) # Обязательно надо подождать

                                actions.move_to_element(video_element).perform()
                                time.sleep(1)

                                print("Нажимаю плей...")
                                try:
                                    play_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_PLAY_CONTROLBAR))
                                    play_button.click()
                                except Exception as e_play:
                                    print(f"Кнопка плей не найдена или ошибка: {e_play}")

                                # Проверка успешности восстановления
                                print("Проверяю, возобновилось ли воспроизведение...")
                                restored_check_start_time = time.time()
                                restored_check_duration = 10
                                previous_time_after_restore = self.driver.execute_script("return arguments[0].currentTime;", video_element)

                                restoration_successful = False
                                while time.time() - restored_check_start_time < restored_check_duration:
                                    time.sleep(1)
                                    current_time_after_restore = self.driver.execute_script("return arguments[0].currentTime;", video_element)
                                    if abs(current_time_after_restore - previous_time_after_restore) > 0.1:
                                        print("Воспроизведение успешно возобновлено через паузу/плей.")
                                        restoration_successful = True
                                        last_known_time = current_time_after_restore
                                        break
                                    previous_time_after_restore = current_time_after_restore

                                if not restoration_successful:
                                    failed_recovery_attempts += 1
                                    print(f"ПРЕДУПРЕЖДЕНИЕ: Попытка восстановления #{failed_recovery_attempts} не удалась.")
                                    if failed_recovery_attempts >= max_failed_recovery_attempts:
                                         print(f"Исчерпан лимит попыток восстановления ({max_failed_recovery_attempts}).")
                                         print(f"Прерываю текущий фрагмент и пытаюсь перезапустить его (попытка #{restart_attempt}).")
                                         raise RuntimeError("Failed to resume playback after multiple attempts. Restarting fragment.") # Возбуждаем исключение для перезапуска

                                # Сбрасываем счётчики и время остановки, если восстановление прошло успешно
                                if restoration_successful:
                                    no_change_count = 0
                                    stop_start_time = None
                                    continue # Переходим к следующей итерации основного цикла

                                # Если восстановление не удалось, но количество неудач < max, продолжаем ждать
                                # Счётчик no_change_count остаётся высоким, и мы снова попадём сюда в следующую итерацию


                        time.sleep(1)

                    except StaleElementReferenceException:
                        print("Обнаружена ошибка StaleElementReferenceException, возможно, DOM изменился.")
                        try:
                            video_element = self.wait.until(EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                            current_time = self.driver.execute_script("return arguments[0].currentTime;", video_element)
                            print(f"Текущее время после обновления элемента: {current_time:.2f}")
                            if abs(current_time - last_known_time) > 0.1:
                                print("Видео продолжает воспроизводиться после обновления элемента")
                                last_known_time = current_time
                                no_change_count = 0
                                stop_start_time = None
                            else:
                                print("Видео не воспроизводится после обновления элемента")
                                no_change_count += 1
                                if stop_start_time is None:
                                    stop_start_time = time.time()
                        except Exception as e_scroll:
                            print(f"Ошибка при повторном поиске видеоэлемента: {e_scroll}")
                            # Попробовать восстановление или перезапуск
                            failed_recovery_attempts += 1
                            if failed_recovery_attempts >= max_failed_recovery_attempts:
                                print(f"Ошибка StaleElementReference и неудачные восстановления. Прерываю текущий фрагмент.")
                                raise RuntimeError("StaleElement and failed resume. Restarting fragment.")
                        continue # Продолжаем цикл, возможно с обновлённым элементом

                    except Exception as e:
                        print(f"Неожиданная ошибка при проверке воспроизведения: {e}")
                        break # Выход из цикла воспроизведения

                # Если мы вышли из цикла воспроизведения не через return, значит, что-то пошло не так
                print(f"Цикл воспроизведения завершён (возможно, с ошибкой) на попытке #{restart_attempt}.")
                # Цикл while restart_attempt <= max_restart_attempts продолжится, если было raise RuntimeError

            except RuntimeError as re:
                print(f"Ошибка во время попытки #{restart_attempt}: {re}")
                if restart_attempt <= max_restart_attempts:
                    print(f"Перезапускаю фрагмент... (осталось попыток: {max_restart_attempts - restart_attempt})")
                    continue # Переход к следующей итерации внешнего цикла (выбор нового дня/фрагмента)
                else:
                    print(f"Исчерпан лимит попыток перезапуска фрагмента ({max_restart_attempts}). Тест завершается с ошибкой.")
                    raise # Повторно выбрасываем исключение, чтобы тест завершился неудачно

            except Exception as e:
                print(f"Неожиданная ошибка в блоке выбора фрагмента или воспроизведения: {e}")
                # Если ошибка произошла вне цикла воспроизведения или не связана с восстановлением
                if restart_attempt <= max_restart_attempts:
                    print(f"Произошла ошибка, пытаюсь перезапустить фрагмент... (осталось попыток: {max_restart_attempts - restart_attempt})")
                    continue
                else:
                    print(f"Исчерпан лимит попыток перезапуска фрагмента ({max_restart_attempts}). Тест завершается с ошибкой.")
                    raise # Повторно выбрасываем исключение, чтобы тест завершился неудачно

        # Если мы дошли до этой строки, значит, все попытки перезапуска исчерпаны
        # Цикл while закончился, и ни одна из попыток не завершилась успешно (с `return`)
        assert False, f"Не удалось успешно воспроизвести фрагмент за {max_restart_attempts} попыток перезапуска."


    # ПРОВЕРКА ВОСПРОИЗВЕДЕНИЯ В ОДНОМ РАНДОМНОМ ДНЕ ЧЕТЫРЕ РАНДОМНЫХ ФРАГМЕНТОВ ЗАПИСИ
    allure.step(("Viewing four fragments one days recording"))
    def viewing_four_fragments_one_days_recording(self):

        print("\n Начало просмотра 4 фрагментов из одного дня")

        # Находим дни с записями
        day_elements = self.wait.until(EC.visibility_of_all_elements_located(self.DATE_CALENDAR_WITH_RECORDING))

        valid_days = []
        for day in day_elements:
            class_attr = day.get_attribute("class")
            if "disabled" not in class_attr and day.text.strip().isdigit():
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
            print(f"\n Просмотр записи #{i + 1} ")
            restart_attempt = 0
            max_restart_attempts = 2  # Максимальное количество попыток перезапуска этого фрагмента

            success = False
            while restart_attempt <= max_restart_attempts and not success:
                restart_attempt += 1
                print(f"Попытка воспроизведения фрагмента #{i + 1} (попытка {restart_attempt})")

                # Клик и получения информации
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", record)
                    time.sleep(1)
                    record.click()
                    time.sleep(3)  # обязательно нужно

                    # Ждём обновления информации под видео
                    camera_name = self.wait.until(
                        EC.presence_of_element_located(self.NAME_CAMERAS_RECORDING_FRAGMENT_VIDEO)).text
                    date_elem = self.wait.until(EC.presence_of_element_located(self.DATE_RECORDING_FRAGMENT_VIDEO))
                    time_elem = self.wait.until(EC.presence_of_element_located(self.TIME_RECORDING_FRAGMENT_VIDEO))
                    duration_elem = self.wait.until(
                        EC.presence_of_element_located(self.DURATION_RECORDING_FRAGMENT_VIDEO))

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

                except (TimeoutException, AssertionError) as e:
                    print(f"Ошибка получения информации о фрагменте: {e}")
                    if restart_attempt <= max_restart_attempts:
                        print(
                            f"Пытаюсь перезапустить фрагмент... (осталось попыток: {max_restart_attempts - restart_attempt})")
                        continue  # Переходим к следующей итерации while (повторный клик)
                    else:
                        print(f"Исчерпан лимит попыток для фрагмента #{i + 1}. Пропускаю.")
                        break  # Переходим к следующему фрагменту в for

                # Получаем видеоэлемент и длительность
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

                except (TimeoutException, AssertionError) as e:
                    print(f"Ошибка загрузки видео или получения длительности: {e}")
                    if restart_attempt <= max_restart_attempts:
                        print(
                            f"Пытаюсь перезапустить фрагмент... (осталось попыток: {max_restart_attempts - restart_attempt})")
                        continue
                    else:
                        print(f"Исчерпан лимит попыток для фрагмента #{i + 1}. Пропускаю.")
                        break  # Переходим к следующему фрагменту в for

                # Мониторинг воспроизведения с остановкой и восстановлением
                print(f"Начинаю мониторинг воспроизведения (длительность: {duration:.2f}s).")
                start_time = time.time()

                # Попробуем получить таймлайн, если он есть
                timeline_element = None
                initial_style = ""
                try:
                    timeline_element = self.wait.until(EC.presence_of_element_located(self.TIMELINE_CONTROLBAR))
                    initial_style = timeline_element.get_attribute("style")
                    print(f"Начальное значение таймлайна: {initial_style[:50]}")  # Обрезаем для читаемости
                except TimeoutException:
                    print("Элемент таймлайна не найден или стиль недоступен.")

                # Получаем начальное время воспроизведения
                last_known_time = self.driver.execute_script("return arguments[0].currentTime;", video_element)
                print(f"Начальное время воспроизведения: {last_known_time:.2f}")

                # Ждём окончания воспроизведения с проверкой остановки
                no_change_count = 0
                max_no_change_count_for_recovery = 60  # Время ожидания до восстановления
                max_failed_recovery_attempts = 2  # Максимум неудачных попыток восстановления перед перезапуском
                actions = ActionChains(self.driver)
                stop_start_time = None
                failed_recovery_attempts = 0

                while True:
                    try:
                        current_time = self.driver.execute_script("return arguments[0].currentTime;", video_element)
                        current_timeline_style = timeline_element.get_attribute("style") if timeline_element else ""

                        time_changed = abs(current_time - last_known_time) > 0.1
                        timeline_changed = current_timeline_style != initial_style if timeline_element else False

                        if time_changed or timeline_changed:
                            if time_changed:
                                last_known_time = current_time
                            if timeline_changed and timeline_element:
                                initial_style = current_timeline_style
                            no_change_count = 0
                            failed_recovery_attempts = 0  # Сбрасываем счётчик неудач, если воспроизведение идёт

                            if stop_start_time is not None:
                                elapsed_while_stopped = int(time.time() - stop_start_time)
                                print(
                                    f"Воспроизведение возобновилось после остановки (~{elapsed_while_stopped} сек).")
                                stop_start_time = None

                            if current_time >= duration - 1:  # Добавим небольшой запас
                                print("Видео полностью воспроизведено.")
                                success = True
                                break  # Выходим из цикла воспроизведения, переходим к следующему фрагменту

                        else:
                            no_change_count += 1
                            if stop_start_time is None:
                                stop_start_time = time.time()

                            if no_change_count == max_no_change_count_for_recovery:
                                elapsed_while_stopped = int(time.time() - stop_start_time)
                                print(
                                    f"Воспроизведение, кажется, остановилось более чем на {elapsed_while_stopped} секунд (~{no_change_count} проверок).")

                            if no_change_count >= max_no_change_count_for_recovery:
                                print("Пытаюсь восстановить воспроизведение через паузу/плей.")
                                # АЛГОРИТМ ВОССТАНОВЛЕНИЯ
                                actions.move_to_element(video_element).perform()
                                time.sleep(1)

                                print("Нажимаю паузу...")
                                try:
                                    pause_button = self.wait.until(
                                        EC.element_to_be_clickable(self.BUTTON_PAUSE_CONTROLBAR))
                                    pause_button.click()
                                except Exception as e_pause:
                                    print(f"Кнопка паузы не найдена или ошибка: {e_pause}")

                                time.sleep(2)  # Обязательно нужно

                                actions.move_to_element(video_element).perform()
                                time.sleep(1)

                                print("Нажимаю плей...")
                                try:
                                    play_button = self.wait.until(
                                        EC.element_to_be_clickable(self.BUTTON_PLAY_CONTROLBAR))
                                    play_button.click()
                                except Exception as e_play:
                                    print(f"Кнопка плей не найдена или ошибка: {e_play}")

                                # Проверка успешности восстановления
                                print("Проверяю, возобновилось ли воспроизведение.")
                                restored_check_start_time = time.time()
                                restored_check_duration = 10
                                previous_time_after_restore = self.driver.execute_script(
                                    "return arguments[0].currentTime;", video_element)

                                restoration_successful = False
                                while time.time() - restored_check_start_time < restored_check_duration:
                                    time.sleep(1)
                                    current_time_after_restore = self.driver.execute_script(
                                        "return arguments[0].currentTime;", video_element)
                                    if abs(current_time_after_restore - previous_time_after_restore) > 0.1:
                                        print("Воспроизведение успешно возобновлено через паузу/плей.")
                                        restoration_successful = True
                                        last_known_time = current_time_after_restore
                                        break
                                    previous_time_after_restore = current_time_after_restore

                                if not restoration_successful:
                                    failed_recovery_attempts += 1
                                    print(
                                        f"ПРЕДУПРЕЖДЕНИЕ: Попытка восстановления #{failed_recovery_attempts} не удалась.")
                                    if failed_recovery_attempts >= max_failed_recovery_attempts:
                                        print(
                                            f"Исчерпан лимит попыток восстановления ({max_failed_recovery_attempts}).")
                                        print(
                                            f"Прерываю текущий фрагмент и возвращаюсь к выбору следующего.")
                                        break  # Выходим из цикла воспроизведения, переходя к следующей итерации while (перезапуск)

                                # Сбрасываем счётчики и время остановки, если восстановление прошло успешно
                                if restoration_successful:
                                    no_change_count = 0
                                    stop_start_time = None
                                    continue  # Переходим к следующей итерации основного цикла

                                # Если восстановление не удалось, но количество неудач < max, продолжаем ждать
                                # Счётчик no_change_count остаётся высоким, и мы снова попадём сюда в следующую итерацию

                        time.sleep(1)

                    except StaleElementReferenceException:
                        print("Обнаружена ошибка StaleElementReferenceException, возможно, DOM изменился.")
                        try:
                            # Попробуем заново найти видеоэлемент с ожиданием
                            current_video_element = self.wait.until(
                                EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                            current_time = self.driver.execute_script("return arguments[0].currentTime;",
                                                                      current_video_element)
                            print(f"Текущее время после обновления элемента: {current_time:.2f}")
                            if abs(current_time - last_known_time) > 0.1:
                                print("Видео продолжает воспроизводиться после обновления элемента")
                                last_known_time = current_time
                                no_change_count = 0
                                stop_start_time = None
                            else:
                                print("Видео не воспроизводится после обновления элемента")
                                no_change_count += 1
                                if stop_start_time is None:
                                    stop_start_time = time.time()
                        except Exception as e_scroll:
                            print(f"Ошибка при повторном поиске видеоэлемента: {e_scroll}")
                            # Можно попробовать восстановление или перезапуск
                            failed_recovery_attempts += 1
                            if failed_recovery_attempts >= max_failed_recovery_attempts:
                                print(
                                    f"Ошибка StaleElementReference и неудачные восстановления. Прерываю текущий фрагмент.")
                                break  # Выходим из цикла воспроизведения, переходим к следующей итерации while (перезапуск)
                        continue  # Продолжаем цикл, возможно с обновлённым элементом

                    except Exception as e:
                        print(f"Неожиданная ошибка при проверке воспроизведения: {e}")
                        break  # Выходим из цикла воспроизведения, переходим к следующей итерации while (перезапуск)

                # Если цикл воспроизведения завершён, но success не True, значит, восстановление не помогло
                if not success:
                    if restart_attempt <= max_restart_attempts:
                        print(
                            f"Воспроизведение фрагмента #{i + 1} не удалось. Пытаюсь перезапустить... (осталось попыток: {max_restart_attempts - restart_attempt})")
                        # Цикл while продолжается, начинается новая попытка (restart_attempt)
                        # Снова будет клик по `record`, что и является "перезапуском" фрагмента в текущем контексте
                    else:
                        print(f"Исчерпан лимит попыток воспроизведения для фрагмента #{i + 1}. Пропускаю.")

            # После завершения попыток для текущего фрагмента
            if not success:
                print(f"Фрагмент #{i + 1} не был успешно воспроизведён за {max_restart_attempts} попыток.")
            else:
                print(f"Фрагмент #{i + 1} успешно воспроизведён.")

        print("\n Завершено просмотра 4 фрагментов из одного дня.")

    # ПРОВЕРКА ВОСПРОИЗВЕДЕНИЯ В КАЖДОМ ВАЛИДНОМ ДНЕ ОДИН РАНДОМНЫЙ ФРАГМЕНТ ЗАПИСИ
    allure.step("View one fragment record on each valid day")
    def view_one_fragment_record_on_each_valid_day(self):

            print("\n  Начало просмотра одного фрагмента из каждого дня с записью")

            # Вспомогательная функция для обработки одного дня ---
            def process_day(day_element, month_label=""):
                print(f"\n Обработка дня в {month_label}месяце: {day_element.text}")
                restart_attempt = 0
                max_restart_attempts = 2  # Максимальное количество попыток перезапуска этого фрагмента

                success = False
                while restart_attempt <= max_restart_attempts and not success:
                    restart_attempt += 1
                    print(f"Попытка воспроизведения фрагмента (попытка {restart_attempt}).")

                    # Клик и получение информации
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", day_element)
                        time.sleep(1.5)
                        day_element.click()
                        time.sleep(1.5)

                        # Проверка наличия записей
                        records = self.wait.until(EC.visibility_of_all_elements_located(self.SEGMENT_RECORDING))
                        assert len(records) > 0, "Записи не найдены!"
                        print(f"Найдено записей: {len(records)}")

                        # Выбираем 1 случайную запись для просмотра
                        selected_record = random.choice(records)
                        print(f"Выбрана запись для просмотра: {records.index(selected_record) + 1}")

                        # Просматриваем выбранную запись
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", selected_record)
                        time.sleep(1)
                        selected_record.click()
                        time.sleep(8)  # Увеличенное ожидание для загрузки видео

                        # Ждём обновления информации под видео
                        camera_name = self.wait.until(
                            EC.presence_of_element_located(self.NAME_CAMERAS_RECORDING_FRAGMENT_VIDEO)).text
                        date_elem = self.wait.until(EC.presence_of_element_located(self.DATE_RECORDING_FRAGMENT_VIDEO))
                        time_elem = self.wait.until(EC.presence_of_element_located(self.TIME_RECORDING_FRAGMENT_VIDEO))
                        duration_elem = self.wait.until(
                            EC.presence_of_element_located(self.DURATION_RECORDING_FRAGMENT_VIDEO))

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

                    except (TimeoutException, AssertionError) as e:
                        print(f"Ошибка получения информации о фрагменте: {e}")
                        if restart_attempt <= max_restart_attempts:
                            print(
                                f"Пытаюсь перезапустить фрагмент... (осталось попыток: {max_restart_attempts - restart_attempt})")
                            continue  # Переходим к следующей итерации while (повторный клик)
                        else:
                            print(f"Исчерпан лимит попыток. Пропускаю день.")
                            return  # Выходим из функции обработки дня

                    # Получение видеоэлемента и длительности
                    try:
                        video_element = self.wait.until(EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                        print("Видео найдено и готово к воспроизведению.")

                        # Перемещаем мышь к области видео, чтобы активировать элементы управления
                        actions = ActionChains(self.driver)
                        actions.move_to_element(video_element).perform()
                        time.sleep(2)  # Даем время для появления элементов управления

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

                    except (TimeoutException, AssertionError) as e:
                        print(f"Ошибка загрузки видео или получения длительности: {e}")
                        if restart_attempt <= max_restart_attempts:
                            print(
                                f"Пытаюсь перезапустить фрагмент... (осталось попыток: {max_restart_attempts - restart_attempt})")
                            continue
                        else:
                            print(f"Исчерпан лимит попыток. Пропускаю день.")
                            return  # Выходим из функции обработки дня

                    # Мониторинг воспроизведения с остановкой и восстановлением
                    print(f"Начинаю мониторинг воспроизведения (длительность: {duration:.2f}s).")
                    start_time = time.time()

                    # Попробуем получить таймлайн, если он есть
                    timeline_element = None
                    initial_style = ""
                    try:
                        timeline_element = self.wait.until(EC.presence_of_element_located(self.TIMELINE_CONTROLBAR))
                        initial_style = timeline_element.get_attribute("style")
                        print(f" Начальное значение таймлайна: {initial_style[:50]}...")  # Обрезаем для читаемости
                    except TimeoutException:
                        print("Элемент таймлайна не найден или стиль недоступен.")

                    # Получаем начальное время воспроизведения
                    # Дожидаемся, пока элемент появится, а затем получаем его
                    video_element_for_time = self.wait.until(EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                    last_known_time = self.driver.execute_script("return arguments[0].currentTime;",
                                                                 video_element_for_time)
                    print(f"Начальное время воспроизведения: {last_known_time:.2f}")

                    # Ждём окончания воспроизведения с проверкой остановки
                    no_change_count = 0
                    max_no_change_count_for_recovery = 60  # Время ожидания до восстановления
                    max_failed_recovery_attempts = 2  # Максимум неудачных попыток восстановления перед перезапуском
                    actions = ActionChains(self.driver)
                    stop_start_time = None
                    failed_recovery_attempts = 0

                    while True:
                        try:
                            # В каждой итерации снова получаем элемент, на случай StaleElement
                            current_video_element = self.wait.until(
                                EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                            current_time = self.driver.execute_script("return arguments[0].currentTime;",
                                                                      current_video_element)

                            current_timeline_style = timeline_element.get_attribute("style") if timeline_element else ""

                            time_changed = abs(current_time - last_known_time) > 0.1
                            timeline_changed = current_timeline_style != initial_style if timeline_element else False

                            if time_changed or timeline_changed:
                                if time_changed:
                                    last_known_time = current_time
                                if timeline_changed and timeline_element:
                                    initial_style = current_timeline_style
                                no_change_count = 0
                                failed_recovery_attempts = 0  # Сбрасываем счётчик неудач, если воспроизведение идёт

                                if stop_start_time is not None:
                                    elapsed_while_stopped = int(time.time() - stop_start_time)
                                    print(
                                        f"Воспроизведение возобновилось после остановки (~{elapsed_while_stopped} сек).")
                                    stop_start_time = None

                                if current_time >= duration - 1:  # Добавим небольшой запас
                                    print("Видео полностью воспроизведено.")
                                    success = True  # Помечаем, что этот фрагмент успешно завершён
                                    break  # Выходим из цикла воспроизведения, переходим к следующему дню (если есть)

                            else:
                                no_change_count += 1
                                if stop_start_time is None:
                                    stop_start_time = time.time()

                                if no_change_count == max_no_change_count_for_recovery:
                                    elapsed_while_stopped = int(time.time() - stop_start_time)
                                    print(
                                        f"Воспроизведение, кажется, остановилось более чем на {elapsed_while_stopped} секунд (~{no_change_count} проверок).")

                                if no_change_count >= max_no_change_count_for_recovery:
                                    print("Пытаюсь восстановить воспроизведение через паузу/плей.")
                                    # АЛГОРИТМ ВОССТАНОВЛЕНИЯ
                                    actions.move_to_element(self.wait.until(
                                        EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))).perform()
                                    time.sleep(1)

                                    print("Нажимаю паузу...")
                                    try:
                                        pause_button = self.wait.until(
                                            EC.element_to_be_clickable(self.BUTTON_PAUSE_CONTROLBAR))
                                        pause_button.click()
                                    except Exception as e_pause:
                                        print(f"Кнопка паузы не найдена или ошибка: {e_pause}")

                                    time.sleep(2)  # обязатено надо подождать

                                    actions.move_to_element(self.wait.until(
                                        EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))).perform()
                                    time.sleep(1)

                                    print("Нажимаю плей...")
                                    try:
                                        play_button = self.wait.until(
                                            EC.element_to_be_clickable(self.BUTTON_PLAY_CONTROLBAR))
                                        play_button.click()
                                    except Exception as e_play:
                                        print(f"Кнопка плей не найдена или ошибка: {e_play}")

                                    # Проверка успешности восстановления
                                    print("Проверяю, возобновилось ли воспроизведение.")
                                    restored_check_start_time = time.time()
                                    restored_check_duration = 10
                                    # Получаем элемент снова для проверки
                                    video_element_for_check = self.wait.until(
                                        EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                                    previous_time_after_restore = self.driver.execute_script(
                                        "return arguments[0].currentTime;", video_element_for_check)

                                    restoration_successful = False
                                    while time.time() - restored_check_start_time < restored_check_duration:
                                        time.sleep(1)
                                        # Получаем элемент снова для проверки
                                        current_video_element_for_check = self.wait.until(
                                            EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                                        current_time_after_restore = self.driver.execute_script(
                                            "return arguments[0].currentTime;", current_video_element_for_check)

                                        if abs(current_time_after_restore - previous_time_after_restore) > 0.1:
                                            print("Воспроизведение успешно возобновлено через паузу/плей.")
                                            restoration_successful = True
                                            last_known_time = current_time_after_restore
                                            break
                                        previous_time_after_restore = current_time_after_restore

                                    if not restoration_successful:
                                        failed_recovery_attempts += 1
                                        print(
                                            f"ПРЕДУПРЕЖДЕНИЕ: Попытка восстановления #{failed_recovery_attempts} не удалась.")
                                        if failed_recovery_attempts >= max_failed_recovery_attempts:
                                            print(
                                                f"Исчерпан лимит попыток восстановления ({max_failed_recovery_attempts}).")
                                            print(
                                                f"Прерываю текущий фрагмент и возвращаюсь к выбору следующего.")
                                            break  # Выходим из цикла воспроизведения, переходя к следующей итерации while (перезапуск)

                                    # Сбрасываем счётчики и время остановки, если восстановление прошло успешно
                                    if restoration_successful:
                                        no_change_count = 0
                                        stop_start_time = None
                                        continue  # Переходим к следующей итерации основного цикла

                                    # Если восстановление не удалось, но количество неудач < max, продолжаем ждать
                                    # Счётчик no_change_count остаётся высоким, и мы снова попадём сюда в следующую итерацию

                            time.sleep(1)

                        except StaleElementReferenceException:
                            print("Обнаружена ошибка StaleElementReferenceException, возможно, DOM изменился.")
                            try:
                                # Попробуем заново найти видеоэлемент с ожиданием
                                current_video_element = self.wait.until(
                                    EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                                current_time = self.driver.execute_script("return arguments[0].currentTime;",
                                                                          current_video_element)
                                print(f"Текущее время после обновления элемента: {current_time:.2f}")
                                if abs(current_time - last_known_time) > 0.1:
                                    print("Видео продолжает воспроизводиться после обновления элемента")
                                    last_known_time = current_time
                                    no_change_count = 0
                                    stop_start_time = None
                                else:
                                    print("Видео не воспроизводится после обновления элемента")
                                    no_change_count += 1
                                    if stop_start_time is None:
                                        stop_start_time = time.time()
                            except Exception as e_scroll:
                                print(f"Ошибка при повторном поиске видеоэлемента: {e_scroll}")
                                # Попробуем восстановление или перезапуск
                                failed_recovery_attempts += 1
                                if failed_recovery_attempts >= max_failed_recovery_attempts:
                                    print(
                                        f"Ошибка StaleElementReference и неудачные восстановления. Прерываю текущий фрагмент.")
                                    break  # Выходим из цикла воспроизведения, переходя к следующей итерации while (перезапуск)
                            continue  # Продолжаем цикл, возможно с обновлённым элементом

                        except Exception as e:
                            print(f"Неожиданная ошибка при проверке воспроизведения: {e}")
                            break  # Выходим из цикла воспроизведения, переходя к следующей итерации while (перезапуск)

                    # Если цикл воспроизведения завершён, но success не True, значит, восстановление не помогло
                    if not success:
                        if restart_attempt <= max_restart_attempts:
                            print(
                                f"Воспроизведение фрагмента не удалось. Пытаюсь перезапустить... (осталось попыток: {max_restart_attempts - restart_attempt})")
                            # Цикл while продолжится, начнётся новая попытка (restart_attempt++)
                            # При этом снова будет клик по `day_element`, что и является "перезапуском" фрагмента в текущем контексте
                        else:
                            print(f"Исчерпан лимит попыток воспроизведения. Пропускаю день.")

                # После завершения попыток для текущего дня
                if not success:
                    print(
                        f"Фрагмент из дня {day_element.text} не был успешно воспроизведён за {max_restart_attempts} попыток.")
                else:
                    print(f"Фрагмент из дня {day_element.text} успешно воспроизведён.")

            # Основная логика метода
            # Собираем активные дни из текущего месяца
            day_elements = self.wait.until(EC.visibility_of_all_elements_located(self.DATE_CALENDAR_WITH_RECORDING))

            valid_days_current_month = []
            for day in day_elements:
                if "disabled" not in day.get_attribute("class") and day.text.strip().isdigit():
                    valid_days_current_month.append(day)

            print(f"Активные дни в текущем месяце: {[d.text for d in valid_days_current_month]}")

            # Проверяем, есть ли в текущем месяце хотя бы один день с записями
            if len(valid_days_current_month) > 0:
                # Выбираем случайные дни из текущего месяца (не более 4)
                days_to_check_current = min(4, len(valid_days_current_month))
                selected_days_current = random.sample(valid_days_current_month, days_to_check_current)

                print(f"Выбрано дней для проверки в текущем месяце: {len(selected_days_current)}")

                # Проверяем записи в выбранных днях текущего месяца
                for day in selected_days_current:
                    process_day(day, "текущем ")

            # Проверяем, нужно ли переходить к предыдущему месяцу
            # Если в текущем месяце не хватает 4 дней с записями, переходим к предыдущему
            if len(valid_days_current_month) < 4:
                print("Переходим к предыдущему месяцу для проверки дополнительных дней с записями...")

                # Клик на кнопку предыдущего месяца
                prev_month_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_HEADING_l))
                prev_month_button.click()
                time.sleep(5)

                # Клик на активное устройство для активации дней с записями
                try:
                    active_device = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_CAMERAS_INSIDE_LIST))
                    active_device.click()
                    print("Кликнули на активное устройство для активации дней в предыдущем месяце")
                    time.sleep(5)
                except Exception as device_click_error:
                    print(f"Не удалось кликнуть на активное устройство: {device_click_error}")

                # Собираем активные дни в предыдущем месяце после клика на устройство
                day_elements_prev = self.wait.until(
                    EC.visibility_of_all_elements_located(self.DATE_CALENDAR_WITH_RECORDING))

                valid_days_prev_month = []
                for day in day_elements_prev:
                    if "disabled" not in day.get_attribute("class") and day.text.strip().isdigit():
                        valid_days_prev_month.append(day)

                print(f"Активные дни в предыдущем месяце: {[d.text for d in valid_days_prev_month]}")

                # Проверяем, есть ли активные дни в предыдущем месяце
                if len(valid_days_prev_month) > 0:
                    # Выбираем случайный день из предыдущего месяца
                    random_day_prev = random.choice(valid_days_prev_month)
                    # Обрабатываем день в предыдущем месяце
                    process_day(random_day_prev, "предыдущем ")

                # Возвращаемся обратно к текущему месяцу
                next_month_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_HEADING_R_NEXT))
                next_month_button.click()
                time.sleep(2)
            else:
                print(
                    "В текущем месяце достаточно дней с записями (4 или более), переход к предыдущему месяцу не требуется")

            print("\n--- Завершено просмотра одного фрагмента из каждого дня с записью ---")


    # ПРОВЕРКА АВТОВОСПРОИЗВЕДЕНИЯ РАНДОМНО ТРЕХ ФРАГМЕНТОВ ЗАПИСИ
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

            # Начальная запись - рандомно выбираем
            start_record = random.choice(records)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", start_record)
            start_record.click()
            time.sleep(3)  # Подождем немного, чтобы клик сработал

            # Ждём, пока появится информация о текущем видео
            print("Ожидаем загрузку информации о первом видео...")

            # Ожидаем, что все поля будут заполнены (не пустые и не "неизвестно")
            max_wait_time = 30
            start_wait_time = time.time()

            initial_camera = None
            initial_date = None
            initial_time = None
            initial_duration = None

            while time.time() - start_wait_time < max_wait_time:
                try:
                    # Получаем значения из полей
                    camera_elem = self.wait.until(EC.presence_of_element_located(self.NAME_CAMERAS_RECORDING_FRAGMENT_VIDEO))
                    date_elem = self.wait.until(EC.presence_of_element_located(self.DATE_RECORDING_FRAGMENT_VIDEO))
                    time_elem = self.wait.until(EC.presence_of_element_located(self.TIME_RECORDING_FRAGMENT_VIDEO))
                    duration_elem = self.wait.until(EC.presence_of_element_located(self.DURATION_RECORDING_FRAGMENT_VIDEO))

                    initial_camera = camera_elem.text or camera_elem.get_attribute("value") or "неизвестно"
                    initial_date = date_elem.text or date_elem.get_attribute("value") or "неизвестно"
                    initial_time = time_elem.text or time_elem.get_attribute("value") or "неизвестно"
                    initial_duration = duration_elem.text or duration_elem.get_attribute("value") or "неизвестно"

                    # Проверяем, что все поля заполнены (не "неизвестно" и не пустые)
                    if (initial_camera != "неизвестно" and initial_camera.strip() and
                            initial_date != "неизвестно" and initial_date.strip() and
                            initial_time != "неизвестно" and initial_time.strip() and
                            initial_duration != "неизвестно" and initial_duration.strip()):

                        print(
                            f"Исходное видео: камера='{initial_camera}', дата='{initial_date}', время='{initial_time}', длительность='{initial_duration}'")
                        break
                    else:
                        print(
                            f"Поля еще не заполнены, ждем... Текущие значения: камера='{initial_camera}', дата='{initial_date}', время='{initial_time}', длительность='{initial_duration}'")
                        time.sleep(1)
                        continue

                except Exception as e:
                    print(f"Ошибка при получении информации о видео: {e}")
                    time.sleep(1)
                    continue

            # Проверяем, что все поля заполнены
            assert initial_camera and initial_camera != "неизвестно", "Название камеры не найдено."
            assert initial_date and initial_date != "неизвестно", "Дата не найдена."
            assert initial_time and initial_time != "неизвестно", "Время не найдено."
            assert initial_duration and initial_duration != "неизвестно", "Длительность не найдена."

            # Ожидаем видеоэлемент для начальной записи
            try:
                video_element = self.wait.until(EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                print("Видео найдено и готово к воспроизведению.")

                # Проверка, что видео действительно загружено
                assert video_element, "Видеоэлемент не найден."

                # Ждём, пока появится длительность
                duration = None
                for _ in range(60):
                    try:
                        duration = self.driver.execute_script("return arguments[0].duration;", video_element)
                        if duration and duration > 0:
                            print(f"Длительность видео: {duration:.2f} секунд")
                            break
                    except Exception as e:
                        print(f"Ошибка получения длительности: {e}")
                    time.sleep(1)

                if not duration or duration <= 0:
                    print("Не удалось определить длительность видео, используем ожидание по таймеру")
                    time.sleep(10)
                else:
                    # Ждём окончания воспроизведения первого видео
                    start_time = time.time()
                    print(
                        f"Начинаем ожидание завершения первого видео длительностью {duration:.2f} секунд ({duration / 60:.2f} минут)")
                    while True:
                        try:
                            current_time_pos = self.driver.execute_script("return arguments[0].currentTime;", video_element)
                            if current_time_pos >= duration - 1:  # погрешность
                                print("Первое видео полностью воспроизведено.")
                                break
                        except Exception as e:
                            print(f"Ошибка получения текущего времени: {e}")
                        time.sleep(1)

                        # Защищаем от бесконечного цикла
                        if time.time() - start_time > duration + 300:
                            print("Превышено время ожидания завершения видео")
                            break

                    end_time = time.time()
                    watch_time = end_time - start_time
                    print(f"Время просмотра первого видео: {watch_time:.2f} секунд ({watch_time / 60:.2f} минут)")

            except TimeoutException:
                print("Видео не загрузилось, пропускаем...")
                assert False, "Видео не загрузилось, невозможно проверить автовоспроизведение."

            # Ждём 3 фрагмента, включая первый
            watched_count = 1  # Уже посмотрели первый фрагмент
            print(f"Начинаем отслеживание автовоспроизведения. Просмотрено: {watched_count}/3 фрагментов")

            # Ждём и отслеживаем следующие 2 фрагмента
            while watched_count < 3:
                print(f"Ожидаем следующий фрагмент... Просмотрено: {watched_count}/3")

                # Запоминаем текущее состояние
                current_camera = self.wait.until(EC.presence_of_element_located(self.NAME_CAMERAS_RECORDING_FRAGMENT_VIDEO)).text
                current_date = self.wait.until(EC.presence_of_element_located(self.DATE_RECORDING_FRAGMENT_VIDEO)).text
                current_time = self.wait.until(EC.presence_of_element_located(self.TIME_RECORDING_FRAGMENT_VIDEO)).text

                print(f"Текущее состояние: камера='{current_camera}', дата='{current_date}', время='{current_time}'")

                # Ждем изменения состояния (нового фрагмента)
                max_wait_time = 1800
                start_wait_time = time.time()

                new_fragment_found = False

                while time.time() - start_wait_time < max_wait_time and not new_fragment_found:
                    time.sleep(2)

                    try:
                        # Ждем, пока поля будут заполнены для нового фрагмента
                        new_camera_elem = self.wait.until(EC.presence_of_element_located(self.NAME_CAMERAS_RECORDING_FRAGMENT_VIDEO))
                        new_date_elem = self.wait.until(EC.presence_of_element_located(self.DATE_RECORDING_FRAGMENT_VIDEO))
                        new_time_elem = self.wait.until(EC.presence_of_element_located(self.TIME_RECORDING_FRAGMENT_VIDEO))
                        new_duration_elem = self.wait.until(EC.presence_of_element_located(self.DURATION_RECORDING_FRAGMENT_VIDEO))

                        new_camera = new_camera_elem.text or new_camera_elem.get_attribute("value") or "неизвестно"
                        new_date = new_date_elem.text or new_date_elem.get_attribute("value") or "неизвестно"
                        new_time = new_time_elem.text or new_time_elem.get_attribute("value") or "неизвестно"
                        new_duration = new_duration_elem.text or new_duration_elem.get_attribute(
                            "value") or "неизвестно"

                        # Если хотя бы одно поле изменилось - это новый фрагмент
                        if ((new_camera != current_camera or
                             new_date != current_date or
                             new_time != current_time) and
                                # Проверяем, что новые значения не "неизвестно" и не пустые
                                new_camera != "неизвестно" and new_camera.strip() and
                                new_date != "неизвестно" and new_date.strip() and
                                new_time != "неизвестно" and new_time.strip() and
                                new_duration != "неизвестно" and new_duration.strip()):

                            print(
                                f"Обнаружена новая запись: дата='{new_date}', время='{new_time}', камера='{new_camera}'")

                            # Проверка, что поля не пусты
                            assert new_camera and new_camera != "неизвестно", "Название камеры не найдено."
                            assert new_date and new_date != "неизвестно", "Дата не найдена."
                            assert new_time and new_time != "неизвестно", "Время не найдено."
                            assert new_duration and new_duration != "неизвестно", "Длительность не найдена."

                            print("=" * 50)
                            print(f"Камера: {new_camera}")
                            print(f"Дата (из поля): {new_date}")
                            print(f"Время (из поля): {new_time}")
                            print(f"Длительность (из поля): {new_duration}")
                            print("=" * 50)

                            new_fragment_found = True

                            # Ожидаем видеоэлемент для нового фрагмента
                            try:
                                video_element = self.wait.until(EC.presence_of_element_located(self.PLAY_VIDEO_WINDOW))
                                print("Видео найдено и готово к воспроизведению.")

                                # Ждём, пока появится длительность
                                duration = None
                                for _ in range(60):
                                    try:
                                        duration = self.driver.execute_script("return arguments[0].duration;", video_element)
                                        if duration and duration > 0:
                                            print(
                                                f"Длительность видео: {duration:.2f} секунд ({duration / 60:.2f} минут)")
                                            break
                                    except Exception as e:
                                        print(f"Ошибка получения длительности: {e}")
                                    time.sleep(1)

                                if not duration or duration <= 0:
                                    print("Не удалось определить длительность видео, используем ожидание по таймеру")
                                    time.sleep(900)
                                else:
                                    # Ждём окончания воспроизведения
                                    start_time = time.time()
                                    print(
                                        f"Начинаем ожидание завершения видео длительностью {duration:.2f} секунд ({duration / 60:.2f} минут)")
                                    while True:
                                        try:
                                            current_time_pos = self.driver.execute_script("return arguments[0].currentTime;", video_element)
                                            if current_time_pos >= duration - 1:  # погрешность
                                                print("Видео полностью воспроизведено.")
                                                break
                                        except Exception as e:
                                            print(f"Ошибка получения текущего времени: {e}")
                                        time.sleep(1)

                                        # Защищаем от бесконечного цикла
                                        if time.time() - start_time > duration + 900:
                                            print("Превышено время ожидания завершения видео")
                                            break

                                    end_time = time.time()
                                    watch_time = end_time - start_time
                                    print(f"Время просмотра: {watch_time:.2f} секунд ({watch_time / 60:.2f} минут)")

                            except TimeoutException:
                                print("Видео не загрузилось, пропускаем...")
                                assert False, "Видео не загрузилось, невозможно проверить автовоспроизведение."

                            watched_count += 1
                            print(f"Просмотрено: {watched_count}/3 фрагментов")

                            if watched_count >= 3:
                                print("Просмотр остановлен после 3 фрагментов.")
                                break

                            # Обновляем текущее состояние для следующей итерации
                            current_camera = new_camera
                            current_date = new_date
                            current_time = new_time

                    except Exception as e:
                        print(f"Ошибка при проверке изменения фрагмента: {e}")
                        time.sleep(2)
                        continue

                if not new_fragment_found:
                    print("Превышено время ожидания следующего фрагмента")
                    break

        finally:
            self.driver.quit()
