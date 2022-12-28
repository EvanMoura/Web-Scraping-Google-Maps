# System
import os
import time
import pyperclip
import pandas as pd
from datetime import datetime

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# GUI
from tkinter.ttk import Label, LabelFrame, Frame, Button, Entry
from tkinter import Tk

        
class WebScraping(object):
    XPATH_CONTAINER        = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]'
    XPATH_FINALLY_MESSAGE  = '//span[@class="HlvSq"]'
    XPATH_NAME             = '//h1[@class="DUwDvf fontHeadlineLarge"]'
    XPATH_NAME_ADDRESS     = '//button[@data-tooltip="Copiar endereço"]'
    XPATH_NAME_TELEPHONE   = '//button[@data-tooltip="Copiar número de telefone"]'
    XPATH_NAME_LINK        = '//a[@class="hfpxzc"]'
    
    def __init__(self, product: str, city: str) -> None:
        self.options = Options()
        self.options.add_argument("start-maximized")
        self.options.add_experimental_option("excludeSwitches", ['enable-logging'])
        self.options.add_experimental_option("prefs", {'profile.default_content_setting_values.cookies': 2})
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)    
        self.action = ActionChains(self.driver)
        self.main(product=product, city=city)

    @staticmethod
    def get_hour() -> str:
        hour = str(datetime.today())[11:]
        return hour[:8]
        
    def get_links(self, url: str) -> list:
        self.driver.get(url) 
        time.sleep(5)
        links = []
        body = self.driver.find_element(By.XPATH, self.XPATH_CONTAINER)
        
        while True:
            time.sleep(0.5)
            body.send_keys(Keys.PAGE_DOWN)
            try:
                finally_message = self.driver.find_element(By.XPATH, self.XPATH_FINALLY_MESSAGE)
                if 'Você chegou ao final da lista.' in finally_message.text:
                    print(finally_message.text)
                    break
            
            except Exception:
                pass      
        
        for link in self.driver.find_elements(By.XPATH, self.XPATH_NAME_LINK):
            print(f"\nLink obtido: {link.get_attribute('href')}")
            if link.get_attribute('href') not in links:
                links.append(link.get_attribute('href'))
            
        return links

    def scraping(self, links: list) -> tuple:
        n = []  # --> Nomes de lugares
        t = []  # --> Telefones
        a = []  # --> Endereços
        l = []  # --> Links
        
        for link in links:
            self.driver.get(link)
            time.sleep(2)
            
            try:                      
                button_addr = self.driver.find_element(By.XPATH, "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[3]/div[2]/div/div/button")
                self.action.move_to_element(button_addr)
                button_addr.click()
                addr = pyperclip.paste()
                a.append(addr)
                
            except Exception as e:
                pass
            
            trys = 1
            row = 5                                           
            while True:
                try:                                               
                    button_tele = self.driver.find_element(By.CLASS_NAME, f"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[{row}]/div[2]/div/div[1]/button")
                    self.action.move_to_element(button_addr)
                    button_tele.click()
                    tele = pyperclip.paste()        
                    a.append(int(tele))
                    break
                
                except Exception as e:
                    print(f"Tentativas [{trys}]")
                    trys += 1
                    row += 1
                    if trys > 10:
                        a.append("")
                        break
                
                # tele = self.driver.find_element(By.XPATH, self.XPATH_NAME_TELEPHONE).text
                # addr = self.driver.find_element(By.XPATH, self.XPATH_NAME_ADDRESS).text
                name = self.driver.find_element(By.XPATH, self.XPATH_NAME).text
                
                #print(f"\n[{name}] [{tele}] [{addr}] [{link}]")
            
                n.append(name)
                # t.append(tele)
                # a.append(addr)
                l.append(link)
        
            #  0  1  2  3
        return n, t, a, l

    def main(self, product, city) -> None:
        try: 
            os.system("cls")
            result = self.get_links(url=f"https://www.google.com.br/maps/search/{product}+em+{city}")
            result_list = list(self.scraping(result))

            df = pd.DataFrame({'Nome': result_list[0], 'Telefone': result_list[1], 'Endereço': result_list[2], 'Links': result_list[3]})
            df.to_excel(f"Resultado da busca {product}.xlsx")
            print(df.head())

        except KeyboardInterrupt:
            self.driver.quit()


class MainFrame(Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.create_widgets()
    
    def create_widgets(self) -> None:
        def get_parameters():
            city = entry_city.get()
            product = entry_product.get().strip()
            WebScraping(product=product, city=city)
            
        frame = LabelFrame(self, text='Área de pesquisa')
        label_product = Label(frame, text='Produto')
        entry_product = Entry(frame, width=25)
        label_city = Label(frame, text='Cidade')
        entry_city = Entry(frame, width=15)
        button_search = Button(frame, text='Procurar', command=get_parameters)
        
        frame.grid(row=0, column=0, padx=5, pady=5)
        label_product.grid(row=0, column=0)
        entry_product.grid(row=0, column=1)
        label_city.grid(row=0, column=2)
        entry_city.grid(row=0, column=3)
        button_search.grid(row=1, column=3, padx=2.5, pady=2.5)


class Gui(Tk):
    NAME_PROGRAM = "Web Scraping"
    
    def __init__(self) -> None:
        super().__init__()
        self.title(self.NAME_PROGRAM)
        self.resizable(width=False, height=False)
        self.create_frame() 
        
    def create_frame(self) -> None:
        main_frame = MainFrame(self)
        main_frame.grid(row=0, column=0)
            

if __name__ == "__main__":
    Gui().mainloop()
