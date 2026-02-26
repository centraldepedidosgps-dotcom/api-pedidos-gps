from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os

app = FastAPI()

UPLOAD_FOLDER = "uploads"

# Garante que a pasta existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.delete("/zerar")
def zerar_pedidos():
    try:
        arquivos_removidos = 0

        for arquivo in os.listdir(UPLOAD_FOLDER):
            caminho = os.path.join(UPLOAD_FOLDER, arquivo)
            if os.path.isfile(caminho):
                os.remove(caminho)
                arquivos_removidos += 1

        return JSONResponse(
            content={
                "message": "Pedidos apagados com sucesso.",
                "arquivos_removidos": arquivos_removidos
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
