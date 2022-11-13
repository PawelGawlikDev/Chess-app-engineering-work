import time
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from chessapp.models import Partie
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

USERNAME = "admin"
PASSWORD = "admin"
NAZWA = "Patria Testowa"
PGN = "1. e4 e5 2. Nf3 Nc6 3. Bc4 Nf6 4. Ng5 Bc5"
FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class ChessAppTests(StaticLiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.admin = User.objects.create_superuser(username=USERNAME,
                                                   email=None,
                                                   password=PASSWORD)
        self.games = Partie.objects.create(nazwa=NAZWA, PGN=PGN)

    def tearDown(self):
        self.driver.close()

    def testMainPage(self):
        self.driver.get(self.live_server_url)
        header = self.driver.find_element(By.ID, "header").text
        self.assertEqual("Home", header, msg="Header don't exist")
        loginLink = self.driver.find_element(By.ID, "login-butt").text
        self.assertEqual("Log In", loginLink, msg="Log in button don't exist")
        signUpLink = self.driver.find_element(By.ID, "singUp-butt").text
        self.assertEqual("Sign up", signUpLink, msg="Sing up button don't exits")

    def testLoginPageLink(self):
        driver = self.driver
        driver.get(self.live_server_url)
        loginButton = driver.find_element(By.ID, "login-butt")
        loginButton.click()
        currentURL = driver.current_url
        self.assertEqual(currentURL, self.live_server_url + "/accounts/login/", msg="Login link don't work")

    def testSignInPageLink(self):
        self.driver.get(self.live_server_url)
        signInbutton = self.driver.find_element(By.ID, "singUp-butt")
        signInbutton.click()
        currentURL = self.driver.current_url
        self.assertEqual(currentURL, self.live_server_url + "/accounts/signup/", msg="Sign up link don't work")

    def testLogInToGoodAccount(self):
        driver = self.driver
        self.testLoginPageLink()
        username = driver.find_element(By.ID, "id_username")
        username.send_keys('admin')
        password = driver.find_element(By.ID, 'id_password')
        password.send_keys('admin')
        LogInButton = driver.find_element(By.ID, 'log-in-button')
        LogInButton.click()
        time.sleep(5)
        header = driver.find_element(By.ID, "welcome-text").text
        self.assertEqual(header, "Hi admin!", msg="Header don't show up")


if __name__ == '__main__':
    StaticLiveServerTestCase.main()
