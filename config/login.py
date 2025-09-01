import random
import time
import allure
import os
from dotenv import load_dotenv


load_dotenv()


class Login:

    LOGIN = os.getenv("LOGIN")
    PASSWORD = os.getenv("PASSWORD")