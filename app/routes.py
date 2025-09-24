from flask import Blueprint, render_template, request, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/classify', methods=['POST'])
def classify_email():
    email_text = request.json.get('text')
    #Test
    print(f"Texto Recebido: {email_text}")
    mock_response = {
        'category' : 'Produtivo (Teste)',
        'suggested_response' : 'Essa é uma resposta de teste gerada pelo backend'
    }
    return jsonify(mock_response)