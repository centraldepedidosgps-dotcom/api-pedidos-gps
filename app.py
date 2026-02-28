from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from functools import wraps
import os

app = Flask(__name__)
CORS(app)  # <--- permite requisições de qualquer origem (navegador)

UPLOAD_FOLDER = "pedidos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================
# CONFIG LOGIN (igual cliente)
# ==========================
API_USER = "admin"
API_PASS = "1234"

# ==========================
# AUTENTICAÇÃO BASIC
# ==========================
def check_auth(username, password):
    return username == API_USER and password == API_PASS

def authenticate():
    return jsonify({"erro": "Autenticação necessária"}), 401

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# ==========================
# ROTAS
# ==========================
@app.route("/")
def home():
    return "API PEDIDOS GPS ONLINE 🔥"

@app.route("/upload", methods=["POST"])
@requires_auth
def upload():
    if "file" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"erro": "Nome de arquivo inválido"}), 400

    caminho = os.path.join(UPLOAD_FOLDER, file.filename)

    if os.path.exists(caminho):
        return jsonify({"erro": "Arquivo já existe"}), 400

    try:
        file.save(caminho)
        return jsonify({"mensagem": "Upload realizado com sucesso!"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/pedidos", methods=["GET"])
@requires_auth
def listar_pedidos():
    try:
        arquivos = os.listdir(UPLOAD_FOLDER)
        arquivos_pdf = [f for f in arquivos if f.endswith(".pdf")]
        return jsonify(arquivos_pdf)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/download/<nome_arquivo>", methods=["GET"])
@requires_auth
def baixar_pedido(nome_arquivo):
    try:
        caminho = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        if not os.path.exists(caminho):
            return jsonify({"erro": "Arquivo não encontrado"}), 404
        return send_from_directory(
            UPLOAD_FOLDER,
            nome_arquivo,
            as_attachment=True
        )
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ==========================
# EXECUÇÃO
# ==========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
