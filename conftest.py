import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function", autouse=True) # будет создавать экземпляр драйвера для каждого теста отдельно и автоматически будет использоваться для каждого теста
def driver(request):
    options = Options()
    # options.add_argument("--headless") # нужен безголовый режим, если запускать тесты в сиа, докере и т.д. Его закомментировать, т.к. пока запускать будем локально
    options.add_argument("--no-sandbox") # это обязательно, подтверждаем, что это не песочница, это реальный проект
    options.add_argument("--disable-dev-shm-usage") # позволяет запускаться браузеру внутри сред, где нет интерфейса (это про все эти опции - набор 4)
    options.add_argument("--window-size=1920,1080") # определенный размер окна
    driver = webdriver.Chrome(options=options) # инициализация драйвера
    request.cls.driver = driver # данная конструкция создает объект драйвера внутри тестовых классов
    yield driver # возвращаем драйвер
    driver.quit() # закрываем наш браузер