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
- Adicionei a tag v0.0. No primeiro mvp ela vai v1.0, depois passa para main. Aí podemos ir trabalhando nos extras nas novas versões.

# Comece a documentar daqui em diante...

![Captura de tela de 2022-04-27 00-08-14](https://user-images.githubusercontent.com/97132510/165432646-227a0248-12a9-4790-b366-c3d2f205ffa2.png)

<h1 align="center">API - BabyShower</h1>

<h2 align="center">Este é o backend da aplicação BabyShower - O objetivo é desenvolver uma plataforma em que os pais possam se cadastrar e interagir com outras pais que passam por fases de vida similares às suas. Nessa plataforma eles se cadastram e também cadastram produtos que não precisa mais.</h2>

[Arquivo para o insomnia](https://drive.google.com/file/d/1Nia7ipq4zCmrQGLPfBY2ICDIZVlDih5N/view?usp=sharing)

O url base da API é [baseUrl](http://localhost:5000/api)

## Rotas que não precisam de autenticação

### Rotas Products
### Obter todos os produtos
`GET /api/products - FORMATO DA REQUISIÇÃO`
```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:
`GET /api/products - FORMATO DA RESPOSTA - STATUS 200`
```json
{
  "products": [
    {
      "price": "100.0",
      "description": "Para crianças de até 2",
      "id": 1,
      "sold": false,
      "title": "Bebe conforto",
      "parent_id": 1,
      "image": "https://google.com"
	},
	{
	  "price": "150.97",
	  "description": "Para crianças de até 2",
	  "id": 2,
	  "sold": false,
	  "title": "Carrinho de bebe",
	  "parent_id": 1,
	  "image": "https://google.com"
	}
  ]
}
```

Podemos utilizar os query params para mudar a lista, mudando a paginação, podemos alterar quantos produtos queremos no perPage e alterar a página no parâmetro page. Podemos também acrescentar parametros para fazer filtragens. Uma requisição apenas no /products irá trazer 5 produtos na página 1.
`GET /api/products?perPage=3&page=1&price=100.0 - FORMATO DA RESPOSTA - STATUS 200`
```json
{
  "products": {
    {
      "price": "100.0",
      "description": "Para crianças de até 2",
      "id": 1,
      "sold": false,
      "title": "Bebe conforto",
      "parent_id": 1,
      "image": "https://google.com"
    },{
      "price": "100.0",
      "description": "Para crianças de até 3",
      "id": 2,
      "sold": false,
      "title": "Bebe conforto",
      "parent_id": 1,
      "image": "https://google.com"
    },{
      "price": "100.0",
      "description": "Para crianças de até 4",
      "id": 4,
      "sold": false,
      "title": "Bebe conforto",
      "parent_id": 1,
      "image": "https://google.com"
    }
  }
}
```

### Obter produto por id
`GET /api/products/<product_id> - FORMATO DA REQUISIÇÃO`
```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:
`GET /api/products/<product_id> - FORMATO DA RESPOSTA - STATUS 200`
```json
{
  "price": "100.0",
  "description": "Para crianças de até 2",
  "id": 1,
  "sold": false,
  "title": "Bebe conforto",
  "parent_id": 1,
  "image": "https://google.com"
}
```

### Obter produto pelo id do parent
`GET /api/products/by_parent/<parent_id> - FORMATO DA REQUISIÇÃO`
```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:
`GET /api/products/by_parent/<parent_id> - FORMATO DA RESPOSTA - STATUS 200`
```json
{
  "products": [
  	{
  	  "price": "100.0",
  	  "description": "Para crianças de até 2",
  	  "id": 1,
  	  "sold": false,
  	  "title": "Bebe conforto",
  	  "parent_id": 1,
  	  "image": "https://google.com"
  	},
  	{
  	  "price": "150.97",
  	  "description": "Para crianças de até 2",
  	  "id": 2,
  	  "sold": false,
  	  "title": "Carrinho de bebe",
  	  "parent_id": 1,
  	  "image": "https://google.com"
  	}
  ]
}
```

### Obter produto por query params
`GET /api/products/params?title=Bebe conforto&parent_id=1&price=100.0 - FORMATO DA REQUISIÇÃO`
```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:
`GET /api/products/params?title=Bebe conforto&parent_id=1&price=100.0 - FORMATO DA RESPOSTA - STATUS 200`
```json
{
  "products": [
  	{
  	  "price": "100.0",
  	  "description": "Para crianças de até 2",
  	  "id": 1,
  	  "sold": false,
  	  "title": "Bebe conforto",
  	  "parent_id": 1,
  	  "image": "https://google.com"
  	}
  ]
}
```

### Rotas Categories
### Obter todas as categories
`GET /api/categories - FORMATO DA REQUISIÇÃO`
```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:
`GET /api/categories - FORMATO DA RESPOSTA - STATUS 200`
```json
{
  "products": [
    {
		"id": 1,
		"name": "até 3 meses",
		"description": "Tudo o que o seu bebê precisa até os seus 3 meses"
	},
	{
		"id": 2,
		"name": "até 6 meses",
		"description": "Tudo o que o seu bebê precisa até os seus 6 meses"
	},
	{
		"id": 3,
		"name": "até 9 meses",
		"description": "Tudo o que o seu bebê precisa até os seus 9 meses"
	}
  ]
}
```

### Rotas Parents

### Obter todos os parents
`GET /api/parents - FORMATO DA REQUISIÇÃO`
```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:
`GET /api/parents - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"parents": [
		{
			"cpf": "12312312311",
			"username": "Maria",
			"email": "km@mail.com",
			"name": "Karen",
			"phone": "11223344556",
			"password_hash": "pbkdf2:sha256:blablabla"
		},
		{
			"cpf": "12312312312",
			"username": "fulano",
			"email": "fulano@mail.com",
			"name": "Fulano de Tal",
			"phone": "99999999999",
			"password_hash": "pbkdf2:sha256:blablabla"
		},
	]
}
```

### Criar novo parent
`POST /api/parents - FORMATO DA REQUISIÇÃO`
```JSON
{
  "cpf": "12312312312",
  "username": "fulano",
  "email": "fulano@mail.com",
  "password": "k3nz13",
  "name": "Fulano de Tal",
  "phone": "99999999999"
}
```

#### Caso dê tudo certo, a resposta será assim:
`POST /api/parents - FORMATO DA RESPOSTA - STATUS 201`
```json
{
	"cpf": "12312312313",
	"username": "fulano",
	"email": "fulano@mail.com",
	"name": "Fulano de Tal",
	"phone": "99999999999",
	"password_hash": "pbkdf2:sha256:blablabla"
}
```
