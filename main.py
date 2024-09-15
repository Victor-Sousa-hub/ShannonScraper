import httpx
from bs4 import BeautifulSoup
import pandas as pd
import asyncio
import argparse
import sys

parser = argparse.ArgumentParser(description='Faz uma busca de artigos no arxiv ou scielo sobre' 
                                              ' o tema selcionado retona titulo,autor,data,sumario e link do artigo'
                                              ' Usage: main.py -a "[Assunto desejado]"')
parser.add_argument('--assunto',type=str,metavar='-a',required=True,help='Assunto que deseja buscar')
parser.add_argument('--periodico',type=str,metavar='-p',required=False,help='Seleciona o periodico que deseja pesquisar ' 
                                                                            'Usage: main.py --assunto [assunto] --periodico [scielo] [arxiv] '
                                                                            '[Caso esteja vazio buscara em ambos]')
parser.add_argument('--saida',type=str,metavar='-o',required=False,help='Nome do arquivo de saida das buscas '
                                                                        'Usage: main.py --assunto [assunto] --saida [nome_do_arquivo.csv] '
                                                                        'Caso esteja vazio sera salvo como [periodico_assunto.csv]')

args = parser.parse_args()

async def fetch(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response


async def scrape_arxiv(assunto,saida):
    f_assunto = assunto.replace(' ','+')
    url = f"https://arxiv.org/search/?query={f_assunto}&searchtype=all"
    response = await fetch(url)

    if response.status_code != 200:
        print(f'Erro ao acessar o site. Status code: {response.status_code}')
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    #coleta todos os artigos
    artigos = soup.find_all('li', class_='arxiv-result')

    #Listas para armazenar todos os dados coletados
    titulos   = []
    autores   = []
    datas     = []
    sumarios  = []

    for artigo in artigos:
        titulo  = artigo.find('p',class_='title is-5 mathjax').text.strip()
        autor   = artigo.find('p',class_='authors').text.strip()
        data    = artigo.find('p',class_='is-size-7').text.strip()
        sumario = artigo.find('span',class_='abstract-full has-text-grey-dark mathjax').text.strip()

        titulos.append(titulo)
        autores.append(autor)
        datas.append(data)
        sumarios.append(sumario)

    #Cria um dataframe dos dados coletados
    df = pd.DataFrame({
        'Titulo': titulos,
        'Autor(es)': autores,
        'Data': datas,
        'Sumario': sumarios
    })

    #Salva em um arquivo CSV
    if saida:
        df.to_csv(f'Artigos/arxiv_{saida}',index=False)
        print(f'Scraping concluido! Dados salvos em Artigos/arxix_{saida}.csv')
    else:
        df.to_csv(f'Artigos/arxiv_{assunto}.csv',index=False)
        print(f'Scraping concluido! Dados salvos em Artigos/arxix_{assunto}.csv')


async def scrape_scielo(assunto,saida):
    f_assunto = assunto.replace(' ','+')
    url = f'https://search.scielo.org/?q={f_assunto}'
    response = await fetch(url)

    if response.status_code != 200:
        print(f"Erro ao acessar o site. Status code: {response.status_code}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Coletar todos os artigos
    artigos = soup.find_all('div', class_='item')

    # Listas para armazenar os dados coletados
    titulos = []
    autores = []
    sumarios = []

    for artigo in artigos:
        titulo_tag = artigo.find('strong', class_='title')
        titulo = titulo_tag.text.strip() if titulo_tag else "Sem título"

        # Verifica se os autores existem
        autor_tag = artigo.find('a', class_='author')
        autor = autor_tag.text.strip() if autor_tag else "Autores não disponíveis"

        # Verifica se o resumo existe
        sumario_tag = artigo.find('div', class_='abstract')
        sumario = sumario_tag.text.strip() if sumario_tag else "Resumo não disponível"

        titulos.append(titulo)
        autores.append(autor)
        sumarios.append(sumario)

    # Criar um DataFrame com os dados coletados
    df = pd.DataFrame({
        'titulo': titulos,
        'autor(es)': autores,
        'sumario': sumarios
    })
    
    # Salvar em um arquivo CSV
    if saida:
        df.to_csv(f'Artigos/scielo_{saida}',index=False)
        print(f"Scraping concluído! Dados salvos em 'scielo_{saida}.csv'")
    else:
        df.to_csv(f'Artigos/scielo_{assunto}.csv', index=False)
        print(f"Scraping concluído! Dados salvos em 'scielo_{assunto}.csv'")
        


if __name__ == '__main__':
    saida = None
    if args.saida:
        saida = args.saida
    if not args.periodico:
        asyncio.run(scrape_scielo(args.assunto,saida))
        asyncio.run(scrape_arxiv(args.assunto,saida))
    if args.periodico == 'scielo':
        asyncio.run(scrape_scielo(args.assunto,saida))
    elif args.periodico == 'arxiv':
        asyncio.run(scrape_arxiv(args.assunto,saida))
    else:
        print(parser.format_help())
    