@echo off

echo Criando ambiente virtual...
python -m venv env

echo Ativando o ambiente virtual...
call env\Scripts\activate

echo Instalando as dependências...
pip install streamlit

echo Executando o servidor Streamlit...
start streamlit run assistant.py

echo Abrindo a página da web...
start "" "http://localhost:8501"

pause
