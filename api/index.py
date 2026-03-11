from flask import Flask, request, jsonify # Framework web leve para criar a API
from flask_cors import CORS # Permite que o frontend (que roda em outro domínio/porta) acesse a API sem problemas de CORS
import google.generativeai as genai # Biblioteca oficial do Google para acessar os modelos de IA generativa (como o Gemini) de forma fácil e segura
import os # Biblioteca padrão do Python para interagir com o sistema operacional, usada aqui para acessar variáveis de ambiente (como a chave da API)
from dotenv import load_dotenv

# Carrega a chave do arquivo .env
load_dotenv() # Carrega as variáveis de ambiente do arquivo .env para que possamos acessar a chave da API de forma segura

app = Flask(__name__) # Cria uma instância do Flask, que é o nosso servidor web
CORS(app) # Habilita CORS para permitir que o frontend (que roda em outro domínio/porta) acesse a API sem problemas de CORS

# 1. Configura a biblioteca oficial do Google com a sua chave secreta
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Escolhe o modelo que vamos usar
model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

@app.route('/api/gerar-roteiro', methods=['POST']) # o usuário clica em "Gerar Roteiro", o Front-end envia um pedido (request) para essa função
def gerar_roteiro():
    try:
        # Recebe os dados do frontend (agora enviaremos apenas o texto puro)
        dados = request.json
        prompt_do_usuario = dados.get("prompt")
        
        if not prompt_do_usuario:
            return jsonify({"error": "Nenhum prompt foi enviado."}), 400

        # 3. Manda a biblioteca gerar o conteúdo (ela faz a requisição por baixo dos panos)
        resposta_ia = model.generate_content(prompt_do_usuario) # A biblioteca oficial do Google cuida de toda a comunicação com a API do Gemini, incluindo autenticação, formatação da requisição e tratamento da resposta. Você só precisa chamar generate_content() com o texto do prompt, e ela retorna um objeto com o texto gerado pela IA. Isso torna o código muito mais limpo e fácil de entender, sem precisar lidar com detalhes técnicos como headers, tokens ou parsing manual da resposta JSON.

        # 4. Devolve o texto gerado de forma limpa e direta para o seu site
        return jsonify({"texto_gerado": resposta_ia.text})

    except Exception as e:
        print("Erro na IA:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__': # Inicia o servidor Flask quando este arquivo for executado diretamente
    print("Servidor Python com SDK do Gemini rodando em http://localhost:5000")
    app.run(port=5000, debug=True)