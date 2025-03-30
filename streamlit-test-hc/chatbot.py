import streamlit as st
import time
from openai_integration import get_chatbot_response, format_conversation_history

def chatbot_page():
    # Configuração da página
    st.markdown("""
        <h1>Life Bot 🤖</h1>
        <p>Assistente virtual para dúvidas sobre bactérias e microbiologia.</p>
    """, unsafe_allow_html=True)

    # Inicializar o histórico de chat na sessão
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Sou o Life Bot, seu assistente virtual especializado em bactérias e microbiologia. Como posso ajudar você hoje?"}
        ]

    # Exibir mensagens do chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Campo de entrada do usuário
    if prompt := st.chat_input("Digite sua mensagem aqui..."):
        # Adicionar mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Exibir mensagem do usuário
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Obter resposta do chatbot
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                # Formatar histórico e obter resposta
                formatted_history = format_conversation_history(st.session_state.messages)
                response = get_chatbot_response(prompt, formatted_history)
                
                # Exibir e salvar resposta
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})