from fastapi import Body, FastAPI
import data_handler 
import json
from typing import Any

api = FastAPI()

# Para rodar a API usar:  uvicorn main:api --reload

@api.get("/")
def read_root():
    return {"Hello": "World"}

@api.get("/hello-world")
def hello_world():
    return {'message': 'Hello World!'}

@api.get("/get-titanic-data")
def get_titanic_data():
    dados = data_handler.load_data()
    # Cada registro, vai trazer o nome da coluna e atributo para todos eles
    json = dados.to_json(orient='records')
    return json

@api.post("/save-prediction")
def save_prediction(passageiro: Any = Body(None)):
    passageiro_obj = json.loads(passageiro)
    result = data_handler.save_prediction(passageiro_obj)
    return result

@api.get("/get-all-predictions")
def get_all_predictions():
    predictions = data_handler.get_all_predictions()
    return predictions


@api.post("/predict")
def predict(passageiro: Any = Body(None)):
    passageiro_obj = json.loads(passageiro)
    result = data_handler.survival_predict(passageiro_obj)
    return result

