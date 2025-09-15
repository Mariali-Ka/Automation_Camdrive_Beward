import pytest
from config.login import Login
from pages.authorization_page import AuthorizationPersonalAccount
from pages.online_tab import OnlineTab






class BaseTest:

    login: Login

    authorization_page: AuthorizationPersonalAccount
    online_tab: OnlineTab
    # online_tab: Turningcameras



    # создаем фикстуру

    @pytest.fixture(autouse=True)
    def setup(self, request, driver):
        request.cls.driver = driver
        request.cls.login = Login()

        request.cls.authorization_page = AuthorizationPersonalAccount(driver)
        request.cls.online_tab = OnlineTab(driver)
        # request.cls.online_tab = Turningcameras(driver)
