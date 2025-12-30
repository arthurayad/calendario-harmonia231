from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from functools import wraps
from pymongo import MongoClient
import logging
import certifi

# Configuração de Logs para o Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'harmonia_secret_key_2026')
CORS(app)

# Configurações de Banco de Dados (MongoDB Atlas)
MONGO_URI = "mongodb+srv://Harmonia231:harmonia231@cluster0.jdonuj2.mongodb.net/?appName=Cluster0"
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '231harmonia')

# Conexão com o MongoDB usando Certifi para evitar erro de SSL
ca = certifi.where()
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, tlsCAFile=ca)
    db = client['calendario_db']
    eventos_col = db['eventos']
    config_col = db['config']
    client.admin.command('ping')
    logger.info("Conectado ao MongoDB com sucesso!")
except Exception as e:
    logger.error(f"Erro ao conectar ao MongoDB: {e}")
    db = None

# Configurações de Upload
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_site_config():
    """Busca a configuração no MongoDB ou retorna padrão."""
    default_config = {
        "title": "Calendário Gestão 2026/A",
        "local": "Rua José Pereira Liberato, 1178",
        "contact": "(47) 99286-0936 (Arthur Ayad)",
        "primaryColor": "#4a9b8e",
        "colors": {
            "estadual": "#1e3a52",
            "ritualistica": "#4a7c59",
            "entretenimento": "#d4a574",
            "publica": "#4a9b8e",
            "feriado": "#e74c3c"
        }
    }
    if db is None: return default_config
    try:
        config = config_col.find_one({}, {'_id': 0})
        return config if config else default_config
    except Exception as e:
        logger.error(f"Erro ao buscar config: {e}")
        return default_config

def migrar_dados_se_vazio():
    """Migra dados do data.json para o MongoDB se o banco estiver vazio."""
    if db is not None:
        try:
            # Verifica se já existem eventos no banco
            if eventos_col.count_documents({}) == 0:
                logger.info("Banco vazio detectado. Iniciando migração do data.json...")
                if os.path.exists('data.json'):
                    with open('data.json', 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Migra configurações
                    if 'config' in data and data['config']:
                        config_col.replace_one({}, data['config'], upsert=True)
                        logger.info("Configurações migradas.")
                    
                    # Migra eventos
                    if 'eventos' in data and data['eventos']:
                        eventos_col.insert_many(data['eventos'])
                        logger.info(f"{len(data['eventos'])} eventos migrados.")
                    
                    logger.info("Migração automática concluída com sucesso!")
                else:
                    logger.warning("Arquivo data.json não encontrado para migração.")
            else:
                logger.info("Banco de dados já contém dados. Pulando migração.")
        except Exception as e:
            logger.error(f"Erro na migração automática: {e}")

# Rotas Frontend
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error="Senha incorreta")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

# API - Obter dados
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        config = get_site_config()
        eventos = []
        if db is not None:
            eventos = list(eventos_col.find({}, {'_id': 0}))
        return jsonify({"config": config, "eventos": eventos})
    except Exception as e:
        logger.error(f"Erro em /api/data: {e}")
        return jsonify({"config": get_site_config(), "eventos": [], "error": str(e)}), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(get_site_config())

@app.route('/api/eventos', methods=['GET'])
def get_eventos():
    try:
        eventos = []
        if db is not None:
            eventos = list(eventos_col.find({}, {'_id': 0}))
        return jsonify(eventos)
    except Exception as e:
        logger.error(f"Erro em GET /api/eventos: {e}")
        return jsonify([]), 500

# API - Atualizar configuração
@app.route('/api/config', methods=['POST'])
@login_required
def update_config():
    if db is None: return jsonify({"status": "error", "message": "Banco indisponível"}), 503
    try:
        config = request.json
        config_col.replace_one({}, config, upsert=True)
        return jsonify({"status": "success", "message": "Configuração atualizada"})
    except Exception as e:
        logger.error(f"Erro ao atualizar config: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# API - Criar evento
@app.route('/api/eventos', methods=['POST'])
@login_required
def create_evento():
    if db is None: return jsonify({"status": "error", "message": "Banco indisponível"}), 503
    try:
        evento = request.json
        last_evento = eventos_col.find_one(sort=[("id", -1)])
        if last_evento and 'id' in last_evento:
            new_id = int(last_evento['id']) + 1
        else:
            new_id = eventos_col.count_documents({}) + 1
        evento['id'] = new_id
        eventos_col.insert_one(evento)
        if '_id' in evento: del evento['_id']
        return jsonify({"status": "success", "evento": evento})
    except Exception as e:
        logger.error(f"Erro ao criar evento: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# API - Atualizar evento
@app.route('/api/eventos/<int:evento_id>', methods=['PUT'])
@login_required
def update_evento(evento_id):
    if db is None: return jsonify({"status": "error", "message": "Banco indisponível"}), 503
    try:
        evento_data = request.json
        evento_data['id'] = evento_id
        result = eventos_col.replace_one({"id": evento_id}, evento_data)
        if result.matched_count > 0:
            if '_id' in evento_data: del evento_data['_id']
            return jsonify({"status": "success", "evento": evento_data})
        return jsonify({"status": "error", "message": "Evento não encontrado"}), 404
    except Exception as e:
        logger.error(f"Erro ao atualizar evento {evento_id}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# API - Deletar evento
@app.route('/api/eventos/<int:evento_id>', methods=['DELETE'])
@login_required
def delete_evento(evento_id):
    if db is None: return jsonify({"status": "error", "message": "Banco indisponível"}), 503
    try:
        eventos_col.delete_one({"id": evento_id})
        return jsonify({"status": "success", "message": "Evento deletado"})
    except Exception as e:
        logger.error(f"Erro ao deletar evento {evento_id}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# API - Upload de imagem
@app.route('/api/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Nenhum arquivo"}), 400
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"status": "error", "message": "Arquivo inválido"}), 400
    try:
        filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({"status": "success", "url": f"/uploads/{filename}"})
    except Exception as e:
        logger.error(f"Erro no upload: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Executa a migração automática antes de iniciar o servidor
    migrar_dados_se_vazio()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
