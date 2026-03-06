from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega a chave do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# 1. Configura a biblioteca oficial do Google com a sua chave secreta
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Escolhe o modelo que vamos usar
model = genai.GenerativeModel('gemini-2.0-flash')

@app.route('/api/gerar-roteiro', methods=['POST'])
def gerar_roteiro():
    try:
        # Recebe os dados do frontend (agora enviaremos apenas o texto puro)
        dados = request.json
        prompt_do_usuario = dados.get("prompt")
        
        if not prompt_do_usuario:
            return jsonify({"error": "Nenhum prompt foi enviado."}), 400

        # 3. Manda a biblioteca gerar o conteúdo (ela faz a requisição por baixo dos panos)
        resposta_ia = model.generate_content(prompt_do_usuario)

        # 4. Devolve o texto gerado de forma limpa e direta para o seu site
        return jsonify({"texto_gerado": resposta_ia.text})

    except Exception as e:
        print("Erro na IA:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Servidor Python com SDK do Gemini rodando em http://localhost:5000")
    app.run(port=5000, debug=True)