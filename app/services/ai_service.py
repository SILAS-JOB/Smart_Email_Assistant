import requests
import os

# --- Configuração ---
API_KEY = os.environ.get("HUGGING_FACE_API_KEY")

# Adicionando um check de segurança para garantir que a chave foi carregada.
if not API_KEY:
    raise ValueError("A chave HUGGING_FACE_API_KEY não foi encontrada no ambiente. Verifique seu arquivo .env")

# Modelos escolhidos por você, que são ótimos!
IDENTIFICADOR_CLASSIFICACAO = 'facebook/bart-large-mnli'
IDENTIFICADOR_GERACAO = 'distilgpt2' 

CLASSIFICATION_API_URL = f"https://api-inference.huggingface.co/models/{IDENTIFICADOR_CLASSIFICACAO}"
GENERATION_API_URL = f"https://api-inference.huggingface.co/models/{IDENTIFICADOR_GERACAO}"

headers = {"Authorization": f"Bearer {API_KEY}"}


def _call_api(payload, url):
    """Função genérica para fazer a chamada à API e tratar a resposta."""
    print(f"Enviando para URL: {url}")
    response = requests.post(url, headers=headers, json=payload)
    return response

def _classify_text(text):
    """Chama a API de classificação para determinar a categoria do e-mail."""
    payload = {
        "inputs": text,
        "parameters": {"candidate_labels": ["Produtivo", "Improdutivo"]},
    }
    response_obj = _call_api(payload, CLASSIFICATION_API_URL)
    
    if response_obj.status_code != 200:
        print(f"!!! Erro na API de Classificação ({response_obj.status_code}): {response_obj.text}")
        return "Erro de Classificação"
        
    response_json = response_obj.json()
    print(f"Resposta da Classificação: {response_json}")
    return response_json['labels'][0]

def _generate_response_text(email_text, category):
    """Chama a API de geração de texto para criar uma resposta sugerida."""
    if category == "Produtivo":
        prompt = f"Escreva uma resposta profissional curta em português para o seguinte e-mail:\n\nE-mail: \"{email_text}\"\n\nResposta:"
    else:
        prompt = f"Escreva uma resposta amigável e muito curta em português para o seguinte e-mail:\n\nE-mail: \"{email_text}\"\n\nResposta:"
    
    payload = { "inputs": prompt, "parameters": { "max_new_tokens": 100, "temperature": 0.7 } }
    
    response_obj = _call_api(payload, GENERATION_API_URL)

    if response_obj.status_code != 200:
        print(f"!!! Erro na API de Geração ({response_obj.status_code}): {response_obj.text}")
        return f"Erro na geração da resposta."

    response_json = response_obj.json()
    print(f"Resposta da Geração: {response_json}")
    return response_json[0]['generated_text'].replace(prompt, "").strip()

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