from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app) # Permite que o S3 converse com o EC2

# Configurações do seu Banco de Dados RDS
DB_HOST = 'projeto2-bancochamadosrds-nsnd0nubreyn.cz4em6ee4m9j.us-east-2.rds.amazonaws.com'
DB_USER = 'admin_florence'
DB_PASS = 'PasswordSegura123!'
DB_NAME = 'florence_db'

@app.route('/chamados', methods=['POST'])
def receber_chamado():
    dados = request.json
    try:
        # Conecta no banco
        conexao = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        cursor = conexao.cursor()
        
        # Insere os dados
        sql = "INSERT INTO chamados (nome_funcionario, setor, prioridade, descricao) VALUES (%s, %s, %s, %s)"
        valores = (dados['nome'], dados['setor'], dados['prioridade'], dados['descricao'])
        cursor.execute(sql, valores)
        conexao.commit()
        conexao.close()
        
        print("Novo chamado registrado: ", dados['nome'])
        return jsonify({"mensagem": "Chamado salvo no banco de dados com sucesso!"}), 201

    except Exception as e:
        print("Erro:", str(e))
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    # Roda a API na porta 80 (HTTP padrão)
    app.run(host='0.0.0.0', port=80)