# Scraper de Artigos Acadêmicos

Este é um script Python para buscar e coletar artigos acadêmicos de dois periódicos, **Arxiv** e **SciELO**, com base em um assunto específico. O script utiliza `httpx` para requisições HTTP assíncronas e `BeautifulSoup` para parsear o HTML. Os resultados são salvos em arquivos CSV.

## Requisitos

Certifique-se de ter as seguintes bibliotecas instaladas:

- `httpx`
- `beautifulsoup4`
- `pandas`

Você pode instalar essas dependências com:

```bash
pip install httpx beautifulsoup4 pandas
Uso
Execução do Script
Você pode executar o script a partir da linha de comando com diferentes opções:

bash
Copiar código
python main.py --assunto "[Assunto desejado]" [--periodico [scielo|arxiv]] [--saida [nome_do_arquivo.csv]]
Argumentos
--assunto (obrigatório): O assunto que deseja buscar. Deve ser fornecido entre aspas se contiver espaços.

Exemplo: --assunto "machine learning"
--periodico (opcional): Seleciona o periódico onde a busca será realizada. Pode ser scielo, arxiv ou deixado em branco para buscar em ambos.

Exemplo: --periodico scielo
--saida (opcional): Nome do arquivo CSV onde os resultados serão salvos. Se não fornecido, o arquivo será salvo com o formato [periodico_assunto.csv].

Exemplo: --saida resultados.csv
Exemplos de Uso
Para buscar artigos sobre "machine learning" em ambos os periódicos e salvar os resultados em um arquivo CSV:

bash
Copiar código
python main.py --assunto "machine learning" --saida resultados.csv
Para buscar apenas no periódico SciELO:

bash
Copiar código
python main.py --assunto "machine learning" --periodico scielo
Para buscar apenas no periódico Arxiv:

bash
Copiar código
python main.py --assunto "machine learning" --periodico arxiv
Estrutura do Projeto
main.py: O script principal que realiza o scraping dos artigos.
Artigos/: Diretório onde os arquivos CSV serão salvos.
Contribuição
Se você tiver sugestões ou encontrar problemas, sinta-se à vontade para contribuir com este projeto. Para contribuir, você pode abrir um issue ou um pull request no repositório.

Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.