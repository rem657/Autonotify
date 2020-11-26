from selenium import webdriver
from time import sleep
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from numpy import random

class Bot_I_need_card_plz():
    def __init__(self,URL:str = "https://www.newegg.ca/p/pl?d=nvidia+3080&N=100007708&isdeptsrh=1"):
        self.list_found = []
        self.core(URL)

    def core(self,URL):
        while(True):
            driver = self.open_web(URL)
            elems = driver.find_elements_by_class_name("item-cells-wrap")
            cards = []
            if len(elems) > 1:
                for sections in elems:
                    try:
                        cards += sections.find_elements_by_class_name("item-cell")# + elems[1].find_elements_by_class_name("item-cell")
                    except Exception as e:
                        print(e)
                        driver.close()
                        continue
            else:
                try:
                    cards = elems[0].find_elements_by_class_name("item-cell")
                except Exception as e:
                    print(e)
                    driver.close()
                    continue
            list_available = []
            for card in cards:
                available = self.is_available(card)
                # print(available)
                if available:
                # list_available = []
                    list_available.append(card)
            temp_name = []
            if bool(list_available):
                title = "Une carte est maintenant en stock:\n\n"
                text = ""
                for card in list_available:
                    name = self.get_name(card)
                    temp_name.append(name)
                    if name not in self.list_found:
                        href = self.get_hyperlink(card)
                        text += f"{name} :\n {href}\n\n\n"
                        self.list_found.append(name)
                if text != "":
                    text = title + text
                    for address in self.get_send_to():
                        # continue
                        self.send_email(message=text,send_to=address,subject="GPU(s) Disponible(s) !")
            for name in self.list_found:
                if name not in temp_name:
                    self.list_found.remove(name)
            driver.close()
            sleep(((random.normal(loc = 10, scale = 5, size =(1,))[0])**2)**(0.5))

    @staticmethod
    def get_name(card) -> str:
        return card.find_element_by_xpath(f".//div[@class='item-container']/div[@class='item-info']/a[@class='item-title']").text

    @staticmethod
    def get_hyperlink(card) -> str:
        return card.find_element_by_xpath(
            f".//div[@class='item-container']/div[@class='item-info']/a").get_attribute("href")

    @staticmethod
    def is_available(card):
        text:str = card.find_element_by_class_name("btn").text
        # print(text)
        return False if text.upper() in ["AUTO NOTIFY","SOLD OUT"] else True

    @staticmethod
    def open_web(URL:str) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(options=options)
        browser.get(URL)
        return browser

    @staticmethod
    def get_credential():
        """
        This method gets the email address and its password from a local file
        :return:
        """
        list_cred = []
        with open("credential.txt","r") as cred:
            list_cred.append(cred.readline()[:-1])
            list_cred.append(cred.readline())
        return tuple(list_cred)

    @staticmethod
    def get_send_to():
        with open("payroll.txt", "r") as cred:
            list_send_to = cred.readlines()
        for index,elem in enumerate(list_send_to):
            if index != len(list_send_to) - 1:
                list_send_to[index] = list_send_to[index][:-1]
            else:
                list_send_to[index] = list_send_to[index]

        return tuple(list_send_to)

    @staticmethod
    def send_email(message:str,send_to:str,subject:str):
        port = 465
        address,pw = Bot_I_need_card_plz.get_credential()
        context = ssl.create_default_context()
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = address
        msg["To"] = send_to
        msg.attach(MIMEText(message,"plain"))
        with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
            server.login(address,pw)
            try:
                server.sendmail(address,send_to,msg.as_string())
            except Exception as e:
                print(e)

if __name__ == '__main__':
    Bot_I_need_card_plz()
