from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.secret_key = 'harmonia_secret_key_2026' # Chave para sessões
CORS(app)

# Configurações
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}
ADMIN_PASSWORD = '231harmonia'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Arquivo de dados
DATA_FILE = 'data.json'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def load_data():
    """Carrega dados do arquivo JSON."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"config": {}, "eventos": []}

def save_data(data):
    """Salva dados no arquivo JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def allowed_file(filename):
    """Verifica se o arquivo é permitido."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rotas Frontend
@app.route('/')
def index():
    """Página principal do calendário."""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login."""
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
    """Faz logout do usuário."""
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    """Página de administração."""
    return render_template('admin.html')

# API - Obter dados (Pública)
@app.route('/api/data', methods=['GET'])
def get_data():
    """Retorna todos os dados (config e eventos)."""
    data = load_data()
    return jsonify(data)

@app.route('/api/config', methods=['GET'])
def get_config():
    """Retorna apenas a configuração."""
    data = load_data()
    return jsonify(data.get('config', {}))

@app.route('/api/eventos', methods=['GET'])
def get_eventos():
    """Retorna todos os eventos."""
    data = load_data()
    return jsonify(data.get('eventos', []))

# API - Atualizar configuração (Protegida)
@app.route('/api/config', methods=['POST'])
@login_required
def update_config():
    """Atualiza a configuração."""
    data = load_data()
    config = request.json
    data['config'] = config
    save_data(data)
    return jsonify({"status": "success", "message": "Configuração atualizada"})

# API - Criar evento (Protegida)
@app.route('/api/eventos', methods=['POST'])
@login_required
def create_evento():
    """Cria um novo evento."""
    data = load_data()
    evento = request.json
    
    # Gera um novo ID
    if data['eventos']:
        evento['id'] = max([e['id'] for e in data['eventos']]) + 1
    else:
        evento['id'] = 1
    
    data['eventos'].append(evento)
    save_data(data)
    return jsonify({"status": "success", "evento": evento})

# API - Atualizar evento (Protegida)
@app.route('/api/eventos/<int:evento_id>', methods=['PUT'])
@login_required
def update_evento(evento_id):
    """Atualiza um evento existente."""
    data = load_data()
    evento_data = request.json
    
    for i, evento in enumerate(data['eventos']):
        if evento['id'] == evento_id:
            # Preservar o ID ao atualizar
            evento_data['id'] = evento_id
            data['eventos'][i] = evento_data
            save_data(data)
            return jsonify({"status": "success", "evento": evento_data})
    
    return jsonify({"status": "error", "message": "Evento não encontrado"}), 404

# API - Deletar evento (Protegida)
@app.route('/api/eventos/<int:evento_id>', methods=['DELETE'])
@login_required
def delete_evento(evento_id):
    """Deleta um evento."""
    data = load_data()
    
    data['eventos'] = [e for e in data['eventos'] if e['id'] != evento_id]
    save_data(data)
    return jsonify({"status": "success", "message": "Evento deletado"})

# API - Upload de imagem (Protegida)
@app.route('/api/upload', methods=['POST'])
@login_required
def upload_file():
    """Faz upload de uma imagem."""
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Nenhum arquivo fornecido"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"status": "error", "message": "Nenhum arquivo selecionado"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"status": "error", "message": "Tipo de arquivo não permitido"}), 400
    
    filename = secure_filename(file.filename)
    # Adiciona timestamp ao nome para evitar conflitos
    filename = f"{datetime.now().timestamp()}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    return jsonify({
        "status": "success",
        "filename": filename,
        "url": f"/uploads/{filename}"
    })

# Servir arquivos de upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve arquivos de upload."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
