# Pessoal, para cada feature que vocês entregarem, façam a documentação aqui.

> Exemplo, se for um endpoint post, basta incluir o modelo de requisição e a resposta.

>Se você está trabalhando em alguma exception, inclua as restrições aqui na documentação também no endpoint apropriado.

>**Se todo mundo fizer um pouco da documentação do que entrega, no final a documentação fica pronta. No caso seria só acertar alguns detalhes.**

## Importante:

Tentem padronizar a mensagem conforme o colega vem fazendo. Por exemplo, no slack a gente vai publicando padrões a seguir. Se todos os textos devem ser normalizados com title, todo mundo segue com title, e assim vai...

## Sobre tests e commands
Comandos uteis, como o de popular tabelas, e testes que podem ser utilizados durante o desenvolvimento podem ser avisados e documentados pelo slack.
Vamos focar os testes nos endpoints e nas views. É interessante cada um fazer o test de uma view e trabalhar em outra view que tenha um teste feito pelo colega.
É sempre melhor a pessoa que fez o teste não ser a pessoa que faz a feature.

## Algumas bibliotecas que eu já deixei instaladas

- Black (para padronizarmos)
- Faker (para criar comandos cli)
- ipdb (para facilitar a localização de bugs)
- pytest
- Flask-JWT-Extended
- E demais bibliotecas do Flask e Cia.

## Sobre a estrutura geral
- Montei a árvore de diretórios com os principais arquivos.
- O create app já está montado.
- O routes já tem um init principal montado para receber as rotas.
- O database está configurado e não precisa importar as models mais por ele. Elas devem ser importadas no __init__.py de models.
- Migrations configurado também. Só fazer o flask db init e construir as models.
- Sobre o diretório "tests", já tem um conftest. Só criar os testes mesmo. Se precisarem de ajuda nessa parte é só dar um grito.

# Comece a documentar daqui em diante...