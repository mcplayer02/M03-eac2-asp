from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
 
class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    #fixtures = ['testdb.json',]
 
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
	# creem superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()
 
    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        cls.selenium.quit()
        super().tearDownClass()
 
    def test_login(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
 
        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )
 
        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()
 
        #Creació d'usuari
        continue_link = self.selenium.find_element(By.LINK_TEXT, 'Users')
        continue_link.click()
        continue_link = self.selenium.find_element(By.LINK_TEXT, 'ADD USER')
        continue_link.click()
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element(By.NAME,"password1")
        password_input.send_keys('pirineus')
        password_input = self.selenium.find_element(By.NAME,"password2")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.NAME, '_continue').click()
        self.selenium.find_element(By.NAME, 'is_staff').click()
        self.selenium.find_element(By.NAME, '_save').click()
        self.selenium.find_element(By.ID, 'logout-form').click()
        self.selenium.find_element(By.LINK_TEXT, 'Log in again').click()
 
        #Inici de sessió previament creat i canvi de contrasenya
        self.selenium.find_element(By.NAME,"username").send_keys('admin')
        self.selenium.find_element(By.NAME,"password").send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()
        self.selenium.find_element(By.LINK_TEXT,'CHANGE PASSWORD').click()

        self.selenium.find_element(By.NAME,"old_password").send_keys('pirineus')
        self.selenium.find_element(By.NAME,"new_password1").send_keys('isardvdi')
        self.selenium.find_element(By.NAME,"new_password2").send_keys('isardvdi')
        self.selenium.find_element(By.XPATH, "//input[@type='submit' and @value='Change my password']").click()
