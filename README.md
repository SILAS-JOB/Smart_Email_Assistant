Assistente Inteligente de E-mails 📧✨

Aplicação web que utiliza Inteligência Artificial para classificar e-mails, otimizar o fluxo de trabalho e aumentar a produtividade. O sistema categoriza mensagens como "Produtivo" ou "Improdutivo" e sugere respostas automáticas adequadas ao contexto.

Este projeto foi desenvolvido como o case prático para o processo seletivo de Desenvolvedor da AutoU.

🚀 Acesse a Aplicação ao Vivo: [COLOQUE AQUI O LINK DO SEU APP NO RENDER.COM]

🎬 Demonstração

A interface permite a análise de texto inserido diretamente ou através do upload de arquivos .txt e .pdf. O resultado exibe a categoria, a confiança da IA e uma resposta sugerida.

[ADICIONE AQUI UM SCREENSHOT OU UM GIF DA SUA APLICAÇÃO FUNCIONANDO]

📋 Índice

    Sobre o Projeto

    Funcionalidades

    Tecnologias Utilizadas

    Arquitetura e Decisões Técnicas

    Como Rodar o Projeto Localmente

    Deploy

    Licença

📖 Sobre o Projeto

O objetivo deste desafio foi desenvolver uma solução para uma empresa do setor financeiro que lida com um alto volume de e-mails. A aplicação automatiza a leitura e triagem, liberando a equipe de tarefas manuais e repetitivas, permitindo que foquem em atividades de maior valor.

O sistema utiliza modelos de Processamento de Linguagem Natural (NLP) para entender o conteúdo dos e-mails e realizar duas ações principais:

    Classificação Zero-Shot: Determina se o e-mail requer uma ação (Produtivo) ou não (Improdutivo).

    Geração de Texto: Cria uma sugestão de resposta em português, adaptada à categoria do e-mail.

✨ Funcionalidades

    ✅ Classificação de E-mails: Análise de texto para categorização automática.

    ✅ Sugestão de Respostas: Geração de respostas contextuais com IA.

    ✅ Input Flexível: Suporte para inserção de texto direto e upload de arquivos (.txt e .pdf).

    ✅ Exibição de Confiança: Mostra a porcentagem de confiança do modelo na classificação.

    ✅ Interface Intuitiva: Feedback visual de "carregando" e botão para copiar a resposta gerada.

    ✅ Pré-processamento de Texto: Utilização de NLTK para limpeza de stopwords antes da análise.

🛠️ Tecnologias Utilizadas

    Backend: Python 3, Flask, Gunicorn

    Inteligência Artificial:

        Hugging Face (Inference API)

        Biblioteca huggingface_hub para comunicação robusta com a API

    Frontend: HTML5, CSS3, JavaScript (ES6)

    Processamento de Arquivos: PyPDF2

    Gerenciamento de Dependências: Pip, Venv

    Deploy: Render

🧠 Arquitetura e Decisões Técnicas

A aplicação foi estruturada seguindo o padrão Application Factory em Flask para garantir organização e escalabilidade, com uma clara separação de responsabilidades entre rotas, serviços e templates.

O principal desafio técnico foi estabelecer uma comunicação estável e correta com a Inference API da Hugging Face. A jornada de depuração foi um aprendizado valioso:

    Diagnóstico de Erros: As tentativas iniciais com requests manuais resultaram em erros 404 Not Found persistentes, mesmo com identificadores de modelo aparentemente válidos.

    Identificação da Causa Raiz: Através de logs detalhados e da análise de erros 402 Payment Required (após esgotar a cota gratuita de testes), ficou claro que a comunicação precisava ser mais robusta. O erro final, Model is not supported for task text-generation. Supported task: conversational, revelou que os modelos mais modernos exigem um tipo de tarefa específico.

    Solução Profissional: A decisão estratégica foi abandonar a abordagem manual e adotar a biblioteca oficial huggingface_hub. Utilizando o InferenceClient, foi possível interagir com os modelos através das funções corretas (zero_shot_classification e chat_completion), o que resolveu definitivamente os problemas de conexão.

    Melhoria de Precisão: Para aumentar a acurácia da classificação de textos em português, foi implementada a técnica de Few-Shot Prompting, fornecendo exemplos diretamente no prompt enviado ao modelo, o que melhorou significativamente seu raciocínio contextual.

⚙️ Como Rodar o Projeto Localmente

Siga os passos abaixo para configurar e executar a aplicação em seu ambiente local.

    Clone o repositório:
    Bash

git clone [COLOQUE AQUI A URL DO SEU REPOSITÓRIO GIT]
cd [NOME-DA-PASTA-DO-PROJETO]

Crie e ative um ambiente virtual:
Bash

# No Windows
python -m venv venv
.\venv\Scripts\activate

# No macOS/Linux
python3 -m venv venv
source venv/bin/activate

Instale as dependências:

pip install -r requirements.txt

Configure as variáveis de ambiente:

    Crie um arquivo chamado .env na raiz do projeto.

    Adicione sua chave de API da Hugging Face dentro dele:

    HUGGING_FACE_API_KEY="hf_sua_chave_secreta_aqui"

Execute a aplicação:
Bash

    python run.py

    A aplicação estará disponível em http://127.0.0.1:5000.

☁️ Deploy

A aplicação está hospedada na plataforma Render, configurada para deploy contínuo a partir da branch main do repositório. O servidor de produção utilizado é o Gunicorn, e as chaves de API são gerenciadas como variáveis de ambiente no painel do Render para garantir a segurança.

📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
