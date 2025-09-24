import os
from dotenv import load_dotenv

load_dotenv() 

class Config:
    """Classe de configuração base."""
    
    DEBUG = True
    
    # Nossas configurações personalizadas
    HUGGING_FACE_API_KEY = os.environ.get("HUGGING_FACE_API_KEY")