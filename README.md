Projeto com início de desenvolvimento em Eng. de Software 2024.1 - Continuação do Desenvolvimento em Eng. de Software 2024.2

Envolvidos(2024.1): Jean Araujo - DOUTORADO / RAFAEL ARAUJO - ESPECIAL / Felipe Pacheco - MESTRADO / Edjair Filho - MESTRADO / Arthur Miranda - GRADUAÇÃO / Mayanne Silva - GRADUAÇÃO / Maria Alves - GRADUAÇÃO
Envolvidos(2024.2): Sérgio Paz de Lira - ESPECIAL / João Paulo Felix - ESPECIAL / Saulo Fernando Bernardo  - MESTRADO / Arthur Sobral de Macedo - GRADUAÇÃO / Pedro Henrique Bezerra de Mello - GRADUAÇÃO / Sergio Henrique de Andrade Lima Filho - GRADUAÇÃO / Tiago Gaspar de Moura - GRADUAÇÃO

Ideias Iniciais: Projeto visa a construção de uma plataforma com editais de invocação, ou seja, Editais publicos/privados disponibilizados/em fase de resultado disponiveis por orgãos de fomento de pesquisa/ICTs (exemplo: FACEPE, CNPQ, SECTI, ....)

Plataforma WEB que seja possivel cadastrar Editais e Demonstrar esses editais:  
Editais (de forma inicial)
  https://www.secti.pe.gov.br/editais/
  https://www.facepe.br/editais/todos/
  http://memoria2.cnpq.br/web/guest/chamadas-publicas
  http://www.finep.gov.br/chamadas-publicas?situacao=aberta


░▄▀▀░▄▀▀▒█▀▄▒▄▀▄▒█▀▄░█░█▄░█░▄▀▒▒██▀░█▀▄░█░▀█▀▒▄▀▄░█░▄▀▀
▒▄██░▀▄▄░█▀▄░█▀█░█▀▒░█░█▒▀█░▀▄█░█▄▄▒█▄▀░█░▒█▒░█▀█░█▒▄██

# Scraping de Editais de Bolsas -Projeto EditalView
Esta parte do projeto foca na criação de bots que fazem o scraping (extração automatizada) de editais. No momento, contando com editais da FINEP(Financiadora de Estudos e Projetos) e FACEPE(Fundação de Amparo à Ciência e Tecnologia de Pernambuco). Esses bots ajudam a coletar informações sobre novas oportunidades e bolsas.

## Arquivos atuais do projeto
BOT_UPE_FACEPE.py: Este script coleta informações sobre editais de bolsas do site da FACEPE.

BOT_UPE_FINEP.py: Este script coleta informações sobre editais de bolsas do site da FINEP.

start.bots.sh.txt: Um script Bash que automatiza a execução dos dois bots. É usado para rodar os scripts periodicamente.

### Como utilizar?
Para rodar o projeto, é necessário se cumprir alguns requisitos:

- **Python** instalado no seu sistema.
- As bibliotecas necessárias para o Python. Você pode instalá-las usando os comandos: `pip install webdriver_manager` e `pip install unidecode`.

Com esse processo feito, você pode agora executar os bots manualmente!

### Executando manualmente
Para rodar os bots manualmente, basta abrir o terminal na pasta onde estão os arquivos e executar os seguintes comandos:

```command
sudo apt-get update
sudo apt-get install python3
```

# Automatizando a execução - Sistemas UNIX(Gnu/Linux e MacOS)
Para que os bots rodem automaticamente em intervalos regulares, você pode usar o arquivo start.bots.sh.txt em conjunto com o Crontab, que é uma ferramenta de agendamento de tarefas em sistemas Linux/macOS.
- Renomeie o arquivo `start.bots.sh.txt` para `start.bots.sh`

Dê permissão de execução ao script:

```command
chmod +x start.bots.sh
```

Abra a crontab para edição:

```command
crontab -e
```

Adicione a seguinte linha para rodar os bots a cada 4 horas, Substituindo /caminho_para/ pelo caminho completo do arquivo **start.bots.sh** no seu computador.:
```command
*/14400 * * * * sh /caminho_para/start.bots.sh
```
salve com :wq.

Agora os seus bots serão executados automaticamente a cada 4 horas.