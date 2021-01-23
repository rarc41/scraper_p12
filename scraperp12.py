from lxml.html import parse
import requests
from bs4 import BeautifulSoup

URL='https://www.pagina12.com.ar/'




def parse_home(url):
    try:
        response_p12=requests.get(url)
        if response_p12.status_code==200:
            html_home=BeautifulSoup(response_p12.text, 'lxml')
            # print(html_home.prettify())
            
            secciones=html_home.find('div', attrs={'class':'p12-dropdown-content'})
            print(secciones.prettify())
            # .find_all('a', attrs={'class':'p12-dropdown-item'})
        else:
            raise ValueError(f'Error: {response_p12.status_code} ')
    except ValueError as ve:
        print('ve')

def run():
    parse_home(URL)

if __name__ == '__main__':
    run()
