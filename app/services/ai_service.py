import requests
import os

# --- Configuração ---
API_KEY = os.environ.get("HUGGING_FACE_API_KEY")
CLASSIFICATION_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
GENERATION_API_URL = "https://api-inference.huggingface.co/models/gpt2" 
headers = {"Authorization": f"Bearer {API_KEY}"}

def _call_api(payload, url):
    """Função genérica para fazer a chamada à API e tratar a resposta."""
    response = requests.post(url, headers=headers, json=payload)
    return response

def _classify_text(text):
    """Chama a API de classificação para determinar a categoria do e-mail."""
    print("----- INICIANDO CLASSIFICAÇÃO -----")
    payload = {
        "inputs": text,
        "parameters": {"candidate_labels": ["Produtivo", "Improdutivo"]},
    }
    response_obj = _call_api(payload, CLASSIFICATION_API_URL)
    
    print(f"Status da Classificação: {response_obj.status_code}")
    response_json = response_obj.json()
    print(f"Resposta Completa da Classificação: {response_json}")
    
    if response_obj.status_code != 200:
        return "Erro de Classificação"
        
    print("----- CLASSIFICAÇÃO BEM SUCEDIDA -----")
    return response_json['labels'][0]

def _generate_response_text(email_text, category):
    """Chama a API de geração de texto para criar uma resposta sugerida."""
    print("----- INICIANDO GERAÇÃO DE RESPOSTA -----")
    
    if category == "Produtivo":
        prompt = f"Given the following productive email, write a short, professional, and helpful reply in Portuguese:\n\nEmail: \"{email_text}\"\n\nProfessional Reply:"
    else:
        prompt = f"Given the following non-productive email, write a very short and friendly reply in Portuguese acknowledging the message:\n\nEmail: \"{email_text}\"\n\nFriendly Reply:"
    
    payload = { "inputs": prompt, "parameters": { "max_length": 100, "num_return_sequences": 1 } }
    
    response_obj = _call_api(payload, GENERATION_API_URL)

    print(f"Status da Geração: {response_obj.status_code}")
    response_json = response_obj.json()
    print(f"Resposta Completa da Geração: {response_json}")

    if response_obj.status_code != 200:
        return f"Erro na geração da resposta. Detalhe: {response_json.get('error', 'Erro desconhecido')}"

    print("----- GERAÇÃO BEM SUCEDIDA -----")
    return response_json[0]['generated_text'].replace(prompt, "").strip()

def get_email_analysis(text):
    """Função principal que orquestra a análise do e-mail."""
    category = _classify_text(text)
    
    if category == "Erro de Classificação":
        return {
            'category': 'Falha na Classificação',
            'suggested_response': 'Não foi possível determinar a categoria do e-mail.'
        }
        
    suggested_response = _generate_response_text(text, category)
    
    return {
        'category': category,
        'suggested_response': suggested_response
    }