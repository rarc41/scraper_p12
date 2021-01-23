import requests
from bs4 import BeautifulSoup

URL='https://www.pagina12.com.ar/'


def parse_sections(link_section):
    try:
        response_link_section=requests.get(link_section)
        if response_link_section.status_code==200:
            html_section=BeautifulSoup(response_link_section.text, 'lxml')
            articles=html_section.find_all('div', attrs={'class': 'article-item__content'})
            # print(articles)

            links_to_news=[article.a.get('href') for article in articles]
            # return links_to_news
            print(links_to_news)
        else:
            raise ValueError(f'Error: {response_link_section.status_code}')

    except ValueError as ve:
        print(ve)

def parse_home_p12(url):
    try:
        response_p12=requests.get(url)
        if response_p12.status_code==200:
            html_home=BeautifulSoup(response_p12.text, 'lxml')
            # print(html_home.prettify())

            sections=html_home.find('div', attrs={'class':'p12-dropdown-content'}).find_all('a', attrs={'class':'p12-dropdown-item'})
            links_to_sections =[section.get('href') for section in sections]
            # return links_to_sections
            # print(links_to_sections)
            
            parse_sections(links_to_sections[0])
            
            
        else:
            raise ValueError(f'Error: {response_p12.status_code} ')
    except ValueError as ve:
        print('ve')

def run():
    parse_home_p12(URL)
if __name__ == '__main__':
    run()
