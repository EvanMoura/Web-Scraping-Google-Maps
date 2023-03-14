from tkinter.ttk import Frame, Label, Entry, Button, LabelFrame
from tkinter import Tk
from core import WebScraping
from threading import Thread


class MainFrame(Frame):
    def __init__(self, root) -> None:
        super().__init__()
        self.createWidgets()
        
    def createWidgets(self):
        def x():
            webscraping = WebScraping()
            response = webscraping.get_links(value=entry.get())
            webscraping.enter_link(links=response[0], name=response[1])
        
        
        labelf = LabelFrame(self, text="Área de pesquisa")
        label_desc = Label(labelf, text="Pesquisa")
        entry = Entry(labelf, width=40)
        button_search = Button(labelf, text="Pesquisar", command=lambda: Thread(target=x).start())
        
        labelf.grid(row=0, column=0, padx=10, pady=10)
        label_desc.grid(row=0, column=0)
        entry.grid(row=0, column=1)
        button_search.grid(row=0, column=2)


class App(Tk):
    def __init__(self) -> None:
        super().__init__()
        self._name: str
        self._version: str
        self._x: str
        self._y: str
    
    def setSettings(self):
        self.title(f"{self._name} - {self._version}")
        self.resizable(False, False)
        
    def createWidgets(self):
        frame = MainFrame(self)
        frame.grid(row=0, column=0)
        
     # --- Set Name   
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        
    # --- Set version
    @property
    def version(self):
        return self._version
    
    @version.setter
    def version(self, value):
        self._version = value
        
    # --- Set x
    @property
    def resize_x(self):
        return self._x
    
    @resize_x.setter
    def resize_x(self, x):
        self._x = x
      
     # --- Set y
    @property
    def resize_y(self):
        return self._y
    
    @resize_y.setter
    def resize_y(self, y):
        self._y = y
    
    
if __name__ == "__main__":
    app = App()
    app.name = "Web Scraping"
    app.version = "20230314"
    app.resize_x = False
    app.resize_y = False
    app.setSettings()
    app.createWidgets()
    app.mainloop()
    