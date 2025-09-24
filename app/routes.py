from flask import Blueprint, render_template, request, jsonify
from app.services.ai_service import get_email_analysis
import PyPDF2
import io

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

def extrair_texto_de_arquivo(arquivo):
    """Função helper para extrair texto de .txt ou .pdf."""
    nome_arquivo = arquivo.filename.lower()
    texto_extraido = ""

    if nome_arquivo.endswith('.pdf'):
        try:
            leitor_pdf = PyPDF2.PdfReader(io.BytesIO(arquivo.read()))
            for pagina in leitor_pdf.pages:
                texto_extraido += pagina.extract_text()
        except Exception as e:
            print(f"Erro ao ler PDF: {e}")
            return None
    elif nome_arquivo.endswith('.txt'):
        try:
            texto_extraido = arquivo.read().decode('utf-8')
        except Exception as e:
            print(f"Erro ao ler TXT: {e}")
            return None
    
    return texto_extraido


@main_bp.route('/classify', methods=['POST'])
def classify_email():
    texto_para_analisar = ""

    if 'email-file' in request.files:
        arquivo = request.files['email-file']
        if arquivo.filename != '':
            texto_para_analisar = extrair_texto_de_arquivo(arquivo)
            if texto_para_analisar is None:
                return jsonify({'error': 'Não foi possível ler o arquivo enviado.'}), 400

    if not texto_para_analisar:
        texto_para_analisar = request.form.get('email-text')

    if not texto_para_analisar:
        return jsonify({'error': 'Nenhum texto ou arquivo válido foi enviado.'}), 400
    
    analysis_result = get_email_analysis(texto_para_analisar)
    return jsonify(analysis_result)