# -- coding: utf-8 --
import os
import codecs
import configparser

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")


class ReadConfig(object):
    def __init__(self):
        fd = open(configPath, encoding='utf-8')
        data = fd.read()

        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w", encoding='utf-8')
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath, encoding='utf-8')

    def get_email(self, name):
        value = None
        try:
            value = self.cf.get("EMAIL", name)
            return value
        except:
            return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_header(self, name):
        value = self.cf.get("HEADER", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    def get_title(self, name):
        value = self.cf.get("TITLE", name)
        return value


if __name__ == '__main__':
    rc = ReadConfig()
    a = rc.get_title('NUM')
    print(a)