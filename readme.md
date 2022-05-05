![Captura de tela de 2022-04-27 00-08-14](https://user-images.githubusercontent.com/97132510/165432646-227a0248-12a9-4790-b366-c3d2f205ffa2.png)

<h1 align="center">API - BabyShower</h1>

<h2 align="center">Este é o backend da aplicação BabyShower - O objetivo é desenvolver uma plataforma em que os pais possam se cadastrar e interagir com outros pais que passam por fases de vida similares às suas. Nessa plataforma eles se cadastram e também cadastram produtos que não precisa mais.</h2>
<h2 align="center">Também é possível fazer uso de recursos de <strong>geolocalização</strong> para obter os pais que estão mais próximos ao usuário para que o negócio tenha mais chances de ser concretizado.</h2>

[Arquivo para o insomnia](https://drive.google.com/file/d/1Nia7ipq4zCmrQGLPfBY2ICDIZVlDih5N/view?usp=sharing)

O url base da API é [baseUrl](https://share-babyshower.herokuapp.com/api)

# Rotas Products

>**Obs.:** Alterações e deleções somente pode ser realizadas pelo parent que publicou o produto.

## **Rotas que não precisam de autenticação**

<h2 align="center">Obter todos os produtos</h2>

`GET /api/products - FORMATO DA REQUISIÇÃO`

```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:

`GET /api/products - FORMATO DA RESPOSTA - STATUS 200`

```json
[
  {
    "id": 429,
    "title": "bebê-conforto",
    "price": 350.0,
    "parent_id": 460,
    "description": "Fugiat expedita eum qui dolorem a temporibus deserunt optio veritatis eius fuga blanditiis veniam ratione recusandae placeat nam atque aliquam impedit nisi dolorum.",
    "image": "https://imagem/320x240",
    "sold": false,
    "categories": [
    	"segurança para bebê",
    	"0 a 3 meses",
    	"4 a 6 meses",
    	"7 a 9 meses",
    	"10 meses a 1 ano",
    	"2 anos"
    ],
    "city/state": "Balneário Arroio do Silva/Santa Catarina",
    "questions": "/api/questions/by_product/429"
  },
  (...)
]
```
### <u>Realizando filtros nesta rota:</u>

Podem ser realizados filtros de duas formas a seguir:
- Via **Query Params**: Para paginações utilizando **'page'(deault=1)** e/ou **'per_page' (default=8)**
- Via **Body** da requisição: 
  - Para título do produto (podendo ser parcial);
  - Para lista de categorias do produto;
  - Para preços máximos e mínimos;
  - Para cidade/estado referência para geolocalização;
  - Para latitude/longitude referência também para geolocalização;
  - Para raio de cobertura geográfica a partir do local de referência.

>**Obs.:** Essa forma de paginar resultados via query params também pode ser utilizada nas rotas para *obter todos os parents(usuários)* ou para *obter todas as perguntas por id de produto*.

**Via Query Params sem body na requisição:**

`GET /api/products?perPage=2&page=1 - FORMATO DA REQUISIÇÃO`

Caso dê tudo certo, a resposta será assim:

`GET /api/products?perPage=2&page=1 - FORMATO DA RESPOSTA - STATUS 200`

```json
[
  {
    "id": 317,
    "title": "Nanina",
    "price": 15.0,
    "parent_id": 339,
    "description": "Ab in neque earum odio quia molestias minima eaque ratione eos illum.",
    "image": "https://imagem/320x240",
    "sold": false,
    "categories": [
    	"brinquedos"
    ],
    "city/state": "Araranguá/Santa Catarina",
    "questions": "/api/questions/by_product/317"
  },
  {
  	"id": 360,
  	"title": "body tamanho M",
  	"price": 36.0,
  	(...)
  }
]
```

**Via Body na na requisição:**

>**Obs.:** Pode ter query params para a paginação em conjunto.

`GET /api/products?page=1&per_page=3 - FORMATO DA REQUISIÇÃO`

```json
{
  "categories": ["roupas", "0 a 3 meses"],
  "min_price": 30.0,
  "max_price": 60.0,
  "title_product": "",
  "city": "Cocal do Sul",
  "state": "Santa catar",
  "distance": 50000
}
```
>**Obs.:** Para categories, title_product, city e state é busca é por aproximação. Exemplo: Pode-se buscar "Santa Catarina" como "santa c" ou "catarina" na informação state.

`GET /api/products?page=1&per_page=3 - FORMATO DA RESPOSTA - STATUS 200`

```json
[
	{
		"id": 2780,
		"title": "Tênis tam 16",
		"price": 36.0,
		"parent_id": 2987,
		"description": "Accusamus nisi aspernatur nulla fuga enim velit quibusdam maxime voluptates vitae mollitia dolorum dolorum.",
		"image": "https://imagem/320x240",
		"sold": false,
		"categories": [
			"roupas",
			"0 a 3 meses"
		],
		"city/state": "Meleiro/Santa Catarina",
		"questions": "/api/questions/by_product/2780"
	},
  (...)
]
```

<h2 align="center">Outras informações sobre a geolocalização</h2>

Sobre a rota anterior, caso seja fornecido o **Token Bearer** no head da requisição a localização de referência para o raio de alcance da pesquisa serão a cidade e o estado no cadastro do usuário. Caso o usuário não esteja autenticado, ou não seja fornecido o token a pesquisa não considerará aspectos geográficos.

Como mencionado anteriormente, podem ser fornecidos no body da requisição como referência para o raio de alcance:
- Cidade E estado; OU
- Latitude E Longitude
  
### Raio de alcance:

O raio de alcance quando não fornecido possui o valor padrão de 50 mil km. Deve-se utilizar a chave "distance" no body da requisição.

>**Obs.:**: Esta área de cobertura só será utilizada se houver um ponto de referênica obtido pelos dados do usuário ou pelo body da requisição.

<h2 align="center">Obter produto por id</h2>

`GET /api/products/<product_id> - FORMATO DA REQUISIÇÃO`

```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:

`GET /api/products/2 - FORMATO DA RESPOSTA - STATUS 200`

```json
{
  "id": 2,
  "title": "Nanina",
  "price": 15.0,
  "parent_id": 2,
  "description": "Repellat deserunt eum necessitatibus nam consequuntur vero harum asperiores excepturi tenetur voluptatem voluptate commodi ratione suscipit quibusdam quibusdam quas illo atque incidunt commodi.",
  "image": "https://imagem/320x240",
  "sold": false,
  "categories": [
  	"brinquedos"
  ],
  "city/state": "Abadia dos Dourados/Minas Gerais",
  "questions": "/api/questions/by_product/2"
}
```

<h2 align="center">Obter produto pelo id do parent</h2>

`GET /api/products/by_parent/<parent_id> - FORMATO DA REQUISIÇÃO`

```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:

`GET /api/products/by_parent/2 - FORMATO DA RESPOSTA - STATUS 200`

```json
{
  "products": [
  	{
  	  "id": 2,
  	  "title": "Nanina",
  	  "price": 15.0,
  	  "parent_id": 2,
  	  "description": "Repellat deserunt eum necessitatibus nam consequuntur vero harum asperiores excepturi tenetur voluptatem voluptate commodi ratione suscipit quibusdam quibusdam quas illo atque incidunt commodi.",
  	  "image": "https://imagem/320x240",
  	  "sold": false,
  	  "categories": [
  	  	"brinquedos"
  	  ],
  	  "city/state": "Abadia dos Dourados/Minas Gerais",
  	  "questions": "/api/questions/by_product/2"
  	},
  (...)
  ]
}
```

## **Rotas que precisam de autenticação**

<h2 align="center">Criar novo produto</h2>

`POST /api/products - FORMATO DA REQUISIÇÃO`

```JSON
{
	"title": "tiptop",
	"description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
	"price": 610.69,
	"image": "https://imagem/320x240",
	"categories": ["0 a 3 meses", "roupas"]
}
```

#### Caso dê tudo certo, a resposta será assim:

`POST /api/products - FORMATO DA RESPOSTA - STATUS 201`

```json

{
	"id": 5542,
	"title": "tiptop",
	"price": 610.69,
	"parent_id": 5542,
	"description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
	"image": "https://imagem/320x240",
	"sold": false,
	"categories": [
		"0 a 3 meses",
		"roupas"
	],
	"city/state": "Cocal do Sul/Santa Catarina",
	"questions": "/api/questions/by_product/5542"
}
```
>**Obs.:** Quando o parent cadastra um novo produto, um email de confirmação é enviado para o seu respectivo email cadastrado.

>**Obs.:** Um produto pode ser criado sem categoria. A categoria é buscada pela palavra aproximada na relação de categories desta api. Ao se inserir uma categoria não existente se obterá o seguinte erro:

`POST /api/products - FORMATO DA RESPOSTA - STATUS 422`

```json

{
  "error": "Categories is invalid",
  "invalid_options": [
  	"teste"
  ],
  "valid_options": "api/categories"
}
```

<h2 align="center">Atualizar produto por id</h2>

`PATCH /api/products/<product_id> - FORMATO DA REQUISIÇÃO`

```JSON
{
  "price": 52.0,
  "categories": ["4 a 6 meses"]
}
```

#### Caso dê tudo certo, a resposta será assim:

`PATCH /api/products/5542 - FORMATO DA RESPOSTA - STATUS 201`

```json
{
  "id": 5542,
  "title": "tiptop",
  "price": 52.0,
  "parent_id": 5542,
  "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
  "image": "https://imagem/320x240",
  "sold": false,
  "categories": [
  	"4 a 6 meses"
  ],
  "city/state": "Cocal do Sul/Santa Catarina",
  "questions": "/api/questions/by_product/5542"
}
```

<h2 align="center">Excluir produto por id</h2>

`DELETE /api/products/<product_id> - FORMATO DA REQUISIÇÃO`

```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:

`DELETE /api/products/1 - FORMATO DA RESPOSTA - STATUS 204`

```json
Sem corpo de resposta
```

# Rota Categories

## **Rota não precisa de autenticação**

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

# Rotas Questions

>**Obs.:** Todos os parents podem fazer perguntas em quaisquer outros produtos. Inclusive nos próprios produtos.

## **Rotas que não precisam de autenticação**

<h2 align="center">Obter todas as perguntas por id de produto</h2>

`GET /api/questions/by_product/<product_id> - FORMATO DA REQUISIÇÃO`

```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:

`GET /api/questions/by_product/3001 - FORMATO DA RESPOSTA - STATUS 200`

```json
[
  {
		"id": 3001,
		"question": "teste",
		"created_at": "Wed, 04 May 2022 21:12:02 GMT",
		"updated_at": null,
		"product_id": 301,
		"parent_id": 20,
		"answer": {
			"link": "/api/answers/1",
			"username": "fdddgd5dfd",
			"answer": "teste2"
		},
		"username": "miguel83"
	},
  (...)
]
```

## **Rotas que precisam de autenticação**

<h2 align="center">Criar nova pergunta em um produto por id de produto</h2>

`POST /api/questions/<product_id> - FORMATO DA REQUISIÇÃO`

```JSON
{
	"question": "Pergunta Teste?"
}
```

#### Caso dê tudo certo, a resposta será assim:

`POST /api/question/3 - FORMATO DA RESPOSTA - STATUS 201`

```json
{
	"id": 3,
	"question": "Pergunta teste?",
	"created_at": "Thu, 05 May 2022 15:41:42 GMT",
	"updated_at": null,
	"product_id": 1,
	"parent_id": 5542,
	"answer": null
}
```
>**Obs.:** É enviado uma mensagem para o e-mail do dono do produto o alertado sobre a nova pergunta enviado uma pergunta.

<h2 align="center">Atualizar pergunta por id de pergunta</h2>

`PATCH /api/questions/<question_id> - FORMATO DA REQUISIÇÃO`

```JSON
{
	"question": "Pergunta Teste Atualizada?"
}
```

#### Caso dê tudo certo, a resposta será assim:

`PATCH /api/questions/1 - FORMATO DA RESPOSTA - STATUS 200`

```json
{
	"id": 1,
	"question": "Pergunta teste atualizada?",
	"created_at": "Thu, 05 May 2022 10:29:22 GMT",
	"updated_at": "Thu, 05 May 2022 15:43:48 GMT",
	"product_id": 1,
	"parent_id": 5542,
	"answer": null
}
```

<h2 align="center">Deletar pergunta por id de pergunta</h2>

`DELETE /api/questions/<question_id> - FORMATO DA REQUISIÇÃO`

```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:

`DELETE /api/questions/1 - FORMATO DA RESPOSTA - STATUS 204`

```
Sem corpo de resposta
```

# Rotas Answers

>**Obs.:** Somente o parent que postou o produto pode responder as perguntas que estiverem vinculadas ao seu produto.

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
	"created_at": "Wed, 04 May 2022 21:13:16 GMT",
	"updated_at": null,
	"parent_id": 19,
	"question": {
		"link": "/api/questions/by_product/3001",
		"question": "Pergunta Teste Atualizada?",
		"username": "Rita231"
	}
}
```
>**Obs.:** É enviado uma mensagem para o e-mail do parent que fez a pergunta o alertado sobre a resposta.

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
	"created_at": "Wed, 04 May 2022 21:13:16 GMT",
	"updated_at": "Wed, 04 May 2022 21:16:26 GMT",
	"parent_id": 19,
	"question": {
		"link": "/api/questions/by_product/3001",
		"question": "Pergunta Teste Atualizada?",
		"username": "Rita231"
	}
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
# Rotas Parents
>**Obs.:** Rotas de obtenção de dados, deleção e atualização só podem ser realizadas pelo próprio usuário.
## **Rotas que não precisam de autenticação**

<h2 align="center">Obter todos os parents(usernames)</h2>

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

<h2 align="center">Criar novo parent(usuário)<h2>

`POST /api/parents - FORMATO DA REQUISIÇÃO`

```JSON
{
	"cpf": "12345678910",
	"username": "marcos2345",
	"name": "Marcos",
	"email": ",marcos@yahoo.com.br",
	"password": "123456",
	"phone": "(21) 99999-9999",
	"city": "Cocal do s",
	"state": "Santa Catarina"
}
```

#### Caso dê tudo certo, a resposta será assim:

`POST /api/parents - FORMATO DA RESPOSTA - STATUS 201`

```json
{
	"cpf": "12345678910",
	"username": "marcos2345",
	"name": "Marcos",
	"email": ",marcos@yahoo.com.br",
	"password": "123456",
	"phone": "(21) 99999-9999",
	"city/state": "Cocal do Sul/SC"
}
```
>**Obs:** Esta api não permite cpf, username ou email repetidos entre os usuários.

<h2 align="center">Fazer login<h2>

`POST /api/parents/login - FORMATO DA REQUISIÇÃO`

```JSON
{
  "username": "fulano",
  "password": "k3nz13",
}
```

>**Obs:** Obrigatórios uma identificação do usuário e seu password. Além de "username" podem ser usados "cpf" ou "email".

#### Caso dê tudo certo, a resposta será assim:

`POST /api/parents - FORMATO DA RESPOSTA - STATUS 201`

```json
{
	"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MTc3OTAxNywianRpIjoiOWJmOGM2M2QtNmFkYS00YTM1LTkxNDItY2FhNmU1NGIwYWM0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6NTU0MiwidXNlcm5hbWUiOiJkX3NhdGlybzMifSwibmJmIjoxNjUxNzc5MDE3LCJleHAiOjE2NTE3Nzk5MTd9.DT8dcAjeSQnzsEw9DqImwqfF3Nm3Q8YIiLuFUTZ72JE"
}
```
>**Obs.:** É possível obter o id do usuário através do JWT. Token expira em 15 minutos.

## **Rotas que precisam de autenticação**

<h2 align="center">Update de parent(usuário)<h2>

`POST /api/parents - FORMATO DA REQUISIÇÃO`

```JSON
{
	"password": "123456789"
}
```

>**Obs.:** Obrigatório pelo menos um campo que queira modificar.

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

>**Obs.:** Obrigatório estar logado. **Atenção!** Trata-se de uma deleção em cascata e todos os produtos, perguntas e respostas, inclusive interações em chats serão deletados.

#### Caso dê tudo certo, a resposta será assim:

`POST /api/parents - FORMATO DA RESPOSTA - STATUS 201`

```json
Sem corpo de resposta
```
# Rotas Cities
>**Obs.:** Nesta rota além de query params para paginações ('page'-> deault=1 e/ou 'per_page' -> default=8). Podem ser utilizados "city" e "state" para filtrar os resultados.
#### Caso dê tudo certo, a resposta será assim:

`GET /api/cities?state=Santa Catarina - FORMATO DA RESPOSTA - STATUS 200`

```json
{
	"cities": [
		{
			"point_id": 1786,
			"capital": true,
			"uf": "SC",
			"longitude": -48.5477,
			"code_uf": 42,
			"code_ibge": 4205407,
			"city": "Florianópolis",
			"state": "Santa Catarina",
			"latitude": -27.5945
		},
		{
			"point_id": 43,
			"capital": false,
			"uf": "SC",
			"longitude": -49.822,
			"code_uf": 42,
			"code_ibge": 4200200,
			"city": "Agrolândia",
			"state": "Santa Catarina",
			"latitude": -27.4087
		},
		(...)
```
## **Rota não precisa de autenticação**

<h2 align="center">Obter todos os parents(usernames)</h2>

`GET /api/cities?state=<estado>&city=<cidade> - FORMATO DA REQUISIÇÃO`


# Rotas Chat

<h2 align="center">Ver todas conversas já iniciadas</h2>

`GET /api/chat - FORMATO DA REQUISIÇÃO`
```
Não é necessário um corpo da requisição.
```

>**Obs:** Rota mostra apenas as conversas ligadas ao usuário logado.

#### Caso dê tudo certo, a resposta será assim:

>**Obs:** Propriedade "read" mostra se a mensagem já foi lida.

`GET /api/chat - FORMATO DA RESPOSTA - STATUS 200`
```json
{
  "chats": [
    {
      "other_parent_id": 1,
      "messages": "chat/1",
      "read": true
    },
    {
      "other_parent_id": 2,
      "messages": "chat/2",
      "read": true
    }
  ]
}
```
<h2 align="center">Enviar uma mensagem</h2>

`POST /api/chat/<parent_id> - FORMATO DA REQUISIÇÃO`

```
Apenas necessário a mensagem no corpo de requisição.
```

>**Obs:** Usuário precisa estar logado para enviar a mensagem.

```json
{
  "message": "Boa noite, vi seu anuncio do site. Será que podemos conversar melhor sobre o envio?"
}
```

>**Obs:** Precisa passar id do parent logado ou de um outro parent existente.

#### Caso dê tudo certo, a resposta será assim:

`POST /api/chat/2 - FORMATO DA RESPOSTA - STATUS 201`
```json
{
  "msg": "Mensagem enviada com sucesso!"
}
```

<h2 align="center">Ver a conversa de um chat específico</h2>

`GET /api/chat/<parent_id> - FORMATO DA REQUISIÇÃO`
```
Não é necessário um corpo da requisição.
```

#### Caso dê tudo certo, a resposta será assim:

`GET /api/chat/2 - FORMATO DA RESPOSTA - STATUS 200`

>**Obs 1 :** propriedade "msg_read" mostra se o usuário já leu a mensagem.
>**Obs 2 :** propriedade "parent" mostra a quem se destina a mensagem enviada

```json
{
  "messages": [
    {
      "data": "Thu, 05 May 2022 19:20:28 GMT",
      "message": "Boa noite, vi seu anuncio do site. Será que podemos conversar melhor sobre o envio?",
      "msg_read": false,
      "parent": "Hirton Santos"
    }
  ]
}
```