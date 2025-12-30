let allEventos = [];
let currentEditingEventoId = null;

// Carregar dados ao iniciar
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    loadData();
    setupNavigation();
    setupConfigForm();
    setupEventosForm();
    setupColorsForm();
});

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

// Navegação entre seções
function setupNavigation() {
    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const section = btn.dataset.section;
            
            // Remover active de todos os botões e seções
            navBtns.forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.admin-section').forEach(s => s.classList.remove('active'));
            
            // Adicionar active ao botão e seção clicados
            btn.classList.add('active');
            document.getElementById(section).classList.add('active');
            
            // Carregar dados específicos da seção
            if (section === 'eventos') {
                renderEventosList();
            }
        });
    });
}

// Carregar dados
async function loadData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        
        allEventos = data.eventos || [];
        
        // Carregar configurações
        if (data.config) {
            document.getElementById('title').value = data.config.title || '';
            document.getElementById('local').value = data.config.local || '';
            document.getElementById('contact').value = data.config.contact || '';
            
            // Carregar cor principal
            if (data.config.primaryColor) {
                const primaryColorInput = document.getElementById('color-primary');
                if (primaryColorInput) {
                    primaryColorInput.value = data.config.primaryColor;
                }
            }
            
            // Carregar cores
            if (data.config.colors) {
                for (const [key, value] of Object.entries(data.config.colors)) {
                    const input = document.getElementById(`color-${key}`);
                    if (input) {
                        input.value = value;
                    }
                }
            }
        }
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
        showMessage('config-message', 'Erro ao carregar dados', 'error');
    }
}

// ===== CONFIGURAÇÕES =====
function setupConfigForm() {
    const saveConfigBtn = document.getElementById('save-config-btn');
    const uploadLogoBtn = document.getElementById('upload-logo-btn');
    
    if (saveConfigBtn) {
        saveConfigBtn.addEventListener('click', saveConfig);
    }
    if (uploadLogoBtn) {
        uploadLogoBtn.addEventListener('click', uploadLogo);
    }
}

async function saveConfig() {
    // Buscar dados atuais para não perder a logo
    let currentData = {};
    try {
        const response = await fetch('/api/data');
        currentData = await response.json();
    } catch (e) {
        console.error("Erro ao buscar dados atuais", e);
    }

    const config = {
        title: document.getElementById('title').value,
        local: document.getElementById('local').value,
        contact: document.getElementById('contact').value,
        primaryColor: document.getElementById('color-primary').value,
        logo: currentData.config ? currentData.config.logo : '',
        colors: {
            estadual: document.getElementById('color-estadual').value,
            ritualistica: document.getElementById('color-ritualistica').value,
            entretenimento: document.getElementById('color-entretenimento').value,
            publica: document.getElementById('color-publica').value,
            feriado: document.getElementById('color-feriado').value
        }
    };

    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });

        if (response.ok) {
            showMessage('config-message', 'Configurações salvas com sucesso!', 'success');
            // Recarregar dados para atualizar o estado global
            loadData();
        } else {
            showMessage('config-message', 'Erro ao salvar configurações', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showMessage('config-message', 'Erro ao salvar configurações', 'error');
    }
}

async function uploadLogo() {
    const fileInput = document.getElementById('logo-file');
    const file = fileInput.files[0];

    if (!file) {
        showMessage('config-message', 'Selecione um arquivo', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.status === 'success') {
            // Mostrar preview
            const preview = document.getElementById('logo-preview');
            preview.innerHTML = `<img src="${data.url}" alt="Logo Preview" style="max-width: 100px; max-height: 100px;">`;
            
            // Salvar a URL da logo na configuração
            const config = {
                title: document.getElementById('title').value,
                local: document.getElementById('local').value,
                contact: document.getElementById('contact').value,
                primaryColor: document.getElementById('color-primary').value,
                logo: data.url,
                colors: {
                    estadual: document.getElementById('color-estadual').value,
                    ritualistica: document.getElementById('color-ritualistica').value,
                    entretenimento: document.getElementById('color-entretenimento').value,
                    publica: document.getElementById('color-publica').value,
                    feriado: document.getElementById('color-feriado').value,
                    sematividade: document.getElementById('color-sematividade').value
                }
            };
            
            const configResponse = await fetch('/api/config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(config)
            });
            
            if (configResponse.ok) {
                showMessage('config-message', 'Logo enviado e salvo com sucesso!', 'success');
            } else {
                showMessage('config-message', 'Logo enviado mas erro ao salvar', 'error');
            }
        } else {
            showMessage('config-message', 'Erro ao enviar logo', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showMessage('config-message', 'Erro ao enviar logo', 'error');
    }
}

// ===== EVENTOS =====
function setupEventosForm() {
    const modal = document.getElementById('evento-modal');
    const closeBtn = document.querySelector('.close');
    const addBtn = document.getElementById('add-evento-btn');
    const saveBtn = document.getElementById('save-evento-btn');
    const cancelBtn = document.getElementById('cancel-evento-btn');
    const deleteBtn = document.getElementById('delete-evento-btn');

    if (addBtn) {
        addBtn.addEventListener('click', () => {
            currentEditingEventoId = null;
            openEventoModal();
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', () => closeEventoModal());
    }
    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => closeEventoModal());
    }
    if (saveBtn) {
        saveBtn.addEventListener('click', saveEvento);
    }
    if (deleteBtn) {
        deleteBtn.addEventListener('click', deleteEvento);
    }

    if (modal) {
        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeEventoModal();
            }
        });
    }
}

function openEventoModal(eventoId = null) {
    const modal = document.getElementById('evento-modal');
    const modalTitle = document.getElementById('modal-title');
    const deleteBtn = document.getElementById('delete-evento-btn');

    if (eventoId !== null && eventoId !== undefined) {
        currentEditingEventoId = eventoId;
        const evento = allEventos.find(e => e.id === eventoId);
        
        if (!evento) {
            console.error('Evento não encontrado com ID:', eventoId);
            showMessage('evento-message', 'Evento não encontrado', 'error');
            return;
        }

        modalTitle.textContent = 'Editar Evento';
        document.getElementById('evento-titulo').value = evento.titulo || '';
        document.getElementById('evento-data').value = evento.data || '';
        document.getElementById('evento-hora').value = evento.hora || '';
        document.getElementById('evento-local').value = evento.local || '';
        document.getElementById('evento-categoria').value = evento.categoria || 'Ritualística';
        if (deleteBtn) {
            deleteBtn.style.display = 'block';
        }
    } else {
        currentEditingEventoId = null;
        modalTitle.textContent = 'Novo Evento';
        document.getElementById('evento-titulo').value = '';
        document.getElementById('evento-data').value = '';
        document.getElementById('evento-hora').value = '';
        document.getElementById('evento-local').value = '';
        document.getElementById('evento-categoria').value = 'Ritualística';
        if (deleteBtn) {
            deleteBtn.style.display = 'none';
        }
    }

    if (modal) {
        modal.classList.add('show');
    }
}

function closeEventoModal() {
    const modal = document.getElementById('evento-modal');
    if (modal) {
        modal.classList.remove('show');
    }
    const msgElement = document.getElementById('evento-message');
    if (msgElement) {
        msgElement.textContent = '';
        msgElement.classList.remove('show', 'success', 'error');
    }
}

async function saveEvento() {
    const titulo = document.getElementById('evento-titulo').value;
    const data = document.getElementById('evento-data').value;
    const hora = document.getElementById('evento-hora').value;
    const local = document.getElementById('evento-local').value;
    const categoria = document.getElementById('evento-categoria').value;

    if (!titulo || !data) {
        showMessage('evento-message', 'Preencha título e data', 'error');
        return;
    }

    const evento = {
        titulo,
        data,
        hora,
        local,
        categoria
    };

    try {
        let response;
        if (currentEditingEventoId !== null && currentEditingEventoId !== undefined) {
            // Editar evento existente
            response = await fetch(`/api/eventos/${currentEditingEventoId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(evento)
            });
        } else {
            // Criar novo evento
            response = await fetch('/api/eventos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(evento)
            });
        }

        if (response.ok) {
            const action = currentEditingEventoId !== null ? 'editado' : 'criado';
            showMessage('evento-message', `Evento ${action} com sucesso!`, 'success');
            setTimeout(() => {
                closeEventoModal();
                loadData();
                renderEventosList();
            }, 1000);
        } else {
            const errorData = await response.json();
            console.error('Erro na resposta:', errorData);
            showMessage('evento-message', 'Erro ao salvar evento', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showMessage('evento-message', 'Erro ao salvar evento', 'error');
    }
}

async function deleteEvento() {
    if (!confirm('Tem certeza que deseja deletar este evento?')) {
        return;
    }

    if (currentEditingEventoId === null || currentEditingEventoId === undefined) {
        showMessage('evento-message', 'Nenhum evento selecionado para deletar', 'error');
        return;
    }

    try {
        const response = await fetch(`/api/eventos/${currentEditingEventoId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showMessage('evento-message', 'Evento deletado com sucesso!', 'success');
            setTimeout(() => {
                closeEventoModal();
                loadData();
                renderEventosList();
            }, 1000);
        } else {
            showMessage('evento-message', 'Erro ao deletar evento', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showMessage('evento-message', 'Erro ao deletar evento', 'error');
    }
}

function renderEventosList() {
    const container = document.getElementById('eventos-list');
    if (!container) return;
    
    container.innerHTML = '';

    // Ordenar eventos por data
    const sorted = [...allEventos].sort((a, b) => new Date(a.data) - new Date(b.data));

    sorted.forEach(evento => {
        const date = new Date(evento.data);
        const day = date.getDate();
        const month = date.toLocaleString('pt-BR', { month: 'short' });

        const card = document.createElement('div');
        card.className = 'evento-card';
        card.innerHTML = `
            <div class="evento-card-date">${day} ${month}</div>
            <div class="evento-card-title">${evento.titulo}</div>
            <div class="evento-card-category">${evento.categoria}</div>
            <div class="evento-card-info">
                <div>⏰ ${evento.hora || 'Sem hora'}</div>
                <div>📍 ${evento.local || 'Sem local'}</div>
            </div>
            <div class="evento-card-buttons">
                <button class="btn btn-primary" onclick="openEventoModal(${evento.id})">Editar</button>
                <button class="btn btn-danger" onclick="deleteEventoQuick(${evento.id})">Deletar</button>
            </div>
        `;
        container.appendChild(card);
    });
}

async function deleteEventoQuick(eventoId) {
    if (!confirm('Tem certeza que deseja deletar este evento?')) {
        return;
    }

    try {
        const response = await fetch(`/api/eventos/${eventoId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadData();
            renderEventosList();
        } else {
            alert('Erro ao deletar evento');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao deletar evento');
    }
}

// ===== CORES =====
function setupColorsForm() {
    const saveColorsBtn = document.getElementById('save-colors-btn');
    if (saveColorsBtn) {
        saveColorsBtn.addEventListener('click', saveColors);
    }
}

async function saveColors() {
    // Reutiliza a lógica de saveConfig para garantir consistência
    await saveConfig();
    showMessage('colors-message', 'Cores salvas com sucesso!', 'success');
}

// Utilidades
function showMessage(elementId, text, type) {
    const element = document.getElementById(elementId);
    if (!element) {
        console.warn(`Elemento com ID ${elementId} não encontrado`);
        return;
    }
    element.textContent = text;
    element.className = `message show ${type}`;
    setTimeout(() => {
        element.classList.remove('show');
    }, 3000);
}
