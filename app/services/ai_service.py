import os
from huggingface_hub import InferenceClient

# --- Configuração ---
API_KEY = os.environ.get("HUGGING_FACE_API_KEY")

if not API_KEY:
    raise ValueError("A chave HUGGING_FACE_API_KEY não foi encontrada. Verifique seu arquivo .env")

# --- Modelos ---
MODELO_CLASSIFICACAO = 'facebook/bart-large-mnli'
MODELO_GERACAO = 'mistralai/Mistral-7B-Instruct-v0.2'

# --- Cliente Oficial da API ---
client = InferenceClient(token=API_KEY)


def _classify_text(text):
    """Chama a API de classificação usando o cliente oficial."""
    print(f"--- Classificando com o modelo: {MODELO_CLASSIFICACAO} ---")
    try:
        resultado = client.zero_shot_classification(
            text,
            candidate_labels=["Produtivo", "Improdutivo"],
            model=MODELO_CLASSIFICACAO
        )
        print(f"Resposta da Classificação: {resultado}")
        return resultado[0].label
    except Exception as e:
        print(f"!!! Erro na API de Classificação: {e}")
        return "Erro de Classificação"

def _generate_response_text(email_text, category):
    """Chama a API de geração de texto usando a tarefa 'conversational'."""
    print(f"--- Gerando resposta com o modelo (modo Chat): {MODELO_GERACAO} ---")
    
    if category == "Produtivo":
        system_prompt = "Você é um assistente de e-mail profissional que escreve respostas curtas e úteis em português."
        user_prompt = f"Escreva uma resposta para o seguinte e-mail:\n\n{email_text}"
    else:
        system_prompt = "Você é um assistente de e-mail amigável que escreve respostas muito curtas e simpáticas em português."
        user_prompt = f"Escreva uma resposta para o seguinte e-mail:\n\n{email_text}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    try:
        resposta_gerada = client.chat_completion(
            messages,
            model=MODELO_GERACAO,
            max_tokens=100, 
        )
        conteudo_resposta = resposta_gerada.choices[0].message.content
        print(f"Resposta da Geração: {conteudo_resposta}")
        return conteudo_resposta.strip()
    except Exception as e:
        print(f"!!! Erro na API de Geração: {e}")
        return "Erro na geração da resposta."

def get_email_analysis(text):
    """Função principal que orquestra a análise do e-mail."""
    category = _classify_text(text)
    
    if "Erro" in category:
        return {'category': category, 'suggested_response': 'Falha na primeira etapa.'}
        
    suggested_response = _generate_response_text(text, category)
    
    return {
        'category': category,
        'suggested_response': suggested_response
    }