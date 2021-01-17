from decouple import config


class FileHander:

    @staticmethod
    def ler_aquivo():
        with open(config('FILE_NAME'), 'r', encoding='utf-8') as ld:
            return ld.read()

    @staticmethod
    def escrever_em_arquivo(t):
        with open(config('FILE_NAME'), 'w', encoding='utf-8') as ld:
            ld.write(t)
