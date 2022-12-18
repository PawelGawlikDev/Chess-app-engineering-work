import time
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from chessapp.models import Partie
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class ChessAppTests(StaticLiveServerTestCase):

    def setUp(self):
        USERNAME = "admin"
        PASSWORD = "admin"
        NAZWA = "Patria Testowa"
        NAZWA2 = "Partia Testowa 2"
        PGN = "1. e4 e5 2. Nf3 Nc6 3. Bc4 Nf6 4. Ng5 Bc5"
        FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.admin = User.objects.create_superuser(username=USERNAME,
                                                   email=None,
                                                   password=PASSWORD)
        self.game1 = Partie.objects.create(user=self.admin, nazwa=NAZWA, PGN=PGN, FEN=FEN)
        self.game2 = Partie.objects.create(user=self.admin, nazwa=NAZWA2, PGN=PGN, FEN=FEN)

    def tearDown(self):
        self.driver.close()

    def _IsBoardVisible(self, name='board', type=By.ID):
        """Helper to checked is board display"""
        driver = self.driver
        board = driver.find_element(type, name)
        self.assertTrue(board.is_displayed(), msg="Board don't display")

    def _LoginPageLink(self):
        """Log in helper"""
        driver = self.driver
        driver.get(self.live_server_url)
        loginButton = driver.find_element(By.ID, "login-butt")
        loginButton.click()
        currentURL = driver.current_url
        self.assertEqual(currentURL, self.live_server_url + "/accounts/login/", msg="Login link don't work")

    def _FillLoginForm(self, username, password):
        """Complete the login form"""
        driver = self.driver
        usernameField = driver.find_element(By.ID, "id_username")
        usernameField.send_keys(username)
        passwordField = driver.find_element(By.ID, 'id_password')
        passwordField.send_keys(password)

    def _SingUpPageLink(self):
        """Sign UP helper"""
        driver = self.driver
        driver.get(self.live_server_url)
        singupButton = driver.find_element(By.ID, "singup-butt")
        singupButton.click()
        currentURL = driver.current_url
        self.assertEqual(currentURL, self.live_server_url + "/accounts/signup/", msg="Sign Up link don't work")

    def _FillSingUpForm(self, username, password):
        """Complete the sing up form"""
        driver = self.driver
        usernameFile = driver.find_element(By.ID, "id_username")
        usernameFile.send_keys(username)
        password1 = driver.find_element(By.ID, 'id_password1')
        password1.send_keys(password)
        password2 = driver.find_element(By.ID, 'id_password2')
        password2.send_keys(password)

    def _EditBoard(self):
        """Go to Edit Board helper"""
        driver = self.driver
        self.testLogIn()
        EditBoardButt = driver.find_element(By.ID, "edti-butt")
        EditBoardButt.click()
        currentURL = driver.current_url
        self.assertEqual(currentURL, self.live_server_url + "/edit/",
                         msg="Edit Board page don't load")

    def _SetUpPositionOnBoard(self):
        """Set up position on Edit Board page"""
        driver = self.driver
        e2Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-e2']")
        e4Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-e4']")
        e7Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-e7']")
        e5Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-e5']")
        g1Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-g1']")
        f3Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-f3']")
        b8Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-b8']")
        c6Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-c6']")
        action = ActionChains(driver)
        action.drag_and_drop(e2Square, e4Square).drag_and_drop(g1Square, f3Square).drag_and_drop(e7Square, e5Square). \
            drag_and_drop(b8Square, c6Square).perform()

    def _MakeLegalMove(self):
        """Make legal move"""
        driver = self.driver
        e2Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-e2']")
        e4Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-e4']")
        e7Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-e7']")
        e5Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-e5']")
        g1Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-g1']")
        f3Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-f3']")
        b8Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-b8']")
        c6Square = driver.find_element(By.CSS_SELECTOR, "div[class$=' square-c6']")
        action = ActionChains(driver)
        action.drag_and_drop(e2Square, e4Square).drag_and_drop(e7Square, e5Square).drag_and_drop(g1Square, f3Square) \
            .drag_and_drop(b8Square, c6Square).perform()

    def _IsMoveListVisible(self, name, type=By.CLASS_NAME):
        driver = self.driver
        moveList = driver.find_element(type, name)
        self.assertTrue(moveList.is_displayed(), msg="Move list don't display")

    def _MoveListContent(self, name, moves, type=By.ID):
        driver = self.driver
        moveList = driver.find_element(type, name)
        self.assertEqual(moves, moveList.text, msg="Move lists is have wrong content")

    def testLogIn(self):
        """PU-P2: Logowanie do konta"""
        username = 'admin'
        password = 'admin'
        driver = self.driver
        self._LoginPageLink()
        self._FillLoginForm(username, password)
        LogInButton = driver.find_element(By.ID, 'log-in-button')
        LogInButton.click()
        time.sleep(3)
        header = driver.find_element(By.ID, "welcome-text").text
        self.assertEqual(header, "HI ADMIN!", msg="Header don't show up")

    def testSingUp(self):
        """PU-P1: Zakładanie konta"""
        username = 'test'
        password = 'test12345'
        driver = self.driver
        self._SingUpPageLink()
        self._FillSingUpForm(username, password)
        SingupButton = driver.find_element(By.ID, 'sign-up-button')
        SingupButton.click()
        time.sleep(3)
        currentURL = driver.current_url
        self.assertEqual(currentURL, self.live_server_url + "/accounts/login/",
                         msg="After Sucess singup user should go to login page")
        self._FillLoginForm(username, password)
        LogInButton = driver.find_element(By.ID, 'log-in-button')
        LogInButton.click()
        time.sleep(3)
        header = driver.find_element(By.ID, "welcome-text").text
        self.assertEqual(header, "HI TEST!", msg="Header don't show up")

    def testEditBoard(self):
        """PU-P3: Edytowanie pozycji"""
        self._EditBoard()
        time.sleep(3)
        self._SetUpPositionOnBoard()
        time.sleep(3)

    def testPlayEditPossAgainstPCasWhite(self):
        """PU-P4: Gra wcześniej stawionej pozycji z komputerem"""
        driver = self.driver
        self._EditBoard()
        time.sleep(3)
        self._SetUpPositionOnBoard()
        time.sleep(3)
        playAsWhiteButt = driver.find_element(By.ID, 'aswhite')
        playAsWhiteButt.click()
        time.sleep(3)
        currentURL = driver.current_url
        self.assertEqual(currentURL, self.live_server_url + "/edit/#")

    def testPlayEditPossAgainstPCasBlack(self):
        """PU-P4: Gra wcześniej stawionej pozycji z komputerem"""
        driver = self.driver
        self._EditBoard()
        time.sleep(3)
        self._SetUpPositionOnBoard()
        time.sleep(3)
        turnButt = driver.find_element(By.ID, 'flipturn')
        turnButt.click()
        playAsBlackButt = driver.find_element(By.ID, 'asblack')
        playAsBlackButt.click()
        time.sleep(3)
        currentURL = driver.current_url
        self.assertEqual(currentURL, self.live_server_url + "/edit/#")

    def testShowUserGames(self):
        """PU-P5: Przeglądanie wszystkich partii przypisanych do użytkownika"""
        driver = self.driver
        self.testLogIn()
        gamesButt = driver.find_element(By.ID, 'games-butt')
        gamesButt.click()
        game = driver.find_elements(By.CLASS_NAME, 'game-link')
        gamesCount = len(game)
        self.assertEqual(gamesCount, 2, msg="Games don't display")

    def testShowGame(self):
        """PU-P6: Przeglądanie konkretnej partii przypisanej do użytkownika"""
        driver = self.driver
        self.testShowUserGames()
        game = driver.find_element(By.CSS_SELECTOR, '#games-list > a:nth-child(2)')
        game.click()
        self._IsBoardVisible(name='board')
        self._IsMoveListVisible(name='gameMoves')

    def testAnalizeOnEditBoardPage(self):
        """PU-P7: Analiza konkretnej pozycji ustawionej przez
         użytkownika na stronie do edytowania szachownicy"""
        driver = self.driver
        self._EditBoard()
        self._SetUpPositionOnBoard()
        time.sleep(2)
        analizeButt = driver.find_element(By.ID, 'start')
        stats = driver.find_element(By.ID, 'stats')
        self.assertEqual(stats.text, "", msg="Stats text should be empty")
        analizeButt.click()
        time.sleep(4)
        self.assertNotEqual(stats.text, "", msg="Stats text shouldn't be empty")

    def testAddMoveToGame(self):
        """PU-P8: Dodanie ruchów do partii"""
        driver = self.driver
        self._EditBoard()
        time.sleep(1)
        gameButt = driver.find_element(By.ID, 'game')
        gameButt.click()
        time.sleep(1)
        self._MakeLegalMove()
        example = '1. e4 e5 2. Nf3 Nc6'
        time.sleep(1)
        self._MoveListContent('pgn', example)

    def testAddCustomGameToDB(self):
        """PU-P9: Zapisanie partii do bazy danych"""
        driver = self.driver
        self._EditBoard()
        time.sleep(1)
        gameButt = driver.find_element(By.ID, 'game')
        gameButt.click()
        time.sleep(1)
        self._MakeLegalMove()
        example = '1. e4 e5 2. Nf3 Nc6'
        time.sleep(1)
        self._MoveListContent('pgn', example)
        copyButt = driver.find_element(By.ID, 'copy-butt')
        copyButt.click()
        time.sleep(2)
        inputName = driver.find_element(By.ID, 'id_nazwa')
        inputName.send_keys("Test")
        time.sleep(2)
        saveButt = driver.find_element(By.CSS_SELECTOR, "#container > form > fieldset > button")
        saveButt.click()
        time.sleep(2)
        currentURL = driver.current_url
        self.assertEqual(currentURL, self.live_server_url + "/partie/", msg="Games page don't load")
        games = driver.find_elements(By.CLASS_NAME, 'game-link')
        gamesCount = len(games)
        self.assertEqual(gamesCount, 3, msg="New game isn't add to list")

    def testFlipBoard(self):
        """PU-P10: Użytkownik chce obrócić szachownicę"""
        driver = self.driver
        self._EditBoard()
        self._IsBoardVisible()
        turnButt = driver.find_element(By.ID, 'flippos')
        turnButt.click()

    def testTurnBoard(self):
        """PU-P11: Użytkownik chce ustawić który kolor się rusza. """
        driver = self.driver
        startFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self._EditBoard()
        self._IsBoardVisible()
        fen = driver.find_element(By.ID, 'fen')
        self.assertEqual(fen.get_attribute('value'), startFEN, msg="Start FEN is wrong")
        turnButt = driver.find_element(By.ID, 'flipturn')
        turnButt.click()
        fen = driver.find_element(By.ID, 'fen')
        newFEN = fen.get_attribute('value')
        self.assertEqual(newFEN, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1', msg="Turn should change")

    def testClearBoard(self):
        """PU-P12: Użytkownik chce wyczyścić szachownicę"""
        driver = self.driver
        self._EditBoard()
        self._IsBoardVisible()
        clearButt = driver.find_element(By.ID, 'clearpos')
        clearButt.click()
        fen = driver.find_element(By.ID, 'fen')
        clearFEN = fen.get_attribute('value')
        self.assertEqual(clearFEN, "4k3/8/8/8/8/8/8/4K3 w - - 0 1", msg="Board isn't clear")

    def testResetPoss(self):
        """PU-P13: Użytkownik chce zresetować pozycję do początkowej"""
        driver = self.driver
        self._EditBoard()
        self._IsBoardVisible()
        clearButt = driver.find_element(By.ID, 'clearpos')
        resetButt = driver.find_element(By.ID, 'startpos')
        clearButt.click()
        time.sleep(2)
        fen = driver.find_element(By.ID, 'fen')
        self.assertEqual(fen.get_attribute('value'), "4k3/8/8/8/8/8/8/4K3 w - - 0 1", msg="Board isn't clear")
        resetButt.click()
        time.sleep(2)
        fen = driver.find_element(By.ID, 'fen')
        self.assertEqual(fen.get_attribute('value'), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                         msg="Baord should have start poss")

    def testAnalizeOnGamePage(self):
        """PU-P14: Użytkownik chce włączyć analizę silnikową pozycji na stronie do dodawania ruchów"""
        driver = self.driver
        self._EditBoard()
        self._SetUpPositionOnBoard()
        time.sleep(2)
        gameButt = driver.find_element(By.ID, 'game')
        gameButt.click()
        analizeButt = driver.find_element(By.ID, 'start')
        stats = driver.find_element(By.ID, 'stats')
        self.assertEqual(stats.text, "", msg="Stats text should be empty")
        analizeButt.click()
        time.sleep(4)
        self.assertNotEqual(stats.text, "", msg="Stats text shouldn't be empty")


if __name__ == '__main__':
    StaticLiveServerTestCase.main()
