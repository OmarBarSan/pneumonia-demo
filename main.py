from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np

from modelo.model import create_model, make_prediction

path = "pesos/model.h5"
model = create_model(path)
app = FastAPI()


@app.post('/predict')
async def predict(file: UploadFile = File(...)) -> dict:
    if file.content_type.startswith('image/'):
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image = np.array(image)
        results = make_prediction(model, image)

        return JSONResponse(content={'results': results})
    else:
        return JSONResponse(content={'error': 'El archivo no es una imagen'}, status_code=400)

@app.post('/predict-bytes')
def predict_bytes(data: bytes = File(...)) -> dict:
    print(f"data {data}")
    if data.startswith('image/'):
        image = Image.open(io.BytesIO(data))
        image = np.array(image)
        results = make_prediction(model, image)

        return JSONResponse(content={'results': results})
    else:
        return JSONResponse(content={'error': 'El archivo no es una imagen'}, status_code=400)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )