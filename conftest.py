import pytest
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function", autouse=True) # будет создавать экземпляр драйвера для каждого теста отдельно и автоматически будет использоваться для каждого теста
def driver(request):
    options = Options()

    user_data_dir = tempfile.mkdtemp(prefix="chrome_test_profile_")

    options.add_argument(f"--user-data-dir={user_data_dir}")

    options.add_argument("--no-sandbox") # это обязательно, подтверждаем, что это не песочница, это реальный проект
    options.add_argument("--disable-dev-shm-usage") # позволяет запускаться браузеру внутри сред, где нет интерфейса (это про все эти опции - набор 4)
    options.add_argument("--window-size=1920,1080") # определенный размер окна
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--password-store=basic")
    options.add_argument(
        "--disable-features="
        "PasswordLeakDetection,"  # Главный выключатель проверки утечек
        "PasswordCheck,"  # Блокирует фоновый модуль сверки данных
        "PasswordGeneration,"  # Отключает генератор паролей
        "SafeBrowsingPasswordCheck,"  # Отключает облачную проверку через SafeBrowsing
        "BiometricAuthenticationForPasswordParsing"
    )

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    chrome_prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_settings.popups": 0,  # на всякий случай
        "safebrowsing.enabled": False,
        "safebrowsing.passwords_enabled": False,
        "profile.password_leak_detection": False,
        "profile.password_check_identity_not_confirmed": False,
        "password_manager.leak_detection_enabled": False,  # Новый ключ для свежих версий Chrom
        "autofill.profile_enabled": False,  # Отключает автозаполнение профилей в целом
        "autofill.credit_card_enabled": False  # Отключает автозаполнение карт для чистоты тестов
    }
    options.add_experimental_option("prefs", chrome_prefs)

    driver = webdriver.Chrome(options=options)  # инициализация драйвера
    # Проверяем, запущен ли тест внутри класса, чтобы избежать ошибки AttributeError
    if request.cls is not None:
        request.cls.driver = driver
    # request.cls.driver = driver # данная конструкция создает объект драйвера внутри тестовых классов
    yield driver # возвращаем драйвер
    driver.quit() # закрываем наш браузер

    shutil.rmtree(user_data_dir, ignore_errors=True)