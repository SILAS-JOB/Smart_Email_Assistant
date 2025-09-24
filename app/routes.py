from flask import Blueprint, render_template, request, jsonify
from app.services.ai_service import get_email_analysis

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/classify', methods=['POST'])
def classify_email():
    email_text = request.json.get('text')
    if not email_text:
        return jsonify({'error': 'Nenhum texto foi enviado.'}), 400
    # mock_response = {
    #     'category': 'Produtivo (Teste)',
    #     'suggested_response': 'Esta é uma resposta de teste gerada pelo backend.'
    # }
    # return jsonify(mock_response)
    analysis_result = get_email_analysis(email_text)
    return jsonify(analysis_result)