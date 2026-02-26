from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "Nenhum arquivo enviado", 400

    file = request.files["file"]

    if file.filename == "":
        return "Nome de arquivo inválido", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    return "Upload realizado com sucesso!", 200


@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    arquivos = os.listdir(UPLOAD_FOLDER)
    return jsonify(arquivos)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
