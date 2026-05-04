// ================================================
// CHAT.JS — Lógica completa del chat
// Envío y recepción de mensajes
// Historial de conversación
// Web Speech API para voz desde el navegador
// ================================================

class Chat {
    constructor(socket, indicador) {
        this.socket    = socket;
        this.indicador = indicador;
        this.historial = [];
        this.procesando = false;

        this.elementos = {
            historial:    document.getElementById('chat-historial'),
            input:        document.getElementById('chat-input'),
            botonEnviar:  document.getElementById('chat-enviar'),
            botonMic:     document.getElementById('chat-mic'),
        };

        this._voz = new GestorVozWeb(this);
        this._configurarEventos();
        this._configurarSocket();
    }

    _configurarEventos() {
        this.elementos.botonEnviar.addEventListener('click', () => {
            this._enviarMensaje();
        });

        this.elementos.input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this._enviarMensaje();
            }
        });

        this.elementos.input.addEventListener('input', () => {
            this._ajustarAlturaInput();
        });

        if (this.elementos.botonMic) {
            this.elementos.botonMic.addEventListener('click', () => {
                this._voz.toggle();
            });
        }
    }

    _configurarSocket() {
        this.socket.on('respuesta_bell', (datos) => {
            this.procesando = false;
            this._habilitarInput();
            this.indicador.ocultar();

            if (datos.respuesta) {
                this._agregarMensaje('bell', datos.respuesta);
            }

            if (window.sincronizador) {
                window.sincronizador.procesarRespuesta(datos);
            }
        });

        this.socket.on('estado_bell', (datos) => {
            if (datos.texto) {
                this.indicador.mostrar(datos.texto);
            }
        });
    }

    _enviarMensaje(textoForzado) {
        const texto = textoForzado || this.elementos.input.value.trim();
        if (!texto || this.procesando) return;

        // Limpiar bienvenida si existe
        const bienvenida = this.elementos.historial.querySelector('.mensaje-bienvenida');
        if (bienvenida) bienvenida.remove();

        this._agregarMensaje('sebastian', texto);

        this.elementos.input.value = '';
        this._ajustarAlturaInput();

        this.procesando = true;
        this._bloquearInput();
        this.indicador.mostrar('Recibiendo mensaje...');

        this.socket.emit('mensaje', { mensaje: texto });

        this.historial.push({ autor: 'sebastian', texto, timestamp: Date.now() });
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

        if (autor === 'bell') {
            this.historial.push({ autor: 'bell', texto, timestamp: Date.now() });
        }
    }

    _formatearTexto(texto) {
        return texto
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/\n/g, '<br>');
    }

    _scrollAlFinal() {
        this.elementos.historial.scrollTop = this.elementos.historial.scrollHeight;
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


// ── GESTOR VOZ WEB ────────────────────────────────────────
// Web Speech API — sin dependencias, nativo del navegador.
// Funciona en Chrome y Edge. En Firefox requiere flag.

class GestorVozWeb {
    constructor(chat) {
        this._chat       = chat;
        this._reconocedor = null;
        this._escuchando  = false;
        this._soportado   = false;
        this._boton       = document.getElementById('chat-mic');
        this._input       = document.getElementById('chat-input');

        this._inicializar();
    }

    _inicializar() {
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SR) {
            // Navegador no soporta Web Speech API — ocultar botón
            if (this._boton) {
                this._boton.style.display = 'none';
            }
            console.warn('[Voz] Web Speech API no disponible en este navegador.');
            return;
        }

        this._soportado   = true;
        this._reconocedor = new SR();

        // Configuración
        this._reconocedor.lang           = 'es-CO';
        this._reconocedor.continuous     = false;   // una frase por vez
        this._reconocedor.interimResults = true;    // mostrar texto mientras hablas

        // Eventos
        this._reconocedor.onstart = () => {
            this._escuchando = true;
            this._setEstado('escuchando');
        };

        this._reconocedor.onresult = (evento) => {
            // Construir transcripción
            let final    = '';
            let parcial  = '';

            for (let i = evento.resultIndex; i < evento.results.length; i++) {
                const texto = evento.results[i][0].transcript;
                if (evento.results[i].isFinal) {
                    final += texto;
                } else {
                    parcial += texto;
                }
            }

            // Mostrar texto en el input mientras habla
            this._input.value = final || parcial;
            this._chat._ajustarAlturaInput();
        };

        this._reconocedor.onend = () => {
            this._escuchando = false;
            this._setEstado('inactivo');

            // Auto-enviar si hay texto transcrito
            const texto = this._input.value.trim();
            if (texto && !this._chat.procesando) {
                // Pequeña pausa para que se vea el texto antes de enviar
                setTimeout(() => {
                    this._chat._enviarMensaje(texto);
                    this._input.value = '';
                }, 300);
            }
        };

        this._reconocedor.onerror = (evento) => {
            this._escuchando = false;
            this._setEstado('inactivo');

            // 'no-speech' es normal — el usuario no dijo nada
            if (evento.error !== 'no-speech' && evento.error !== 'aborted') {
                console.error('[Voz] Error:', evento.error);
            }
        };
    }

    toggle() {
        if (!this._soportado) return;

        if (this._escuchando) {
            this._reconocedor.stop();
        } else {
            // Limpiar input antes de escuchar
            this._input.value = '';
            this._chat._ajustarAlturaInput();
            try {
                this._reconocedor.start();
            } catch (e) {
                // Ya está corriendo — detener y reiniciar
                this._reconocedor.stop();
            }
        }
    }

    _setEstado(estado) {
        if (!this._boton) return;

        this._boton.classList.remove('escuchando', 'inactivo');
        this._boton.classList.add(estado);

        if (estado === 'escuchando') {
            this._boton.title = 'Escuchando... (clic para cancelar)';
            this._input.placeholder = 'Escuchando...';
        } else {
            this._boton.title = 'Hablar con Bell';
            this._input.placeholder = 'Habla con Bell...';
        }
    }
}

window.Chat         = Chat;
window.GestorVozWeb = GestorVozWeb;