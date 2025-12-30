from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from functools import wraps
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'harmonia_secret_key_2026')
CORS(app)

# Configurações de Banco de Dados (MongoDB Atlas)
# A URI será lida de uma variável de ambiente para maior segurança
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://Harmonia231:harmonia231@cluster0.jdonuj2.mongodb.net/?appName=Cluster0')
client = MongoClient(MONGO_URI)
db = client['calendario_db']
eventos_col = db['eventos']
config_col = db['config']

# Configurações de Upload
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '231harmonia')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_site_config():
    """Busca a configuração no MongoDB ou retorna padrão."""
    config = config_col.find_one({}, {'_id': 0})
    if not config:
        return {
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
    return config

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    config = get_site_config()
    eventos = list(eventos_col.find({}, {'_id': 0}))
    return jsonify({"config": config, "eventos": eventos})

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(get_site_config())

# API - Atualizar configuração
@app.route('/api/config', methods=['POST'])
@login_required
def update_config():
    config = request.json
    config_col.replace_one({}, config, upsert=True)
    return jsonify({"status": "success", "message": "Configuração atualizada"})

# API - Criar evento
@app.route('/api/eventos', methods=['POST'])
@login_required
def create_evento():
    evento = request.json
    # Gerar ID numérico simples para compatibilidade com o frontend atual
    last_evento = eventos_col.find_one(sort=[("id", -1)])
    new_id = (last_evento['id'] + 1) if last_evento else 1
    evento['id'] = new_id
    
    eventos_col.insert_one(evento)
    if '_id' in evento: del evento['_id']
    return jsonify({"status": "success", "evento": evento})

# API - Atualizar evento
@app.route('/api/eventos/<int:evento_id>', methods=['PUT'])
@login_required
def update_evento(evento_id):
    evento_data = request.json
    evento_data['id'] = evento_id
    result = eventos_col.replace_one({"id": evento_id}, evento_data)
    
    if result.matched_count > 0:
        if '_id' in evento_data: del evento_data['_id']
        return jsonify({"status": "success", "evento": evento_data})
    return jsonify({"status": "error", "message": "Evento não encontrado"}), 404

# API - Deletar evento
@app.route('/api/eventos/<int:evento_id>', methods=['DELETE'])
@login_required
def delete_evento(evento_id):
    eventos_col.delete_one({"id": evento_id})
    return jsonify({"status": "success", "message": "Evento deletado"})

# API - Upload de imagem
@app.route('/api/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Nenhum arquivo fornecido"}), 400
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"status": "error", "message": "Arquivo inválido"}), 400
    
    filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return jsonify({"status": "success", "url": f"/uploads/{filename}"})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
