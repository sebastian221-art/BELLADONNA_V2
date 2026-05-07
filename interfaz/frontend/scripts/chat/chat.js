// ================================================
// CHAT.JS — Lógica completa del chat v2
// Nuevas funciones:
//   - Detección automática de código pegado (Ctrl+V)
//   - Renderizado de bloques de código en el chat
//   - Input visual diferenciado: texto vs código
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
            this._actualizarEstiloInput();
        });

        // ── Detección de código pegado ────────────────────────
        this.elementos.input.addEventListener('paste', (e) => {
            // Leer el texto pegado
            const textoPegado = (e.clipboardData || window.clipboardData).getData('text');
            if (!textoPegado) return;

            if (this._esCodigoPython(textoPegado)) {
                e.preventDefault(); // Evitar el pegado normal

                const inputActual = this.elementos.input.value;
                const cursor      = this.elementos.input.selectionStart;

                // Si el input ya tiene texto (la instrucción), agregar el código como bloque
                if (inputActual.trim()) {
                    // Hay instrucción previa: agregar código como bloque separado
                    const separador  = inputActual.endsWith('\n') ? '' : '\n';
                    const bloqueCode = separador + '```python\n' + textoPegado.trim() + '\n```';
                    const nuevaPos   = inputActual.length + bloqueCode.length;

                    this.elementos.input.value = inputActual + bloqueCode;
                    this.elementos.input.setSelectionRange(nuevaPos, nuevaPos);
                } else {
                    // Input vacío: pegar directo como bloque de código
                    this.elementos.input.value = '```python\n' + textoPegado.trim() + '\n```';
                }

                this._ajustarAlturaInput();
                this._actualizarEstiloInput();

                // Mostrar tooltip brevemente
                this._mostrarTooltipCodigo();
            }
            // Si no es código, dejar el paste normal
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

        // ── Botón panel de código ─────────────────────────────
        const botonCodigo = document.getElementById('chat-codigo');
        if (botonCodigo) {
            botonCodigo.addEventListener('click', () => {
                this._abrirPanelCodigo();
            });
        }
    }

    _abrirPanelCodigo() {
        let panel = document.getElementById('bell-panel-codigo');
        if (!panel) {
            panel = this._crearPanelCodigo();
            document.body.appendChild(panel);
        }
        panel.style.display = 'flex';
        panel.querySelector('#panel-codigo-textarea').focus();
    }

    _crearPanelCodigo() {
        const panel = document.createElement('div');
        panel.id = 'bell-panel-codigo';
        panel.innerHTML = `
            <div class="panel-codigo-overlay" id="panel-overlay"></div>
            <div class="panel-codigo-modal">
                <div class="panel-codigo-header">
                    <span>{ } Pega tu código aquí</span>
                    <button class="panel-codigo-cerrar" id="panel-cerrar">✕</button>
                </div>
                <textarea
                    id="panel-codigo-textarea"
                    class="panel-codigo-area"
                    placeholder="Pega tu código Python aquí...&#10;&#10;Puede ser cualquier cantidad de líneas."
                    spellcheck="false"
                ></textarea>
                <div class="panel-codigo-footer">
                    <span class="panel-codigo-hint">Después de confirmar escribe tu instrucción en el chat</span>
                    <button class="panel-codigo-confirmar" id="panel-confirmar">Confirmar →</button>
                </div>
            </div>
        `;

        const cerrar = () => { panel.style.display = 'none'; };

        panel.querySelector('#panel-overlay').addEventListener('click', cerrar);
        panel.querySelector('#panel-cerrar').addEventListener('click', cerrar);
        panel.querySelector('#panel-confirmar').addEventListener('click', () => {
            const codigo = panel.querySelector('#panel-codigo-textarea').value.trim();
            if (!codigo) { cerrar(); return; }

            // Poner el código en el input envuelto en marcadores
            const marcador = '```python\n' + codigo + '\n```';
            const inputActual = this.elementos.input.value.trim();
            this.elementos.input.value = inputActual
                ? inputActual + '\n' + marcador
                : marcador;

            this.elementos.input.classList.add('input-con-codigo');
            this._ajustarAlturaInput();
            this.elementos.input.focus();

            // Limpiar panel
            panel.querySelector('#panel-codigo-textarea').value = '';
            cerrar();

            // Tooltip
            this._mostrarTooltipCodigo('✓ Código adjuntado — escribe tu instrucción y envía');
        });

        // Ctrl+Enter confirma
        panel.querySelector('#panel-codigo-textarea').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                panel.querySelector('#panel-confirmar').click();
            }
        });

        return panel;
    }

    _configurarSocket() {
        this.socket.on('respuesta_bell', (datos) => {
            this.procesando = false;
            this._habilitarInput();
            this.indicador.ocultar();

            if (datos.respuesta) {
                this._agregarMensaje('bell', datos.respuesta);
                this._vozPC.hablar(this._extraerTextoVoz(datos.respuesta));
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
        this.elementos.input.classList.remove('input-con-codigo');
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

    // ── Formateador de texto con soporte de código ────────────
    _formatearTexto(texto) {
        // Escapar HTML primero
        let html = texto
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

        // ── Bloques de código con backticks ──────────────────
        // ``` python o ``` bash → bloque de código con estilo
        html = html.replace(
            /```(?:python|py|bash|js|javascript|sql|json)?\s*\n?([\s\S]*?)```/g,
            (match, code) => {
                const codeEscapado = code.trim();
                return `<div class="bloque-codigo">
                    <div class="bloque-codigo-header">
                        <span class="bloque-codigo-icono">{ }</span>
                        <button class="bloque-codigo-copiar" onclick="navigator.clipboard.writeText(decodeURIComponent('${encodeURIComponent(codeEscapado)}'))">Copiar</button>
                    </div>
                    <pre class="bloque-codigo-contenido"><code>${codeEscapado}</code></pre>
                </div>`;
            }
        );

        // ── Código inline con backtick simple ─────────────────
        html = html.replace(
            /`([^`\n]+)`/g,
            '<code class="codigo-inline">$1</code>'
        );

        // ── Saltos de línea normales ───────────────────────────
        // Solo fuera de bloques de código (ya fueron reemplazados)
        html = html.replace(/\n/g, '<br>');

        return html;
    }

    // ── Detectar si texto pegado es código Python ─────────────
    _esCodigoPython(texto) {
        if (!texto || texto.length < 5) return false;

        // Ya tiene backticks → no procesar de nuevo
        if (texto.trim().startsWith('```')) return false;

        const señales = [
            /^\s*(def |class |import |from )\s*\w/m,
            /^\s*if\s+__name__\s*==\s*['"]/m,
            /Traceback\s*\(most recent call last\)/,
            /^\s*(try:|except\s*\w*:|finally:|with\s+)/m,
            /^\s*(for |while |async def |@\w+)\s*/m,
            /^\s*\w+Error:\s*\S+/m,
            /```\w*/,
        ];

        const lineasConIndentacion = texto.split('\n').filter(
            l => l.match(/^    \S/) || l.match(/^\t\S/)
        ).length;

        return señales.some(r => r.test(texto)) || lineasConIndentacion >= 2;
    }

    // ── Actualizar estilo visual del input según contenido ────
    _actualizarEstiloInput() {
        const val = this.elementos.input.value;
        if (val.includes('```')) {
            this.elementos.input.classList.add('input-con-codigo');
        } else {
            this.elementos.input.classList.remove('input-con-codigo');
        }
    }

    // ── Tooltip breve "código detectado" ──────────────────────
    _mostrarTooltipCodigo(texto) {
        let tip = document.getElementById('bell-tooltip-codigo');
        if (!tip) {
            tip = document.createElement('div');
            tip.id = 'bell-tooltip-codigo';
            tip.style.cssText = `
                position: fixed; bottom: 90px; left: 50%; transform: translateX(-50%);
                background: rgba(80,200,120,0.92); color: #000; padding: 6px 14px;
                border-radius: 8px; font-size: 13px; z-index: 9999;
                pointer-events: none; transition: opacity 0.3s;
            `;
            document.body.appendChild(tip);
        }
        tip.textContent = texto || '{ } Código detectado — agrega tu instrucción arriba';
        tip.style.opacity = '1';
        clearTimeout(this._tooltipTimer);
        clearTimeout(this._tooltipTimer);
        this._tooltipTimer = setTimeout(() => {
            tip.style.opacity = '0';
        }, 2500);
    }

    // ── Para voz: extraer solo el texto (sin código) ──────────
    _extraerTextoVoz(texto) {
        // Quitar bloques de código para que Bell no lea el código en voz
        return texto
            .replace(/```[\s\S]*?```/g, ' [ejemplo de código] ')
            .replace(/`[^`]+`/g, '')
            .trim();
    }

    _scrollAlFinal() {
        this.elementos.historial.scrollTop = this.elementos.historial.scrollHeight;
    }

    _ajustarAlturaInput() {
        const input = this.elementos.input;
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 180) + 'px';
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

class GestorVozPC {
    constructor() {
        this.activa     = true;
        this._soportado = 'speechSynthesis' in window;
        this._voz       = null;
        this._listo     = false;

        if (this._soportado) {
            this._cargarVoz();
            window.speechSynthesis.onvoiceschanged = () => {
                this._cargarVoz();
            };
        }
    }

    _cargarVoz() {
        const voces = window.speechSynthesis.getVoices();
        if (!voces.length) return;

        if (!this._listo) {
            const vocesEs = voces.filter(v => v.lang.startsWith('es'));
            console.log('[Bell Voz] Voces en español disponibles:');
            vocesEs.forEach(v => console.log(`  ${v.name} | ${v.lang} | local: ${v.localService}`));
        }

        const preferidas = [
            v => v.name.includes('Dalia'),
            v => v.name.includes('Sabina'),
            v => v.name.includes('Salome'),
            v => v.name.includes('Elvira'),
            v => v.name.includes('Laura'),
            v => v.name.includes('Paulina'),
            v => v.name.includes('Monica'),
            v => v.name.includes('Conchita'),
            v => v.name.includes('Camila'),
            v => v.lang.startsWith('es') && (
                v.name.toLowerCase().includes('female') ||
                v.name.toLowerCase().includes('mujer') ||
                v.name.toLowerCase().includes('femenin')
            ),
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

        this._voz   = voces[0];
        this._listo = true;
        console.warn(`[Bell Voz] Sin voz en español — usando: ${voces[0].name}`);
    }

    hablar(texto) {
        if (!this._soportado || !this.activa || !texto) return;
        window.speechSynthesis.cancel();
        setTimeout(() => {
            const frase    = new SpeechSynthesisUtterance(texto);
            frase.lang     = 'es-CO';
            frase.rate     = 1.0;
            frase.pitch    = 1.1;
            frase.volume   = 1.0;
            if (this._voz) frase.voice = this._voz;
            window.speechSynthesis.speak(frase);
        }, 50);
    }

    toggleActiva() {
        this.activa = !this.activa;
        if (!this.activa) window.speechSynthesis.cancel();
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
            if (this._chat._vozPC) this._chat._vozPC.silenciar();
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
            try { this._reconocedor.start(); }
            catch (e) { this._reconocedor.stop(); }
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