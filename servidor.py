import os
import re
from flask import Flask, jsonify, request, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(BASE, "cardapio.txt")   # formato: codigo;descricao;valor
app = Flask(__name__, static_folder="static")


def ler():
    if not os.path.exists(ARQUIVO):
        open(ARQUIVO, "a+", encoding="utf-8").close()
    produtos = []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split(";")
            if len(partes) == 3 and partes[0].isdigit():
                produtos.append({"c": int(partes[0]), "n": partes[1], "v": partes[2]})
    return sorted(produtos, key=lambda p: p["c"])


def gravar(produtos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        for p in sorted(produtos, key=lambda p: p["c"]):
            f.write(f'{p["c"]};{p["n"]};{p["v"]}\n')


def cod_bruto(produtos):
    usados = {p["c"] for p in produtos}
    codigo = 100
    while codigo in usados:
        codigo += 1
    return codigo


def validar(dados):
    nome = str(dados.get("n", "")).replace(";", " ").strip()
    valor = str(dados.get("v", "")).strip().replace(",", ".")
    if not nome:
        return None, "Informe o nome do produto."
    if not re.fullmatch(r"\d+(\.\d{1,2})?", valor):
        return None, "Informe um valor em números, como 12,50."
    return (nome, f"{float(valor):.2f}"), None


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.get("/api/produtos")
def listar():
    return jsonify(ler())


@app.post("/api/produtos")
def cadastrar():
    ok, erro = validar(request.get_json(force=True))
    if erro:
        return jsonify({"erro": erro}), 400
    produtos = ler()
    novo = {"c": cod_bruto(produtos), "n": ok[0], "v": ok[1]}
    produtos.append(novo)
    gravar(produtos)
    return jsonify(novo), 201


@app.put("/api/produtos/<int:cod>")
def alterar(cod):
    ok, erro = validar(request.get_json(force=True))
    if erro:
        return jsonify({"erro": erro}), 400
    produtos = ler()
    for p in produtos:
        if p["c"] == cod:
            p["n"], p["v"] = ok
            gravar(produtos)
            return jsonify(p)
    return jsonify({"erro": "Código não encontrado."}), 404


@app.delete("/api/produtos/<int:cod>")
def excluir(cod):
    produtos = ler()
    restantes = [p for p in produtos if p["c"] != cod]
    if len(restantes) == len(produtos):
        return jsonify({"erro": "Código não encontrado."}), 404
    gravar(restantes)
    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)