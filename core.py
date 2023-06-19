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


class WebScraping:
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
            cursor.execute("CREATE TABLE IF NOT EXISTS Resultados(Date TEXT, Nome TEXT, Endereço TEXT, Telefone TEXT, Site TEXT, Input TEXT, Link TEXT);")
            
        
        
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
                    console.log(f"[{datetime.now().strftime('%H:%M:%S')}] [[green]Coleta de links concluido[/]]")
                    break

                except selenium.common.exceptions.NoSuchElementException:
                    pass

    
                time.sleep(1)
                
        except selenium.common.exceptions.ElementNotInteractableException:
            pass

        return links, value

    def enter_link(self, links: list, input: str):
        console.log(f"[blue]Links obtidos: [{len(links)}][/]")
        
        data = []
        
        try:
            for link in links:
                console.log(f"\n[{datetime.now().strftime('%H:%M:%S')}] [Coletando dados do link] [[green]{link}[/]]")
                line = {}

                time.sleep(1)
                self.driver.get(url=link)
                self.driver.execute_script("document.body.style.zoom='50%'")
                time.sleep(2.5)

                # Obtendo nome
                name_store = '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1'
                name_store_element = self.driver.find_element(By.XPATH, name_store)
                line['name'] = name_store_element.text
 
                # Obtendo dados
                try:
                    elements_number = self.driver.find_elements(By.CLASS_NAME, 'CsEnBe')
                    for element in elements_number:
                        value = element.get_attribute("aria-label")

                        if 'Website: ' in str(value):
                            line['website'] = str(value).replace("Website: ", "")
                            
                        if 'Telefone: ' in str(value):
                            line['telphone'] = str(value).replace("Telefone: ", "")
                            
                        if 'Endereço: ' in str(value):
                            line['address'] = str(value).replace("Endereço: ", "")

                except selenium.common.exceptions.NoSuchElementException:
                    pass
                
                line['link'] = link
                line['input'] = input
                line['date'] = datetime.now().strftime('%d/%m/%Y')
                columns = ['name', 'website', 'telphone', 'address', 'link', 'input']
                for column in columns:
                    if column not in line.keys():
                        line[column] = "Sem informação"

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
                                INSERT INTO Resultados (Data, Nome, Endereço, Telefone, Site, Input, Link)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            """,
                            (line['date'], line['name'], line['address'], line['telphone'], line['website'], line['input'], line['link'],)
                        )
                        console.log(f"[[green]Inserindo resultado de busca[/]] {line['name']}")