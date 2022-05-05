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
			"id": 1,
			"title": "body tamanho M",
			"price": "36.0",
			"parent_id": 4,
			"description": "Lorem (...) book.",
			"image": "https://imagem/320x240",
			"sold": false,
			"categories": [
				"roupas"
			],
			"questions": "/api/questions/1"
		},
		(...)
	]
}
```
### <u>Realizando filtros nesta rota:</u>

Podem ser realizados filtros de duas formas a seguir:
- Via Query Params: Para paginações utilizando **'page'(deault=1)** e/ou **'per_page' (default=8)**
- Via Body da requisição: 
  - Para título do produto (podendo ser parcial);
  - Para lista de categorias do produto;
  - Para preços;
  - Para cidade/estado referência para geolocalização;
  - Para latitude/longitude referência também para geolocalização;
  - Para raio de cobertura geográfica a partir do local de referência.


> **Via Query Params sem body na requisição:**
>
`GET /api/products?perPage=3&page=1&price=100.0 - FORMATO DA REQUISIÇÃO`

Caso dê tudo certo, a resposta será assim:

`GET /api/products?perPage=3&page=1&price=100.0 - FORMATO DA RESPOSTA - STATUS 200`

```json
{
	"products": [
		{
			"id": 1,
			"title": "body tamanho M",
			"price": "36.0",
			"parent_id": 4,
			"description": "Lorem (...) book.",
			"image": "https://imagem/320x240",
			"sold": false,
			"categories": [
				"roupas"
			],
			"questions": "/api/questions/1"
		},
		{
			"id": 2,
			"title": "babá eletrônica",
			"price": "250.0",
			"parent_id": 5,
			"description": "Lorem (...) book.",
			"image": "https://imagem/320x240",
			"sold": false,
			"categories": [
				"0 a 3 meses",
				"4 a 6 meses",
				"7 a 9 meses",
				"10 meses a 1 ano",
				"2 anos",
				"3 a 5 anos",
				"segurança para bebê"
			],
			"questions": "/api/questions/2"
		},
		{
			"id": 3,
			"title": "berço",
			"price": "560.0",
			"parent_id": 10,
			"description": "Lorem (...) book.",
			"image": "https://imagem/320x240",
			"sold": false,
			"categories": [
				"0 a 3 meses",
				"4 a 6 meses",
				"7 a 9 meses",
				"10 meses a 1 ano",
				"2 anos",
				"3 a 5 anos",
				"quarto do bebê"
			],
			"questions": "/api/questions/3"
		}
	]
}
```

> **Via Body na na requisição:**

**Observação:** Poderia ter query params para a paginação em conjunto.

`GET /api/products - FORMATO DA REQUISIÇÃO`

```json
{
	"categories": ["roupas", "0 a 3 meses"],
	"min_price": 30.0,
	"max_price": 60.0,
	"title_product": "",
	"city": "Cocal do Sul",
	"state": "SC",
  "radius": 50000
}
```

`GET /api/products - FORMATO DA RESPOSTA - STATUS 200`

```json
{
	"products": [
		{
			"id": 9,
			"title": "Tênis tam 16",
			"price": "36.0",
			"parent_id": 10,
			"description": "Lorem (...) book.",
			"image": "https://imagem/320x240",
			"sold": false,
			"categories": [
				"0 a 3 meses",
				"roupas"
			],
			"questions": "/api/questions/9"
		}
	]
}
```

<h2 align="center">Outras informações sobre a geolocalização</h2>

Sobre a rota anterior, caso seja fornecido o **Token Bearer** no head da requisição a localização de referência para o raio de alcance da pesquisa serão a cidade e o estado no cadastro do usuário. Caso o usuário não esteja autenticado, ou não seja fornecido o token a pesquisa não considerará aspectos geográficos.

Como mencionado anteriormente, podem ser fornecidos no body da requisição como referência para o raio de alcance:
- Cidade E estado; OU
- Latitude e Longitude
  
### Raio de alcance:

O raio de alcance quando não fornecido possui o valor padrão de 50 mil km.

**Importante**: Esta área de cobertura só será utilizada se houver um ponto de referênica obtido pelos dados do usuário ou pelo body da requisição.

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

# Rotas Answers

## **Rotas que precisam de autenticação**

<h2 align="center">Criar uma resposta</h2>

`POST /api/answers/<question_id> - FORMATO DA REQUISIÇÃO`

```JSON
{
  "answer": "Resposta Teste!"
}
```

#### Caso tudo dê certo, a resposta será assim:

`POST /api/answers/1 - FORMATO DA RESPOSTA - STATUS 201`

```JSON
{
  "id": 1,
  "answer": "Resposta Teste!",
  "parent_id": 1,
  "question_id": 1
}
```

<h2 align="center">Editar uma resposta</h2>

`PATCH /api/answers/<answer_id> - FORMATO DA REQUISIÇÃO`

```JSON
{
  "answer": "Resposta Teste Editada!"
}
```

#### Caso tudo dê certo, a resposta será assim:

`PATCH /api/answers/1 - FORMATO DA RESPOSTA - STATUS 200`

```JSON
{
  "id": 1,
  "answer": "Resposta Teste Editada!",
  "parent_id": 1,
  "question_id": 1
}
```

<h2 align="center">Deletar uma resposta</h2>

`DELETE /api/answers/<answer_id> - FORMATO DA REQUISIÇÃO`

```JSON
Não é necessário um corpo da requisição.
```

#### Caso tudo dê certo, a resposta será assim:

`DELETE /api/answers/1 - FORMATO DA RESPOSTA - STATUS 204`

```JSON
Sem corpo de resposta.
```

## **Rotas que não precisam de autenticação**

<h2 align="center">Obter uma resposta</h2>

`GET /api/answers/<answer_id> - FORMATO DA REQUISIÇÃO`

```JSON
Não é necessário um corpo da requisição.
```

#### Caso tudo dê certo, a resposta será assim:

`GET /api/answers/1 - FORMATO DA RESPOSTA - STATUS 200`

```JSON
{
  "id": 1,
  "answer": "Resposta Teste Editada!",
  "parent_id": 1,
  "question_id": 1
}
```
