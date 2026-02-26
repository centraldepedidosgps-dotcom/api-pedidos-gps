from flask import Flask, request, jsonify, send_from_directory
import os
from functools import wraps

app = Flask(__name__)

UPLOAD_FOLDER = "pedidos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔐 Login fixo da API
USUARIO = "admin"
SENHA = "1234"

def verificar_auth(username, password):
    return username == USUARIO and password == SENHA

def autenticar():
    return jsonify({"erro": "Acesso não autorizado"}), 401

def requer_autenticacao(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not verificar_auth(auth.username, auth.password):
            return autenticar()
        return f(*args, **kwargs)
    return decorated


@app.route("/")
def home():
    return "API PEDIDOS GPS ONLINE 🔥"


@app.route("/upload", methods=["POST"])
@requer_autenticacao
def upload():
    if "file" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({"mensagem": "Upload realizado com sucesso!"})


@app.route("/pedidos", methods=["GET"])
@requer_autenticacao
def listar_pedidos():
    arquivos = os.listdir(UPLOAD_FOLDER)
    return jsonify(arquivos)


@app.route("/download/<nome_arquivo>", methods=["GET"])
@requer_autenticacao
def baixar_pedido(nome_arquivo):
    return send_from_directory(UPLOAD_FOLDER, nome_arquivo, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
