# Como Instalar e Executar no Seu Computador

## Windows

### 1. Instalar Python
- Baixe o Python em https://www.python.org/downloads/
- **Importante**: Marque a opção "Add Python to PATH" durante a instalação

### 2. Extrair os arquivos
- Extraia a pasta `calendario_gestao` em um local de sua preferência

### 3. Abrir o Prompt de Comando
- Pressione `Win + R`
- Digite `cmd` e pressione Enter
- Navegue até a pasta do projeto:
  ```
  cd C:\caminho\para\calendario_gestao
  ```

### 4. Criar ambiente virtual
```
python -m venv venv
```

### 5. Ativar o ambiente virtual
```
venv\Scripts\activate
```

### 6. Instalar dependências
```
pip install flask flask-cors python-dotenv pillow
```

### 7. Executar o servidor
```
python app.py
```

### 8. Acessar o site
- Abra seu navegador e acesse: **http://localhost:5000**
- Painel de Admin: **http://localhost:5000/admin**

---

## Mac/Linux

### 1. Instalar Python (se não tiver)
```bash
# Mac (com Homebrew)
brew install python3

# Linux (Ubuntu/Debian)
sudo apt-get install python3 python3-pip
```

### 2. Extrair os arquivos
```bash
cd ~/calendario_gestao
```

### 3. Criar ambiente virtual
```bash
python3 -m venv venv
```

### 4. Ativar o ambiente virtual
```bash
source venv/bin/activate
```

### 5. Instalar dependências
```bash
pip install flask flask-cors python-dotenv pillow
```

### 6. Executar o servidor
```bash
python3 app.py
```

### 7. Acessar o site
- Abra seu navegador e acesse: **http://localhost:5000**
- Painel de Admin: **http://localhost:5000/admin**

---

## Usando o Script (Mac/Linux)

Se preferir, pode usar o script fornecido:

```bash
cd ~/calendario_gestao
./run.sh
```

---

## Solução de Problemas

### Porta 5000 já está em uso
Se receber um erro dizendo que a porta 5000 está em uso:

1. **Windows**: Abra o Prompt de Comando como Administrador e execute:
   ```
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```

2. **Mac/Linux**: Execute:
   ```
   lsof -ti:5000 | xargs kill -9
   ```

### Python não é reconhecido
- Certifique-se de que Python foi adicionado ao PATH
- Reinicie o Prompt de Comando/Terminal

### Erro ao instalar dependências
- Certifique-se de que o ambiente virtual está ativado
- Tente: `pip install --upgrade pip`

---

## Parar o Servidor

Pressione `CTRL + C` no terminal onde o servidor está rodando.

---

## Dados

Os dados do calendário são armazenados em `data.json`. Você pode:
- Editar manualmente o arquivo
- Usar o painel de administração em http://localhost:5000/admin
- Fazer backup copiando o arquivo `data.json`

---

**Pronto! Seu calendário está funcionando localmente!** 🎉
