// sincronizador.js — versión optimizada
class Sincronizador {
    constructor(socket, estadoBell, gestorNodos,
                gestorConexiones, gestorImpulsos) {
        this.socket           = socket;
        this.estadoBell       = estadoBell;
        this.gestorNodos      = gestorNodos;
        this.gestorConexiones = gestorConexiones;
        this.gestorImpulsos   = gestorImpulsos;

        // Cola de activaciones para procesarlas
        // en lotes y no colapsar el render
        this._colaActivaciones = [];
        this._procesandoCola   = false;

        this._configurarEscuchas();
    }

    _configurarEscuchas() {

        this.socket.on('actualizar_nodo', (datos) => {
            const { nodo_id, estado } = datos;
            this.gestorNodos?.actualizarEstado(nodo_id, estado);
            document.dispatchEvent(new CustomEvent(
                'bell:nodo_actualizado', { detail: { nodo_id, estado } }
            ));
        });

        // Neurona activada — agregar a cola en vez de procesar inmediato
        this.socket.on('activar_neurona', (datos) => {
            this._colaActivaciones.push(datos);
            if (!this._procesandoCola) {
                this._procesarCola();
            }
        });

        this.socket.on('respuesta_bell', (datos) => {
            this._procesarRespuestaCompleta(datos);
            if (window.indicador) window.indicador.ocultar(300);
        });

        this.socket.on('estado_bell', (datos) => {
            if (datos.texto && window.indicador) {
                window.indicador.mostrar(datos.texto);
            }
        });
    }

    _procesarCola() {
        if (this._colaActivaciones.length === 0) {
            this._procesandoCola = false;
            return;
        }

        this._procesandoCola = true;

        // Procesar máximo 3 activaciones por frame
        // para no bloquear el render
        const lote = this._colaActivaciones.splice(0, 3);

        lote.forEach(datos => {
            this._activarNeurona(datos);
        });

        // Continuar en el siguiente frame
        requestAnimationFrame(() => this._procesarCola());
    }

    _activarNeurona(datos) {
        const { nodo_id, nivel, energia } = datos;

        const colores = {
            primario:   0xFFFFFF,
            secundario: 0x4A9EFF,
            terciario:  0x1A5FAB
        };
        const estados = {
            primario:   'procesando',
            secundario: 'activo',
            terciario:  'activo'
        };
        const delays = {
            primario:   2000,
            secundario: 1500,
            terciario:  1000
        };

        const color  = colores[nivel]  || 0x4A9EFF;
        const estado = estados[nivel]  || 'activo';
        const delay  = delays[nivel]   || 1000;

        // Actualizar nodo
        this.gestorNodos?.actualizarEstado(nodo_id, estado);

        // Solo lanzar ola para primarios y algunos secundarios
        // No lanzar ola para terciarios — muy costoso
        if (nivel === 'primario' && this.gestorImpulsos) {
            this.gestorImpulsos.lanzarOlaActivacion(nodo_id, color);
        } else if (nivel === 'secundario' && this.gestorImpulsos) {
            // Solo lanzar impulso directo, no ola completa
            this._lanzarImpulsoSimple(nodo_id, color);
        }

        // Volver a inactivo
        setTimeout(() => {
            this.gestorNodos?.actualizarEstado(nodo_id, 'inactivo');
        }, delay);

        document.dispatchEvent(new CustomEvent('bell:neurona_activada', {
            detail: { nodo_id, nivel, energia, color, estado }
        }));
    }

    _lanzarImpulsoSimple(nodoId, color) {
        // Impulso liviano — solo cambia el color del glow
        // sin recorrer todas las conexiones
        if (!this.gestorConexiones || !this.gestorImpulsos) return;

        // Tomar máximo 2 conexiones del nodo
        let contador = 0;
        this.gestorConexiones.conexiones.forEach((conn, connId) => {
            if (contador >= 2) return;
            if (conn.origenId === nodoId || conn.destinoId === nodoId) {
                this.gestorImpulsos.crearImpulso(connId, color, 0.15);
                contador++;
            }
        });
    }

    _procesarRespuestaCompleta(datos) {
        const capas = datos.capas_procesadas || [];
        capas.forEach((capaId, i) => {
            setTimeout(() => {
                this.gestorNodos?.actualizarEstado(capaId, 'activo');
                setTimeout(() => {
                    this.gestorNodos?.actualizarEstado(capaId, 'inactivo');
                }, 1000);
            }, i * 200);
        });

        document.dispatchEvent(new CustomEvent('bell:respuesta_completa', {
            detail: datos
        }));
    }

    procesarRespuesta(datos) {
        this._procesarRespuestaCompleta(datos);
    }
}

window.Sincronizador = Sincronizador;