import openai
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar a API key da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chatbot_response(prompt, conversation_history):
    """
    Obtém uma resposta do chatbot usando a API da OpenAI e dados do banco.
    
    Args:
        prompt (str): A mensagem do usuário
        conversation_history (list): Histórico da conversa
    
    Returns:
        str: Resposta do chatbot
    """
    try:
        # Buscar informações no banco de dados
        db_info = get_bacteria_info(prompt)
        
        # Preparar o histórico de mensagens para a API
        messages = [
            {"role": "system", "content": """Você é um assistente virtual especializado em bactérias e microbiologia.
             Use as informações do banco de dados para responder às perguntas do usuário.
             Se não encontrar informações específicas no banco, forneça informações gerais sobre o tema.
             Mantenha um tom profissional e amigável."""}
        ]
        
        # Adicionar histórico da conversa
        messages.extend(conversation_history)
        
        # Adicionar informações do banco de dados
        messages.append({"role": "system", "content" : """Você é o Life Bot, um assistente especializado em microbiologia e análise bacteriana, integrado ao sistema Micro Life. Suas principais responsabilidades são:
            1. Informações sobre Bactérias:
            - Identificação e características de diferentes bactérias
            - Impactos na saúde humana
            - Condições de crescimento e proliferação

            2. Orientações sobre Medicamentos:
            - Antibióticos específicos para cada tipo de bactéria
            - Dosagens recomendadas (sempre com ressalva de consulta médica)
            - Possíveis efeitos colaterais
            - Resistência bacteriana

            3. Sistema Micro Life:
            - Funcionalidades do sistema de identificação bacteriana
            - Interpretação de resultados de análises
            - Mapeamento de incidências bacterianas
            - Tendências e padrões de distribuição geográfica

            4. Diretrizes de Comunicação:
            - Manter linguagem técnica mas acessível
            - Sempre recomendar consulta a profissionais de saúde
            - Focar exclusivamente em temas relacionados a bactérias
            - Priorizar informações baseadas em evidências científicas

            5. Limitações:
            - Não fazer diagnósticos
            - Não substituir orientação médica
            - Não discutir temas fora do escopo bacteriológico
            - Não revelar detalhes técnicos do sistema"""})
        
        # Adicionar a mensagem atual do usuário
        messages.append({"role": "user", "content": prompt})
        
        # Fazer a chamada à API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        # Extrair e retornar a resposta
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Desculpe, ocorreu um erro ao processar sua mensagem: {str(e)}"

def format_conversation_history(messages):
    """
    Formata o histórico de mensagens para o formato esperado pela API.
    
    Args:
        messages (list): Lista de mensagens no formato do Streamlit
    
    Returns:
        list: Lista formatada para a API
    """
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    return formatted_messages 