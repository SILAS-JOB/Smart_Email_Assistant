import nltk
from dotenv import load_dotenv

try:
    print("Verificando pacotes NLTK...")
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt')
    print("Pacotes NLTK já existem.")
except LookupError:
    print("Baixando pacotes NLTK necessários...")
    nltk.download('popular')
    nltk.download('stopwords')
    print("Download dos pacotes NLTK concluído.")

load_dotenv()

from app import create_app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)