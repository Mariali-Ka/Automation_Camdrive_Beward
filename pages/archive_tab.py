import re
import time
import random
import calendar
from datetime import datetime
import allure
from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



class ArchiveTab(BasePage):

    PAGE_URL = Links.ARCHIVE_TAB

    TAB_ARCHIVE = ("xpath", "//a[text()='Архив']")
    FIELD_CALENDAR = ("xpath", "//div[text()='Календарь']")
    OPENING_CALENDAR = ("xpath", "//img[@alt='Выберите дату']")
    OPENING_CALENDAR_MONTH_AGO =("xpath", "//a[@title='<Пред']")
    SELECT_DAY_OPENING_CALENDAR = ("xpath", "//td[@data-handler='selectDay']")
    FIELD_INPUT_DATE = ("xpath", "//input[@id='download-date']")
    HEADING_C = ("xpath", "//th[@class='heading-c']")
    HEADING_l = ("xpath", "//th[@class='heading-l prev']")
    HEADING_R = ("xpath", "//th[@class='heading-r off']")
    HEADING_R_NEXT = ("xpath", "//th[@class='heading-r next']")
    ALL_CELLS_WITH_DAYS_CALENDAR = ("xpath", "//div[@class='item day']")  # все ячейки с днями в календаре
    ALL_CELLS_WITH_VIEWING_RECORDS = ("xpath", "//div[@class='time item  constant']")  # все ячейки с днями в календаре

    @allure.step("Go to archive tab")
    def click_go_to_archive_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.TAB_ARCHIVE)).click()

    @allure.step("Is Opened Archive Tab")
    def is_opened_archive_tab(self):
        current_url = self.PAGE_URL
        assert current_url == Links.ARCHIVE_TAB, "Ошибка в URL, открыта не та страница"

    @allure.step("Go to one month ago calendar")
    def click_go_to_one_month_ago_calendar(self):
        month_header = self.wait.until(EC.presence_of_element_located(self.HEADING_C))
        current_month_text = month_header.text.strip()
        print(f"Исходный месяц: {current_month_text}")
        self.wait.until(EC.element_to_be_clickable(self.HEADING_l)).click()
        self.wait.until(lambda driver: self.wait.until(EC.presence_of_element_located(self.HEADING_C)).text.strip() != current_month_text)
        new_month_header = self.wait.until(EC.presence_of_element_located(self.HEADING_C))
        new_month_text = new_month_header.text.strip()
        print(f"Новый месяц после нажатия: {new_month_text}")
        assert new_month_text != current_month_text, "Месяц не изменился после нажатия кнопки"

    @allure.step("Go to one month advance calendar")
    def click_go_to_one_month_advance_calendar(self):
        self.wait.until(EC.element_to_be_clickable(self.HEADING_R_NEXT)).click()

    @allure.step("Checking opening calendar")
    def click_checking_opening_calendar(self):
        self.wait.until(EC.element_to_be_clickable(self.OPENING_CALENDAR)).click()
        assert self.wait.until(EC.visibility_of_element_located(self.OPENING_CALENDAR)).is_displayed()

    allure.step("Selected date displayed field")
    def selected_date_displayed_field(self):
        self.wait.until(EC.element_to_be_clickable(self.OPENING_CALENDAR_MONTH_AGO)).click()
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

    allure.step("Viewing from camera")
    def viewing_from_camera(self):
        day_elements = self.wait.until(EC.visibility_of_all_elements_located(self.ALL_CELLS_WITH_DAYS_CALENDAR))

        # Фильтруем только активные/валидные дни
        valid_days = []
        for day in day_elements:
            # Пример: проверка, что день не отключён
            if "disabled" not in day.get_attribute("class") and day.text.strip().isdigit():
                valid_days.append(day)
        print("Валидные дни:", [d.text for d in valid_days])

        random_valid_days = random.choice(day_elements)
        random_valid_days.click()

        try:

            records = self.wait.until(EC.visibility_of_all_elements_located(self.ALL_CELLS_WITH_VIEWING_RECORDS))

            if not records:
                print("Записи не найдены!")
            else:
                print(f"Найдено записей: {len(records)}")

                # Выбираем случайную запись
                random_record = random.choice(records)

                # Прокручиваем к элементу (на случай, если он вне экрана)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", random_record)
                random_record.click()
                time.sleep(5)
                print("Перешли к просмотру записи.")

        finally:
            pass




