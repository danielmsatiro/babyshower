![Captura de tela de 2022-04-27 00-08-14](https://user-images.githubusercontent.com/97132510/165432646-227a0248-12a9-4790-b366-c3d2f205ffa2.png)

<h1 align="center">API - BabyShower</h1>

<h2 align="center">Este é o backend da aplicação BabyShower - O objetivo é desenvolver uma plataforma em que os pais possam se cadastrar e interagir com outros pais que passam por fases de vida similares às suas. Nessa plataforma eles se cadastram e também cadastram produtos que não precisa mais.</h2>

[Arquivo para o insomnia](https://drive.google.com/file/d/1Nia7ipq4zCmrQGLPfBY2ICDIZVlDih5N/view?usp=sharing)

O url base da API é [baseUrl](http://localhost:5000/api)

# Rotas Products

## **Rotas que não precisam de autenticação**
<h2 align="center">Obter todos os produtos</h2>

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

<h2 align="center">Obter produto por id</h2>

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

<h2 align="center">Obter produto pelo id do parent</h2>

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

<h2 align="center">Obter produto por query params</h2>

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
## **Rotas que precisam de autenticação**
<h2 align="center">Criar novo produto</h2>

`POST /api/products - FORMATO DA REQUISIÇÃO`
```JSON
{
  "title": "Lorem ipsum",
  "price": 100.0,
  "parent_id": 1,
  "description": "Lorem ipsum pa pa pa, Lorem ipsum pa pa pa",
  "image": "http://imagem"
}
```

#### Caso dê tudo certo, a resposta será assim:
`POST /api/products - FORMATO DA RESPOSTA - STATUS 201`
```json
{
  "id": 1,
  "title": "Lorem ipsum",
  "price": "100.0",
  "parent_id": 1,
  "description": "Lorem ipsum pa pa pa, Lorem ipsum pa pa pa",
  "image": "http://imagem"
}
```

<h2 align="center">Atualizar produto por id</h2>

`PATCH /api/products/1 - FORMATO DA REQUISIÇÃO`
```JSON
{
  "title": "New Lorem ipsum",
  "price": 80.0
}
```

#### Caso dê tudo certo, a resposta será assim:
`PATCH /api/products/1 - FORMATO DA RESPOSTA - STATUS 201`
```json
{
  "id": 1,
  "title": "New Lorem ipsum",
  "price": "80.0",
  "parent_id": 1,
  "description": "Lorem ipsum pa pa pa, Lorem ipsum pa pa pa",
  "image": "http://imagem",
  "sold": false
}
```

<h2 align="center">Excluir produto por id</h2>

`DELETE /api/products/1 - FORMATO DA REQUISIÇÃO`
```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:
`DELETE /api/products/1 - FORMATO DA RESPOSTA - STATUS 204`
```json
Sem corpo de resposta
```
# Rotas Categories
## **Rotas que não precisam de autenticação**
<h2 align="center">Obter todas as categories</h2>

`GET /api/categories - FORMATO DA REQUISIÇÃO`
```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:
`GET /api/categories - FORMATO DA RESPOSTA - STATUS 200`
```json
{
  "categories": [
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

# Rotas Parents
## **Rotas que não precisam de autenticação**
<h2 align="center">Obter todos os parents</h2>

`GET /api/parents - FORMATO DA REQUISIÇÃO`
```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:
`GET /api/parents - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"users": [
		{
			"id": 1,
			"username": "luiz-miguel90"
		},
		{
			"id": 2,
			"username": "kalmeida"
		},
		{
			"id": 3,
			"username": "ryanteixeira"
		}
	]
}
```
## **Rotas que não precisam de autenticação**
<h2 align="center">Criar novo parent(usuário)<h2>

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
  "id": 28,
  "cpf": "12312312313",
  "username": "fulano",
  "email": "fulano@mail.com",
  "name": "Fulano de Tal",
  "phone": "99999999999"
}
```
<h2 align="center">Fazer login<h2>

`POST /api/parents/login - FORMATO DA REQUISIÇÃO`
```JSON
{
  "username": "fulano",
  "password": "k3nz13",
}
```
### Obrigatórios uma identificação do usuário e seu password. Além de "username" podem ser usados "cpf" ou "email".

#### Caso dê tudo certo, a resposta será assim:
`POST /api/parents - FORMATO DA RESPOSTA - STATUS 201`
```json
{
  "id": 28,
  "cpf": "12312312313",
  "username": "fulano",
  "email": "fulano@mail.com",
  "name": "Fulano de Tal",
  "phone": "99999999999"
}
```
## **Rotas que precisam de autenticação**
<h2 align="center">Update de parent(usuário)<h2>

`POST /api/parents - FORMATO DA REQUISIÇÃO`
```JSON
{
	"password": "123456789"
}
```
### Obrigatório pelo menos um campo que queira modificar.

#### Caso dê tudo certo, a resposta será assim:
`POST /api/parents - FORMATO DA RESPOSTA - STATUS 201`
```json
{
  "id": 28,
  "cpf": "12312312313",
  "username": "fulano",
  "email": "fulano@mail.com",
  "name": "Fulano de Tal",
  "phone": "99999999999"
}
```
<h2 align="center">Deletar parent(usuário)<h2>

`GET /api/parents - FORMATO DA REQUISIÇÃO`
```
Não é necessário um corpo da requisição.

```
### Obrigatório estar logado.

#### Caso dê tudo certo, a resposta será assim:
`POST /api/parents - FORMATO DA RESPOSTA - STATUS 201`
```json
Sem corpo de resposta
```

# Rotas Questions
## **Rotas que não precisam de autenticação**
<h2 align="center">Obter todas as perguntas por id de produto</h2>

`GET /api/questions/<product_id> - FORMATO DA REQUISIÇÃO`
```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:
`GET /api/questions/1 - FORMATO DA RESPOSTA - STATUS 200`
```json
[
	{
		"id": 1,
		"question": "Teste 1",
		"parent_id": 1,
		"product_id": 1
	},
	{
		"id": 2,
		"question": "Teste 2",
		"parent_id": 1,
		"product_id": 1
	}
]
```
## **Rotas que precisam de autenticação**
<h2 align="center">Criar nova pergunta em um produto,por id de produto</h2>

`POST /api/questions/<product_id> - FORMATO DA REQUISIÇÃO`
```JSON
{
	"question": "Pergunta Teste?"
}
```

#### Caso dê tudo certo, a resposta será assim:
`POST /api/question/1 - FORMATO DA RESPOSTA - STATUS 201`
```json
{
	"id": 3,
	"question": "Pergunta Teste?",
	"product_id": 1,
	"parent_id": 1
}
```
<h2 align="center">Atualizar pergunta por id de pergunta</h2>

`PATCH /api/questions/<question_id> - FORMATO DA REQUISIÇÃO`
```JSON
{
	"question": "Pergunta Teste Atualizada?"
}
```

#### Caso dê tudo certo, a resposta será assim:
`PATCH /api/questions/3 - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"id": 3,
	"question": "Pergunta Teste Atualizada?",
	"product_id": 1,
	"parent_id": 1
}
```

<h2 align="center">Deletar pergunta por id de pergunta</h2>

`DELETE /api/questions/<question_id> - FORMATO DA REQUISIÇÃO`
```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:
`DELETE /api/questions/3 - FORMATO DA RESPOSTA - STATUS 204`
```
Sem corpo de resposta
```
