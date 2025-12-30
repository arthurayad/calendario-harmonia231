import json
from pymongo import MongoClient
import certifi

# Configurações
MONGO_URI = "mongodb+srv://Harmonia231:harmonia231@cluster0.jdonuj2.mongodb.net/?appName=Cluster0"
DATA_FILE = 'data.json'

def migrar():
    ca = certifi.where()
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client['calendario_db']
        eventos_col = db['eventos']
        config_col = db['config']
        
        print(f"Lendo arquivo {DATA_FILE}...")
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'config' in data and data['config']:
            print("Migrando configurações...")
            config_col.replace_one({}, data['config'], upsert=True)
        
        if 'eventos' in data and data['eventos']:
            print(f"Migrando {len(data['eventos'])} eventos...")
            eventos_col.delete_many({})
            eventos_col.insert_many(data['eventos'])
        
        print("\nMigração concluída com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    migrar()
