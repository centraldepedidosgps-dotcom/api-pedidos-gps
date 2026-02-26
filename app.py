from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = "pedidos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return "API PEDIDOS GPS ONLINE 🔥"


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({"mensagem": "Upload realizado com sucesso!"})


@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    arquivos = os.listdir(UPLOAD_FOLDER)
    return jsonify(arquivos)


@app.route("/download/<nome_arquivo>", methods=["GET"])
def baixar_pedido(nome_arquivo):
    return send_from_directory(UPLOAD_FOLDER, nome_arquivo, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
