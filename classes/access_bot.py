import time

from decouple import config
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class Bot:

    def __init__(self):
        self.__email = self.__retorna_var_embiente('EMAIL')
        self.__link = self.__retorna_var_embiente('AMAZON_LINK')
        self.__password = self.__retorna_var_embiente('PASSWORD')
        self.__driver = self.__define_driver()

    def __retorna_var_embiente(self, var):
        return config(var)

    def __define_driver(self):
        return Chrome(ChromeDriverManager().install(), chrome_options=self.__configura_navegacao())

    def __configura_navegacao(self):
        configuracoes = ChromeOptions()
        configuracoes.add_argument('--incognito')
        configuracoes.add_argument('--headless')
        return configuracoes

    def __abre_web_page(self):
        print('\n>> Acessando página web...')
        self.__driver.get(self.__link)

    def __entra_email(self):
        email_input = self.__driver.find_element_by_xpath('//input[contains(@name, "email")]')
        email_input.click()
        email_input.send_keys(self.__email)
        email_input.send_keys(Keys.ENTER)

    def __entra_senha(self):
        senha_input = self.__driver.find_element_by_xpath('//input[contains(@name, "password")]')
        senha_input.click()
        senha_input.send_keys(self.__password)
        senha_input.send_keys(Keys.ENTER)

    def __fazer_login(self):
        print('\n>> Realizando login...')
        self.__entra_email()
        time.sleep(3)
        self.__entra_senha()

    def __executar(self):
        self.__abre_web_page()
        time.sleep(3)
        self.__fazer_login()

    def retorna_fonte(self):
        self.__executar()
        time.sleep(3)
        print('\n>> Retornando o código fonte...\n')
        return self.__driver.page_source

    def fecha_conexao(self):
        self.__driver.close()
