// ================================================
// CHAT.JS — Lógica completa del chat
// Envío y recepción de mensajes
// Historial de conversación
// ================================================

class Chat {
    constructor(socket, indicador) {
        this.socket = socket;
        this.indicador = indicador;
        this.historial = [];
        this.procesando = false;

        this.elementos = {
            historial: document.getElementById('chat-historial'),
            input: document.getElementById('chat-input'),
            botonEnviar: document.getElementById('chat-enviar')
        };

        this._configurarEventos();
        this._configurarSocket();
        this._limpiarBienvenida();
    }

    _limpiarBienvenida() {
        // Se limpia cuando Bell responde por primera vez
        // No antes — para que se vea que está iniciando
    }

    _configurarEventos() {
        // Botón enviar
        this.elementos.botonEnviar.addEventListener('click', () => {
            this._enviarMensaje();
        });

        // Enter para enviar — Shift+Enter para nueva línea
        this.elementos.input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this._enviarMensaje();
            }
        });

        // Auto-resize del textarea
        this.elementos.input.addEventListener('input', () => {
            this._ajustarAlturaInput();
        });
    }

    _configurarSocket() {
        // Respuesta de Bell via WebSocket
        this.socket.on('respuesta_bell', (datos) => {
            this.procesando = false;
            this._habilitarInput();
            this.indicador.ocultar();

            if (datos.respuesta) {
                this._agregarMensaje('bell', datos.respuesta);
            }

            // Notificar al sincronizador sobre
            // los datos de procesamiento
            if (window.sincronizador) {
                window.sincronizador.procesarRespuesta(datos);
            }
        });

        // Estado de Bell mientras procesa
        this.socket.on('estado_bell', (datos) => {
            if (datos.texto) {
                this.indicador.mostrar(datos.texto);
            }
        });
    }

    _enviarMensaje() {
        const texto = this.elementos.input.value.trim();

        if (!texto || this.procesando) return;

        // Limpiar bienvenida si existe
        const bienvenida = this.elementos.historial
            .querySelector('.mensaje-bienvenida');
        if (bienvenida) bienvenida.remove();

        // Agregar mensaje de Sebastian
        this._agregarMensaje('sebastian', texto);

        // Limpiar input
        this.elementos.input.value = '';
        this._ajustarAlturaInput();

        // Bloquear mientras procesa
        this.procesando = true;
        this._bloquearInput();
        this.indicador.mostrar('Recibiendo mensaje...');

        // Enviar via WebSocket
        this.socket.emit('mensaje', { mensaje: texto });

        // Guardar en historial
        this.historial.push({
            autor: 'sebastian',
            texto: texto,
            timestamp: Date.now()
        });
    }

    _agregarMensaje(autor, texto) {
        const mensaje = document.createElement('div');
        mensaje.className = `mensaje ${autor}`;

        const nombreAutor = autor === 'bell' ? 'Bell' : 'Tú';

        mensaje.innerHTML = `
            <div class="mensaje-autor">${nombreAutor}</div>
            <div class="mensaje-contenido">${this._formatearTexto(texto)}</div>
        `;

        this.elementos.historial.appendChild(mensaje);
        this._scrollAlFinal();

        // Guardar si es de Bell
        if (autor === 'bell') {
            this.historial.push({
                autor: 'bell',
                texto: texto,
                timestamp: Date.now()
            });
        }
    }

    _formatearTexto(texto) {
        // Escapar HTML básico
        return texto
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/\n/g, '<br>');
    }

    _scrollAlFinal() {
        this.elementos.historial.scrollTop =
            this.elementos.historial.scrollHeight;
    }

    _ajustarAlturaInput() {
        const input = this.elementos.input;
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 120) + 'px';
    }

    _bloquearInput() {
        this.elementos.input.disabled = true;
        this.elementos.botonEnviar.disabled = true;
        this.elementos.botonEnviar.textContent = '...';
    }

    _habilitarInput() {
        this.elementos.input.disabled = false;
        this.elementos.botonEnviar.disabled = false;
        this.elementos.botonEnviar.textContent = 'Enviar';
        this.elementos.input.focus();
    }
}

window.Chat = Chat;