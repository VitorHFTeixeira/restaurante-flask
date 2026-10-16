# Restaurante Flask · Cardápio e Comanda
projeto realizado no 1 semestre de engenharia de software

Sistema de cardápio para restaurante com interface web em vermelho e preto, feito em **Python (Flask)**, HTML, CSS e JavaScript. Ele reproduz todas as funções de um programa de terminal original e guarda os produtos em um arquivo de texto (`cardapio.txt`).

## Funcionalidades

**Menu inicial**
- Escolha entre Administrador, Operador ou Sair (também funciona com as teclas `1`, `2` e `0`).

**Administrador**
- Cadastrar produto, com código gerado automaticamente (começa em 100 e reaproveita o primeiro código livre).
- Listar os produtos cadastrados.
- Alterar nome e valor de um produto.
- Apagar produto, com confirmação.

**Operador**
- Montar o pedido tocando nos produtos ou digitando o código.
- Comanda com quantidade, total e botões para somar ou remover itens.
- Resumo final do pedido ("Pedidos do cliente") e mensagem de agradecimento.

## Estrutura do projeto

```
Restaurante_Flask/
├── servidor.py          # servidor Flask e API dos produtos
├── app.py               # versão original do programa, para o terminal
├── cardapio.txt         # produtos (codigo;descricao;valor)
├── requirements.txt     # dependências
└── static/
    ├── index.html       # página da interface
    ├── css/
    │   └── style.css    # estilos
    └── js/
        └── app.js       # lógica da interface
```

## Como executar

Pré-requisito: [Python 3](https://www.python.org/downloads/) instalado.

1. Clone o repositório:
   ```
   git clone https://github.com/VitorHFTeixeira/restaurante-flask.git
   cd restaurante-flask
   ```
2. Instale o Flask:
   ```
   pip install -r requirements.txt
   ```
3. Inicie o servidor:
   ```
   python servidor.py
   ```
4. Abra o endereço mostrado no terminal, normalmente `http://127.0.0.1:5000`.

Para usar a versão de terminal, rode `python app.py`.

## API

| Método | Rota | Função |
|---|---|---|
| GET | `/api/produtos` | Lista os produtos |
| POST | `/api/produtos` | Cadastra um produto (`{"n": "nome", "v": "12.50"}`) |
| PUT | `/api/produtos/<codigo>` | Altera nome e valor |
| DELETE | `/api/produtos/<codigo>` | Apaga o produto |

## Formato do `cardapio.txt`

Uma linha por produto, separada por ponto e vírgula:

```
100;Pastel de carne;9.50
101;X-Burguer da casa;24.90
```

## Tecnologias

- Python e Flask
- HTML, CSS e JavaScript puros, sem frameworks

## Autor

Feito por [VitorHFTeixeira](https://github.com/VitorHFTeixeira).
