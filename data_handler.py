import pandas as pd
import json

def load_data():
    dados = pd.read_csv('./data/titanic.csv')
    return dados

def get_all_predictions():
    data = None
    with open('predictions.json', 'r') as f:
        data = json.load(f)
        
    return data

def save_prediction(passageiro):
    data = get_all_predictions()
    data.append(passageiro)
    with open('predictions.json', 'w') as f:
        json.dump(data, f)
        


