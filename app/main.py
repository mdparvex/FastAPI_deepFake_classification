from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
import os
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tensorflow.keras.models import load_model
from .utils import allowed_file, model_predict

origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR , 'model.h5'))

#app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.post('/predict/')
async def predict(file: UploadFile = File(...)):

    if file and allowed_file(file.filename):

        prediction, confidence, result = model_predict(file , model)
        predictions = {
                      "prediction": prediction,
                      "confidence": confidence
                }
        
        return JSONResponse(content={
            "filename": file.filename,
            "predictions": predictions,
            "message": "File uploaded successfully"
        })

    else:
        return JSONResponse(
            status_code=400,
            content={"message": "Please upload images of jpg, jpeg, or png extension only"}
        )
