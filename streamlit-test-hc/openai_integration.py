from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd
import json

# Carregar variáveis de ambiente
load_dotenv()

# Configurar a API key da OpenAI
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def load_csv_data():
    """
    Carrega os dados das planilhas CSV e retorna um dicionário com as informações.
    """
    try:
        # Carregar dados da planilha de registros
        registers_df = pd.read_csv('databases/registers_202503301413.csv')
        registers_info = registers_df.to_dict('records')
        
        # Carregar dados da planilha de pragas
        plague_df = pd.read_csv('databases/plague_202503301415.csv')
        plague_info = plague_df.to_dict('records')
        
        return {
            "registers": registers_info,
            "plague": plague_info
        }
    except Exception as e:
        print(f"Erro ao carregar dados CSV: {str(e)}")
        return None

def format_csv_context(csv_data):
    """
    Formata os dados CSV em um contexto estruturado para o chatbot.
    """
    if not csv_data:
        return ""
    
    context = "Você tem acesso às seguintes informações especializadas:\n\n"
    
    # Formatar informações sobre pragas
    context += "Informações sobre Pragas:\n"
    for plague in csv_data["plague"]:
        context += f"- Nome: {plague.get('name', 'N/A')}\n"
        context += f"  Características: {plague.get('characteristics', 'N/A')}\n"
        context += f"  Localização: {plague.get('Location', 'N/A')}\n"
        context += f"  Diagnóstico: {plague.get('Diessing', 'N/A')}\n"
        context += f"  Sintomas: {plague.get('Symptoms', 'N/A')}\n"
        context += f"  Medicamentos: {plague.get('Medications', 'N/A')}\n"
        context += f"  Dicas: {plague.get('Tips', 'N/A')}\n"
        context += f"  Prevenção: {plague.get('Prevention', 'N/A')}\n\n"
    
    # Formatar informações sobre registros
    context += "\nRegistros de Detecções:\n"
    for register in csv_data["registers"]:
        context += f"- Praga: {register.get('plague', 'N/A')}\n"
        context += f"  Data: {register.get('timestamp', 'N/A')}\n"
        context += f"  Localização: {register.get('location', 'N/A')}\n"
        context += f"  Observações: {register.get('observations', 'N/A')}\n\n"
    
    return context

def get_chatbot_response(prompt, conversation_history, stream=False):
    """
    Obtém uma resposta do chatbot usando a API da OpenAI e dados do banco.
    
    Args:
        prompt (str): A mensagem do usuário
        conversation_history (list): Histórico da conversa
        stream (bool): Se True, retorna um gerador para streaming da resposta
    
    Returns:
        str ou generator: Resposta do chatbot ou gerador de tokens
    """
    try:        
        # Carregar dados CSV
        csv_data = load_csv_data()
        csv_context = format_csv_context(csv_data)
        
        # Preparar o histórico de mensagens para a API
        messages = [
            {
                "role": "system",
                "content": f"""Você é um assistente virtual especializado em bactérias e microbiologia.
                Use as informações do banco de dados para responder às perguntas do usuário.
                Se não encontrar informações específicas no banco, forneça informações gerais sobre o tema.
                Mantenha um tom profissional e amigável.
                
                {csv_context}"""
            }
        ]
        
        # Adicionar histórico da conversa
        messages.extend(conversation_history)
        
        # Adicionar informações do banco de dados
        messages.append({
            "role": "system",
            "content": """Você é o Life Bot, um assistente especializado em microbiologia e análise bacteriana, integrado ao sistema Micro Life. Suas principais responsabilidades são:
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
            - Sempre que listar dados do nosso banco, formato no seguinte, latitude e longitude, é um array, ler cada informação,  não precisa mostrar o dado, porém informe locais próximos de onde foram encontradas baseado nas localizações com locais mais conhecidos e possíveis, data sempre em formato dd/mm/yyyy, Palavra praga virar bacteria e as obersavações no seguinte formato "Obs: <observacoes>"


            5. Limitações:
            - Não fazer diagnósticos
            - Não substituir orientação médica
            - Não discutir temas fora do escopo bacteriológico
            - Não revelar detalhes técnicos do sistema"""
        })
        
        # Adicionar a mensagem atual do usuário
        messages.append({"role": "user", "content": prompt})
        
        # Fazer a chamada à API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            stream=stream
        )
        
        if stream:
            return response
        else:
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

def get_response(prompt, conversation_history=None):
    """
    Obtém uma resposta do assistente usando a API da OpenAI.
    
    Args:
        prompt (str): A mensagem do usuário
        conversation_history (list, optional): Histórico da conversa
    
    Returns:
        str: Resposta do assistente
    """
    if conversation_history is None:
        conversation_history = []
    
    return get_chatbot_response(prompt, conversation_history)

# my_assistants = client.beta.assistants.list(
#     order="desc",
#     limit="20",
# )
# print(my_assistants.data)