import sqlite3
import streamlit as st
import random
import json

# Função para ensinar o assistente
def teach_assistant(question, answer):
    conn = sqlite3.connect("assistant_db.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS conversations (question TEXT, answer TEXT)")
    cursor.execute("SELECT answer FROM conversations WHERE question LIKE ?", ('%' + question + '%',))
    result = cursor.fetchone()

    if result:
        # A pergunta já existe no banco de dados, adicione a nova resposta à lista de respostas
        answers = json.loads(result[0])
        answers.append(answer)
        cursor.execute("UPDATE conversations SET answer = ? WHERE question LIKE ?", (json.dumps(answers), '%' + question + '%'))
    else:
        # A pergunta não existe no banco de dados, insira uma nova linha com a pergunta e a resposta
        cursor.execute("INSERT INTO conversations VALUES (?, ?)", (question, json.dumps([answer])))

    conn.commit()
    conn.close()
    st.success("Assistente ensinado com sucesso!")

# Função para buscar a resposta do assistente no banco de dados
def get_answer(question):
    conn = sqlite3.connect("assistant_db.db")
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM conversations WHERE question LIKE ?", ('%' + question + '%',))
    result = cursor.fetchone()
    conn.close()

    if result and result[0]:
        # Escolha uma resposta aleatória das respostas possíveis
        answers = json.loads(result[0])
        return random.choice(answers)
    else:
        return "Desculpe, não tenho uma resposta para isso."

# Função para editar uma entrada
def edit_entry(question, new_question, new_answer):
    conn = sqlite3.connect("assistant_db.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE conversations SET question = ?, answer = ? WHERE question LIKE ?", (new_question, json.dumps([new_answer]), '%' + question + '%'))
    conn.commit()
    conn.close()
    st.success("Entrada editada com sucesso!")

# Função para deletar uma entrada
def delete_entry(question):
    conn = sqlite3.connect("assistant_db.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM conversations WHERE question LIKE ?", ('%' + question + '%',))
    conn.commit()
    conn.close()
    st.success("Entrada deletada com sucesso!")

def main():
    mode = st.sidebar.selectbox("Escolha um modo", ("Conversar", "Ensinar", "Editar", "Deletar"), index=0)

    if mode == "Ensinar":
        st.header("Modo de ensinar")
        question = st.text_input("Digite a pergunta aqui")
        answer = st.text_input("Digite a resposta aqui")
        if st.button("Enviar"):
            teach_assistant(question, answer)
    elif mode == "Conversar":
        st.header("Modo de conversar")
        question = st.text_input("Digite a pergunta aqui")
        if st.button("Enviar"):
            st.write(get_answer(question))
    elif mode == "Editar":
        st.header("Modo de editar")
        question = st.text_input("Digite a pergunta atual aqui")
        new_question = st.text_input("Digite a nova pergunta aqui")
        new_answer = st.text_input("Digite a nova resposta aqui")
        if st.button("Enviar"):
            edit_entry(question, new_question, new_answer)
    elif mode == "Deletar":
        st.header("Modo de deletar")
        question = st.text_input("Digite a pergunta aqui")
        if st.button("Deletar"):
            delete_entry(question)

if __name__ == "__main__":
    main()
