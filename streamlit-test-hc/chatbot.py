import streamlit as st
import time
import json
from openai_integration import get_chatbot_response, format_conversation_history
from datetime import datetime

def save_conversation_to_cache(messages):
    """Salva a conversa no cache do navegador"""
    st.session_state['cached_conversation'] = json.dumps(messages)
    st.markdown(
        f"""
        <script>
            localStorage.setItem('chatbot_conversation', '{st.session_state['cached_conversation']}');
        </script>
        """,
        unsafe_allow_html=True
    )

def load_conversation_from_cache():
    """Carrega a conversa do cache do navegador"""
    st.markdown(
        """
        <script>
            var conversation = localStorage.getItem('chatbot_conversation');
            if (conversation) {
                window.parent.postMessage({type: 'load_conversation', data: conversation}, '*');
            }
        </script>
        """,
        unsafe_allow_html=True
    )

def initialize_conversation():
    """Inicializa a conversa com mensagem de boas-vindas"""
    return [
        {
            "role": "assistant",
            "content": "Olá! Sou o Life Bot, seu assistente virtual especializado em bactérias e microbiologia. Como posso ajudar você hoje?",
            "timestamp": datetime.now().isoformat()
        }
    ]

def chatbot_page():
    # Configuração da página
    st.markdown("""
        <h1>Life Bot 🤖</h1>
        <p>Assistente virtual para dúvidas sobre bactérias e microbiologia.</p>
    """, unsafe_allow_html=True)

    # Inicializar o histórico de chat na sessão
    if "messages" not in st.session_state:
        st.session_state.messages = initialize_conversation()
        save_conversation_to_cache(st.session_state.messages)

    # Carregar conversa do cache
    load_conversation_from_cache()

    # Exibir mensagens do chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Exibir timestamp se disponível
            if "timestamp" in message:
                st.caption(f"Enviado em: {datetime.fromisoformat(message['timestamp']).strftime('%d/%m/%Y %H:%M:%S')}")

    # Campo de entrada do usuário
    if prompt := st.chat_input("Digite sua mensagem aqui..."):
        # Adicionar mensagem do usuário ao histórico
        user_message = {
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        }
        st.session_state.messages.append(user_message)
        
        # Exibir mensagem do usuário
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"Enviado em: {datetime.fromisoformat(user_message['timestamp']).strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Obter resposta do chatbot
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                # Formatar histórico e obter resposta
                formatted_history = format_conversation_history(st.session_state.messages)
                response_stream = get_chatbot_response(prompt, formatted_history, stream=True)
                
                # Criar um placeholder para a resposta
                message_placeholder = st.empty()
                full_response = ""
                
                # Exibir a resposta token por token
                for chunk in response_stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                # Atualizar o placeholder com a resposta final
                message_placeholder.markdown(full_response)
                
                # Criar mensagem do assistente com timestamp
                assistant_message = {
                    "role": "assistant",
                    "content": full_response,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Salvar a resposta completa no histórico
                st.session_state.messages.append(assistant_message)
                
                # Salvar conversa atualizada no cache
                save_conversation_to_cache(st.session_state.messages)
                
                # Exibir timestamp da resposta
                st.caption(f"Enviado em: {datetime.fromisoformat(assistant_message['timestamp']).strftime('%d/%m/%Y %H:%M:%S')}")

    # Adicionar botão para limpar histórico
    if st.sidebar.button("Limpar Histórico"):
        st.session_state.messages = initialize_conversation()
        save_conversation_to_cache(st.session_state.messages)
        st.rerun()