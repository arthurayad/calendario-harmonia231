# Calendário Gestão 2026/A

Um calendário de eventos interativo com painel de administração completo, desenvolvido em Python com Flask.

## Características

- ✅ **Calendário Interativo**: Visualize eventos em um calendário mensal
- ✅ **Filtro por Categoria**: Filtre eventos por tipo (Estadual, Ritualística, Entretenimento, Pública)
- ✅ **Exibição de Horários e Local**: Cada evento mostra hora e local
- ✅ **Painel de Administração Funcional**: Controle total sobre o conteúdo
- ✅ **Gerenciamento de Eventos**: Criar, editar e deletar eventos
- ✅ **Personalização de Cores**: Altere as cores de cada categoria
- ✅ **Configurações Gerais**: Modifique título, local, contato e logo
- ✅ **Responsivo**: Funciona em desktop, tablet e mobile

## Requisitos

- Python 3.7+
- pip (gerenciador de pacotes Python)

## Instalação e Execução

### Opção 1: Usando o script (Recomendado)

```bash
cd calendario_gestao
./run.sh
```

### Opção 2: Execução manual

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install flask flask-cors python-dotenv pillow

# Executar servidor
python3 app.py
```

## Acesso

- **Site Principal**: http://localhost:5000
- **Painel de Admin**: http://localhost:5000/admin

## Estrutura do Projeto

```
calendario_gestao/
├── app.py                 # Servidor Flask
├── data.json             # Dados dos eventos e configurações
├── run.sh                # Script para executar
├── templates/
│   ├── index.html        # Página principal
│   └── admin.html        # Painel de administração
├── static/
│   ├── css/
│   │   ├── style.css     # Estilos da página principal
│   │   └── admin.css     # Estilos do painel admin
│   └── js/
│       ├── calendar.js   # Lógica do calendário
│       └── admin.js      # Lógica do painel admin
├── uploads/              # Pasta para imagens enviadas
└── venv/                 # Ambiente virtual Python
```

## Funcionalidades do Painel Admin

### 1. Configurações Gerais
- Alterar título do site
- Modificar local das reuniões
- Atualizar informações de contato
- Fazer upload de logo

### 2. Gerenciar Eventos
- Criar novos eventos
- Editar eventos existentes
- Deletar eventos
- Definir data, hora, local e categoria

### 3. Personalizar Cores
- Alterar cores de cada categoria
- Visualizar alterações em tempo real

## Dados

Os dados são armazenados em `data.json` no formato JSON. Você pode:
- Editar manualmente o arquivo JSON
- Usar o painel de administração para gerenciar dados
- Fazer backup dos dados copiando o arquivo `data.json`

## Categorias de Eventos

- **Estadual**: Eventos estaduais (azul escuro)
- **Ritualística**: Eventos ritualísticos (verde)
- **Entretenimento**: Eventos de entretenimento (bege)
- **Pública**: Eventos públicos (verde-azulado)
- **Feriado**: Feriados (vermelho)
- **Sem Atividade**: Dias sem atividades (cinza escuro)

## Troubleshooting

### Porta 5000 já está em uso
Se a porta 5000 já está sendo usada, você pode:
1. Parar o processo que está usando a porta
2. Modificar a porta no arquivo `app.py` (linha final: `app.run(port=5001)`)

### Erro ao instalar dependências
Certifique-se de que você está no ambiente virtual ativado:
```bash
source venv/bin/activate
pip install flask flask-cors python-dotenv pillow
```

### Imagens não aparecem
Certifique-se de que o arquivo `logo.jfif` está no diretório raiz do projeto.

## Suporte

Para questões ou problemas, verifique:
1. Se o servidor está rodando (`python3 app.py`)
2. Se está acessando a URL correta (http://localhost:5000)
3. Se o arquivo `data.json` existe e está válido

## Licença

Este projeto é de uso livre.

---

**Desenvolvido com ❤️ para o Calendário Gestão 2026/A**
