import requests
import os

# --- Configuração ---
API_KEY = os.environ.get("HUGGING_FACE_API_KEY")

CLASSIFICATION_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
GENERATION_API_URL = "https://api-inference.huggingface.co/models/gpt2-large" 

headers = {"Authorization": f"Bearer {API_KEY}"}


# --- Funções "Helper" ---
def _call_api(payload, url):
    """Função genérica para fazer a chamada à API e tratar a resposta."""
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        return {"error": f"API request failed with status code {response.status_code}: {response.text}"}
    return response.json()

def _classify_text(text):
    """Chama a API de classificação para determinar a categoria do e-mail."""
    payload = {
        "inputs": text,
        "parameters": {"candidate_labels": ["Produtivo", "Improdutivo"]},
    }
    api_response = _call_api(payload, CLASSIFICATION_API_URL)
    
    if "error" in api_response:
        return "Erro de Classificação"
        
    return api_response['labels'][0]

def _generate_response_text(email_text, category):
    """Chama a API de geração de texto para criar uma resposta sugerida."""
    
    # --- Engenharia de Prompt ---
    if category == "Produtivo":
        prompt = f"Given the following productive email, write a short, professional, and helpful reply in Portuguese:\n\nEmail: \"{email_text}\"\n\nProfessional Reply:"
    elif category == "Improdutivo":
        prompt = f"Given the following non-productive (e.g., thank you, happy holidays) email, write a very short and friendly reply in Portuguese acknowledging the message:\n\nEmail: \"{email_text}\"\n\nFriendly Reply:"
    else:
        prompt = f"Given the following email, write a short, neutral reply in Portuguese:\n\nEmail: \"{email_text}\"\n\nNeutral Reply:"
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 100,      
            "num_return_sequences": 1
        }
    }
    api_response = _call_api(payload, GENERATION_API_URL)

    if "error" in api_response:
        return "Erro na geração da resposta."

    return api_response[0]['generated_text'].replace(prompt, "").strip()


# --- Função Principal ---

def get_email_analysis(text):
    """
    Função principal que orquestra a análise do e-mail.
    1. Classifica o texto.
    2. Gera uma resposta com base na classificação.
    3. Retorna um dicionário com os resultados.
    """
    category = _classify_text(text)
    suggested_response = _generate_response_text(text, category)
    
    return {
        'category': category,
        'suggested_response': suggested_response
    }