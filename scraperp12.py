import requests
from bs4 import BeautifulSoup
import pandas as pd


URL='https://www.pagina12.com.ar/'


def parse_notice(link_notice): #esta funcion extrae titulo, volanta, copete, contenido y autor de la noticia
    #diccionaro para guardar informacion de la noticia
    info_notice={}
    try:
        note=requests.get(link_notice)
        if note.status_code==200:
            html_note=BeautifulSoup(note.text, 'lxml')

            #extraemos el titulo
            title=html_note.find('h1', attrs={'class':'article-title'})
            if title:
                info_notice['Titulo']=title.text
            else:
                info_notice['Titulo']=None

            #extraemos la fecha del articulo
            fecha=html_note.find('span', attrs={'pubdate':'pubdate'})
            if fecha:
                info_notice['Fecha_publicacion']=fecha.get('datetime')
            else:
                info_notice['Fecha_publicacion']=None

            #si la noticia incluye una volanta, la extraemos
            volanta=html_note.find('h2', attrs={'class':'article-prefix'})
            if volanta:
                info_notice['Volanta']=volanta.text
            else:
                info_notice['Volanta']=None

            #si la noticia incluye un copete, lo extraemos
            copete=html_note.find('div', attrs={'class':'article-summary'})
            if copete:
                info_notice['Copete']=copete.text
            else:
                info_notice['Copete']=None

            body=html_note.find('div', attrs={'class':'article-text'})
            info_notice['Body']=body.get_text(' ')

            #extraemos el author, si es que lo tiene
            author=html_note.find('div', attrs={'class':'article-author'})
            if author:
                info_notice['Author']=author.a.text
            else:
                info_notice['Author']=None

    except Exception as e:
        print('Error: ')
        print(e)
        print('\n')

    return info_notice

def parse_sections(link_section):
    try:
        response_link_section=requests.get(link_section)
        if response_link_section.status_code==200:
            html_section=BeautifulSoup(response_link_section.text, 'lxml')
            articles=html_section.find_all('div', attrs={'class': 'article-item__content'})

            links_to_news=[article.a.get('href') for article in articles]
            return links_to_news

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
            return links_to_sections

        else:
            raise ValueError(f'Error: {response_p12.status_code} ')
    except ValueError as ve:
        print('ve')

def run():
    links_to_sections=parse_home_p12(URL)
    # print(links_to_sections)
    links_to_notices=[parse_sections(link) for link in links_to_sections]
    news=[]
    for list_links in links_to_notices:
        news.extend(list_links)
    # print(news)
    data=[]
    for i, link_notice in enumerate(news):
        print(f'Scraping nota{i}/{len(news)}')
        data.append(parse_notice(link_notice))
    df=pd.DataFrame(data)
    df.to_csv('News Pagina12.csv')
    
if __name__ == '__main__':
    run()
