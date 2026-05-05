// ================================================
// CHAT.JS — Lógica completa del chat
// Incluye:
//   - GestorVozWeb  → micrófono (SpeechRecognition)
//   - GestorVozPC   → Bell habla por parlantes (SpeechSynthesis)
//                     Voz femenina en español forzada
// ================================================

class Chat {
    constructor(socket, indicador) {
        this.socket     = socket;
        this.indicador  = indicador;
        this.historial  = [];
        this.procesando = false;

        this.elementos = {
            historial:   document.getElementById('chat-historial'),
            input:       document.getElementById('chat-input'),
            botonEnviar: document.getElementById('chat-enviar'),
            botonMic:    document.getElementById('chat-mic'),
            botonVoz:    document.getElementById('chat-voz-pc'),
        };

        this._vozPC  = new GestorVozPC();
        this._vozWeb = new GestorVozWeb(this);

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
                this._vozWeb.toggle();
            });
        }

        if (this.elementos.botonVoz) {
            this.elementos.botonVoz.addEventListener('click', () => {
                this._vozPC.toggleActiva();
                this._actualizarBotonVoz();
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
                this._vozPC.hablar(datos.respuesta);
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

    _actualizarBotonVoz() {
        const btn = this.elementos.botonVoz;
        if (!btn) return;
        if (this._vozPC.activa) {
            btn.classList.add('activo');
            btn.title = 'Bell habla — clic para silenciar';
        } else {
            btn.classList.remove('activo');
            btn.title = 'Bell en silencio — clic para activar voz';
        }
    }

    _enviarMensaje(textoForzado) {
        const texto = textoForzado || this.elementos.input.value.trim();
        if (!texto || this.procesando) return;

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


// ── VOZ PC (SpeechSynthesis) ──────────────────────────────
// Bell habla por los parlantes del PC.
// Busca específicamente voces femeninas en español.

class GestorVozPC {
    constructor() {
        this.activa     = true;
        this._soportado = 'speechSynthesis' in window;
        this._voz       = null;
        this._listo     = false;

        if (this._soportado) {
            // Las voces pueden cargar de forma asíncrona
            this._cargarVoz();
            window.speechSynthesis.onvoiceschanged = () => {
                this._cargarVoz();
            };
        }
    }

    _cargarVoz() {
        const voces = window.speechSynthesis.getVoices();
        if (!voces.length) return;

        // Imprimir voces disponibles para debug (solo la primera vez)
        if (!this._listo) {
            const vocesEs = voces.filter(v => v.lang.startsWith('es'));
            console.log('[Bell Voz] Voces en español disponibles:');
            vocesEs.forEach(v => console.log(`  ${v.name} | ${v.lang} | local: ${v.localService}`));
        }

        // Orden de preferencia — voces femeninas en español
        // Microsoft tiene las mejores en Windows
        const preferidas = [
            // Microsoft Neural (Windows 11)
            v => v.name.includes('Dalia'),         // es-MX femenina
            v => v.name.includes('Sabina'),       // es-MX femenina
            v => v.name.includes('Salome'),        // es-CO femenina
            v => v.name.includes('Elvira'),        // es-ES femenina
            v => v.name.includes('Laura'),         // es femenina
            v => v.name.includes('Paulina'),       // es-MX femenina
            v => v.name.includes('Monica'),        // es femenina
            v => v.name.includes('Conchita'),      // es-ES femenina
            v => v.name.includes('Camila'),        // es-US femenina
            // Genérico — cualquier voz femenina en español
            v => v.lang.startsWith('es') && (
                v.name.toLowerCase().includes('female') ||
                v.name.toLowerCase().includes('mujer') ||
                v.name.toLowerCase().includes('femenin')
            ),
            // Fallback — cualquier voz en español
            v => v.lang === 'es-CO',
            v => v.lang === 'es-MX',
            v => v.lang === 'es-ES',
            v => v.lang === 'es-US',
            v => v.lang.startsWith('es'),
        ];

        for (const filtro of preferidas) {
            const voz = voces.find(filtro);
            if (voz) {
                this._voz   = voz;
                this._listo = true;
                console.log(`[Bell Voz] Usando: ${voz.name} (${voz.lang})`);
                return;
            }
        }

        // Último recurso — primera voz disponible
        this._voz   = voces[0];
        this._listo = true;
        console.warn(`[Bell Voz] Sin voz en español — usando: ${voces[0].name}`);
    }

    hablar(texto) {
        if (!this._soportado || !this.activa || !texto) return;

        // Cancelar si está hablando algo
        window.speechSynthesis.cancel();

        // Pequeña pausa para que cancel() surta efecto
        setTimeout(() => {
            const frase    = new SpeechSynthesisUtterance(texto);
            frase.lang     = 'es-CO';
            frase.rate     = 1.0;
            frase.pitch    = 1.1;   // pitch ligeramente más alto → más femenino
            frase.volume   = 1.0;

            if (this._voz) {
                frase.voice = this._voz;
            }

            window.speechSynthesis.speak(frase);
        }, 50);
    }

    toggleActiva() {
        this.activa = !this.activa;
        if (!this.activa) {
            window.speechSynthesis.cancel();
        }
    }

    silenciar() {
        window.speechSynthesis.cancel();
    }
}


// ── VOZ WEB (SpeechRecognition) ───────────────────────────

class GestorVozWeb {
    constructor(chat) {
        this._chat        = chat;
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
            if (this._boton) this._boton.style.display = 'none';
            return;
        }

        this._soportado   = true;
        this._reconocedor = new SR();

        this._reconocedor.lang           = 'es-CO';
        this._reconocedor.continuous     = false;
        this._reconocedor.interimResults = true;

        this._reconocedor.onstart = () => {
            this._escuchando = true;
            this._setEstado('escuchando');
            // Silenciar a Bell mientras el usuario habla
            if (this._chat._vozPC) {
                this._chat._vozPC.silenciar();
            }
        };

        this._reconocedor.onresult = (evento) => {
            let final = '', parcial = '';
            for (let i = evento.resultIndex; i < evento.results.length; i++) {
                const texto = evento.results[i][0].transcript;
                if (evento.results[i].isFinal) final += texto;
                else parcial += texto;
            }
            this._input.value = final || parcial;
            this._chat._ajustarAlturaInput();
        };

        this._reconocedor.onend = () => {
            this._escuchando = false;
            this._setEstado('inactivo');
            const texto = this._input.value.trim();
            if (texto && !this._chat.procesando) {
                setTimeout(() => {
                    this._chat._enviarMensaje(texto);
                    this._input.value = '';
                }, 300);
            }
        };

        this._reconocedor.onerror = (evento) => {
            this._escuchando = false;
            this._setEstado('inactivo');
            if (evento.error !== 'no-speech' && evento.error !== 'aborted') {
                console.error('[Mic] Error:', evento.error);
            }
        };
    }

    toggle() {
        if (!this._soportado) return;
        if (this._escuchando) {
            this._reconocedor.stop();
        } else {
            this._input.value = '';
            this._chat._ajustarAlturaInput();
            try {
                this._reconocedor.start();
            } catch (e) {
                this._reconocedor.stop();
            }
        }
    }

    _setEstado(estado) {
        if (!this._boton) return;
        this._boton.classList.remove('escuchando', 'inactivo');
        this._boton.classList.add(estado);
        if (estado === 'escuchando') {
            this._boton.title       = 'Escuchando... (clic para cancelar)';
            this._input.placeholder = 'Escuchando...';
        } else {
            this._boton.title       = 'Hablar con Bell';
            this._input.placeholder = 'Habla con Bell...';
        }
    }
}

window.Chat         = Chat;
window.GestorVozPC  = GestorVozPC;
window.GestorVozWeb = GestorVozWeb;