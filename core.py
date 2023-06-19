# System
import os
import time
import sqlite3
import pandas as pd
import selenium.common.exceptions
from datetime import datetime
from rich.console import Console

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


console = Console()


class Bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKCYAN    = '\033[96m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'


class WebScraping(Bcolors):
    home = '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]'
    ads      = '//a[@class="hfpxzc"]'
    end_page = '//span[@class="HlvSq"]'

    def __init__(self) -> None:
        self.options = Options()
        self.options.add_argument("start-maximized")
        self.options.add_experimental_option("excludeSwitches", ['enable-logging'])
        self.options.add_experimental_option("prefs", {'profile.default_content_setting_values.cookies': 2})
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.action = ActionChains(self.driver)
        
        try:
            os.mkdir(".data")
            
        except FileExistsError:
            pass
        
        with sqlite3.connect(database='.data/Google Maps.sqlite') as db:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Resultados(Nome TEXT, Endereço TEXT, Telefone TEXT, Input TEXT, Link TEXT);")
            
        
        
    def get_links(self, value: str) -> list:
        links = []

        self.driver.get(f"https://www.google.com.br/maps/search/{value}/")
        
        # Coleta de Links da pesquisa
        try:
            home = self.driver.find_element(By.XPATH, self.home)
            while True:
                links_element = self.driver.find_elements(By.XPATH, self.ads)
                for link_element in links_element:
                    link = link_element.get_attribute("href")
                    if link not in links:
                        links.append(link)

                home.send_keys(Keys.PAGE_DOWN)

                try:
                    self.driver.find_element(By.XPATH, self.end_page)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] [{self.OKGREEN}Coleta de links concluido{self.ENDC}]")
                    break

                except selenium.common.exceptions.NoSuchElementException:
                    pass

    
                time.sleep(1)
                
        except selenium.common.exceptions.ElementNotInteractableException:
            pass

        return links, value

    def enter_link(self, links: list, input: str):
        print(f"{Bcolors.OKBLUE} Links obtidos: [{len(links)}]{Bcolors.ENDC}")
        
        data = []
        
        try:
            for link in links:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] [Coletando dados do link] [{self.OKGREEN}{link}{self.ENDC}]")
                line = {}

                time.sleep(1)
                self.driver.get(url=link)
                self.driver.execute_script("document.body.style.zoom='50%'")
                time.sleep(2.5)

                # Obtendo nome
                name_store = '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1'
                name_store_element = self.driver.find_element(By.XPATH, name_store)
                line['name'] = (name_store_element.text)

                # Obtendo endereço
                try:
                    a = 0
                    elements_number = self.driver.find_elements(By.CLASS_NAME, 'CsEnBe')
                    for i in elements_number:
                        value = i.get_attribute("aria-label")
                        if 'Endereço: ' in str(value):
                            line['address'] = str(value).replace("Endereço: ", "")
                            a += 1
                            
                    if a == 0:
                        line['address'] =  "Sem informação"
        
                except selenium.common.exceptions.NoSuchElementException:
                    pass

                # Obtendo número
                try:
                    b = 0
                    elements_number = self.driver.find_elements(By.CLASS_NAME, 'CsEnBe')
                    for i in elements_number:
                        value = i.get_attribute("aria-label")
                        if 'Telefone: ' in str(value):
                            line['telphone'] = str(value).replace("Telefone: ", "")
                            b += 1
                            
                    if b == 0:
                        line['telphone'] = "Sem informação"
    
                except selenium.common.exceptions.NoSuchElementException:
                    pass
                
                line['link'] = link
                line['input'] = input
                data.append(line)

        except KeyboardInterrupt:
            self.driver.close()
        
        finally:
            for line in data:
                with sqlite3.connect(database='.data/Google Maps.sqlite') as db:
                    cursor = db.cursor()
                
                    cursor.execute("SELECT 1 FROM Resultados WHERE Link = ?", (line['link'],))
                    result = cursor.fetchall()
                    if not result:
                        cursor.execute(
                            """
                                INSERT INTO Resultados (Nome, Endereço, Telefone, Input, Link)
                                VALUES (?, ?, ?, ?)
                            """,
                            (line['name'], line['address'], line['telphone'], line['input'], line['link'],)
                        )
                        console.log(f"[[green]Inserindo resultado de busca[/]] {line['name']}")