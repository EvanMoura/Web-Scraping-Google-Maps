# Web Scraping do Google Maps

Este é um código Python para fazer web scraping no Google Maps usando Selenium. O objetivo do código é coletar informações de empresas, como nome, endereço, número de telefone e link da página do Google Maps, a partir de uma pesquisa de palavra-chave.

O código usa o módulo Selenium para automatizar o processo de navegação e coleta de dados do Google Maps. O Google Maps é aberto em um navegador Chrome, e o script navega por várias páginas de resultados da pesquisa e coleta os dados das empresas em cada página.

Os dados são armazenados em um dataframe do pandas e exportados para um arquivo Excel para análise posterior.

O código usa as seguintes bibliotecas Python:

- time
- pandas
- selenium
- datetime
- webdriver_manager

O código também usa a classe Bcolors para adicionar cores ao texto do terminal.

O código tem duas funções principais:

- **get_links**: obtém uma lista de links das páginas do Google Maps que correspondem à pesquisa de palavra-chave.
- **enter_link**: acessa cada um dos links coletados pela função get_links e extrai as informações da empresa.

# Como usar o código

Para usar o código, basta instalar as bibliotecas necessárias e executar o arquivo GUI.py. O código foi criado usando o Google Chrome, portanto, certifique-se de que o Chrome esteja instalado em sua máquina.

O resultado final será um arquivo Excel como o nome da pesquisa contendo as informações coletadas.

# Limitações

O código pode apresentar limitações e problemas, pois depende de muitos fatores externos, como a estabilidade da conexão com a internet, as atualizações do Google Maps e as alterações na estrutura HTML do site.

Além disso, o Google Maps tem uma política rígida contra web scraping e pode bloquear o acesso do usuário ao site. É importante usar o código com cautela e responsabilidade, e verificar a política de uso do Google Maps antes de usar o código em um ambiente de produção.
