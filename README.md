# Rodar no PowerShell Como Adm e executar:
Set-ExecutionPolicy Unrestricted

# Para iniciar o ambiente virtual
venv\Scripts\Activate.ps1

# Para rodar o Streamlit com um exemplo da biblioteca
python -m streamlit hello

# Para rodar um arquivo local do computador
streamlit run .\app.py

