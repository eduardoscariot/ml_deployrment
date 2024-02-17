import requests

# Teste 1
response = requests.get("http://127.0.0.1:8000/hello-world")
print(response)

if response.status_code == 200:
    response_data = response.json()
    print(f"Teste 01 - OK. Response: {response_data}")
else:
    print(f"Falha na requisição do Teste 01: {response.status_code}")