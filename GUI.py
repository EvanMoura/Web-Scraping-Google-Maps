import  time
from tkinter.ttk import Frame, Label, Entry, Button, LabelFrame
from tkinter import Tk, filedialog, END
from core import WebScraping
from threading import Thread


class MainFrame(Frame):
    def __init__(self, root) -> None:
        super().__init__()
        self.createWidgets()
        
    def createWidgets(self):
        def search():
            webscraping = WebScraping()
            response = webscraping.get_links(value=entry_1.get())
            webscraping.enter_link(links=response[0], name=response[1])
            
        def file_search():
            filepath = filedialog.askopenfilename(defaultextension='.txt')
            entry_2.delete(0, END)
            entry_2.insert(0, filepath)
            
            words = []
            with open(file=filepath, mode='r', encoding='UTF-8') as file:
                for word in file.readlines():
                    words.append(word.strip())
            
            
            webscraping = WebScraping()
            for word in words:
                response = webscraping.get_links(value=word)
                df = webscraping.enter_link(links=response[0], input=response[1])
                time.sleep(60 * 1)
        
        
        labelf = LabelFrame(self, text="Área de pesquisa")
        label_desc_1 = Label(labelf, text="Pesquisa")
        entry_1 = Entry(labelf, width=40)
        button_search_1 = Button(labelf, text="Pesquisar", command=lambda: Thread(target=search).start())
    
        label_desc_2 = Label(labelf, text="Arquivo")
        entry_2 = Entry(labelf, width=40)
        button_search_2 = Button(labelf, text="Abrir...", command=lambda: Thread(target=file_search).start())
        
        
        
        labelf.grid(row=0, column=0, padx=10, pady=10)
        
        label_desc_1.grid(row=0, column=0)
        entry_1.grid(row=0, column=1)
        button_search_1.grid(row=0, column=2)
        
        label_desc_2.grid(row=1, column=0)
        entry_2.grid(row=1, column=1)
        button_search_2.grid(row=1, column=2)


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
    