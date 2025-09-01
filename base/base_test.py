import pytest
from config.login import Login
from pages.host_page import ExitPersonalAccount
from pages.online_tab import ClickButtonExit





class BaseTest:

    login: Login

    host_page: ExitPersonalAccount
    online_tab: ClickButtonExit


    # создаем фикстуру

    @pytest.fixture(autouse=True)
    def setup(self, request, driver):
        request.cls.driver = driver
        request.cls.login = Login()

        request.cls.host_page = ExitPersonalAccount(driver)
        request.cls.online_tab = ClickButtonExit(driver)