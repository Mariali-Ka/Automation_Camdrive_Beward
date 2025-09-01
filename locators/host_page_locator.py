

class ExitPersonalAccountLocator:
    # форма полей
    LOGIN_FIELD = ("xpath", "//input[@class='input']")  # поле для ввода login
    PASSWORD_FIELD = ("xpath", "//input[@class='input password']")  # поле для ввода password
    ENTER_BUTTON = ("xpath", "//*[@id='login']")  # кнопка Войти
    EYE_BUTTON = ("xpath", "//div[@title='Показать пароль']")  # кнопка глаз
    CHECKBOX_REMEMBER_ME = ("xpath", "//input[@type='checkbox']")  # чек-бокс Запомнить меня