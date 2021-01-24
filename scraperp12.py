import requests
from bs4 import BeautifulSoup

URL='https://www.pagina12.com.ar/'


def parse_notices(link_notice): #esta funcion extrae titulo, volanta, copete, contenido y autor de la noticia
    try:
        note=requests.get(link_notice)
        if note.status_code==200:
            html_note=BeautifulSoup(note.text, 'lxml')
            #extraemos el titulo
            title=html_note.find('h1', attrs={'class':'article-title'}).text
            print(f'Titulo de la noticia: {title}')

            #extraemos la fecha del articulo
            fecha=html_note.find('span', attrs={'pubdate':'pubdate'}).get('datetime')
            print(f'Fecha de publicacion: {fecha}')

            #si la noticia incluye una volanta, la extraemos
            try:
                volanta=html_note.find('h2', attrs={'class':'article-prefix'}).text
                print(f'Volanta: {volanta}')
            except Exception as e:
                print('Error: esta noticia no tiene volanta')
                print(e)
                print('\n')

            #si la noticia incluye un copete, lo extraemos
            try:
                copete=html_note.find('div', attrs={'class':'article-summary'}).text
                print(f'Copete: {copete}')
            except Exception as e:
                print('Error: esta noticia no tiene copete')
                print(e)
                print('\n')

            body=html_note.find('div', attrs={'class':'article-text'}).get_text(' ')
            print('Contenidp de la noticia: ')
            print(body)

            #extraemos el author, si es que lo tiene
            try:
                author=html_note.find('div', attrs={'class':'article-author'}).a.text
                print(f'Articulo escrito por: {author}')
            except Exception as e:
                print('Error: esta noticia no tiene un autor')
                print(e)
                

        else:
            raise Exception(f'{note.status_code}')

    except Exception as e:
        print('Error: ')
        print(e)
        print('\n')

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
            print('')
            print('***********Extracion toda la info de la noticia********\n')
            parse_notices(links_to_news[0])
        else:
            raise ValueError(f'Error en la request, status_code: {response_link_section.status_code}')

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
                        
            print('\n***********extrayendo los links de las noticias***********\n')
            parse_sections(links_to_sections[0])

        else:
            raise ValueError(f'Error: {response_p12.status_code} ')
    except ValueError as ve:
        print('ve')

def run():
    parse_home_p12(URL)
if __name__ == '__main__':
    run()
