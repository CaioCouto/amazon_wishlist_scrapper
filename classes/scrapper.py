import re

from bs4 import BeautifulSoup
from classes.access_bot import Bot
from classes.file_handler import FileHander


class Scrapper:

    def __init__(self):
        self.__s = self.__define_objeto_soup()
        self.__nomes_dos_itens = self.__busca_nomes_dos_itens()
        self.__valores_dos_itens = self.__busca_valores_dos_itens()
        self.__valores_antigos_dos_itens = self.__busca_valores_antigos_dos_itens()
        self.__texto_final = ''

    def __define_objeto_soup(self):
        bot = Bot()
        fonte_pagina = bot.retorna_fonte()
        bot.fecha_conexao()
        return BeautifulSoup(fonte_pagina, 'html.parser')

    def __busca_nomes_dos_itens(self):
        itens = self.__s.find_all('a', attrs={'id': re.compile('itemName_')})
        return [i.get_text() for i in itens]

    def __busca_valores_dos_itens(self):
        valores = self.__s.find_all('span', attrs={'class': 'a-offscreen'})
        valores = ' '.join([i.get_text() for i in valores])
        padrao = '\\d{1,4}\\,\\d{1,2}'
        return re.findall(padrao, valores)

    def __valida_valores_antigos(self, va):
        if (len(va) > 0):
            return [v for v in va]
        else:
            return ['00,00' for _ in range(len(self.__valores_dos_itens))]

    def __busca_valores_antigos_dos_itens(self):
        texto = FileHander().ler_aquivo()
        padrao = '\\d{1,4}\\,\\d{1,2}'
        return self.__valida_valores_antigos(re.findall(padrao, texto))

    def __retorna_par_item_valor(self):
        return \
            zip(self.__nomes_dos_itens, self.__valores_dos_itens, self.__valores_antigos_dos_itens)

    def __gera_texto_final(self, texto):
        self.__texto_final += texto

    def imprime_lista_de_desejos(self):
        print('>> Imprimindo Lista de Desejos...\n')
        for item, valor, valor_antigo in self.__retorna_par_item_valor():
            texto = f'>> Item: {item}\n>> Valor: R$ {valor} (era R$ {valor_antigo.replace(",", ".")})\n'
            texto += '------------------------------------\n'
            self.__gera_texto_final(texto)
        print(self.__texto_final)
        FileHander().escrever_em_arquivo(self.__texto_final)
