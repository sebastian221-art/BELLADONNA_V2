// ================================================
// ESTADO_BELL.JS — Estado actual de Bell
// Se actualiza en tiempo real via WebSocket
// ================================================

class EstadoBell {
    constructor(socket) {
        this.socket = socket;
        this.estado = {
            global: 'iniciando',
            capaActiva: null,
            nodosActivos: new Set(),
            ultimaActualizacion: null
        };

        this._escucharEventos();
    }

    _escucharEventos() {
        // Estado general de Bell
        this.socket.on('estado_bell', (datos) => {
            this.estado.global = datos.estado;
            this.estado.ultimaActualizacion = Date.now();

            // Notificar a quien escuche
            this._emitirCambio('estado_global', datos);
        });

        // Nodo activado
        this.socket.on('actualizar_nodo', (datos) => {
            if (datos.estado === 'procesando' ||
                datos.estado === 'activo') {
                this.estado.nodosActivos.add(datos.nodo_id);
            } else {
                this.estado.nodosActivos.delete(datos.nodo_id);
            }

            this._emitirCambio('nodo_actualizado', datos);
        });

        // Estado completo de la red
        this.socket.on('estado_red', (datos) => {
            this._emitirCambio('red_actualizada', datos);
        });
    }

    _emitirCambio(tipo, datos) {
        // Emitir evento personalizado para que
        // otros módulos puedan escuchar
        const evento = new CustomEvent(`bell:${tipo}`, {
            detail: datos
        });
        document.dispatchEvent(evento);
    }

    obtenerEstado() {
        return { ...this.estado };
    }
}

window.EstadoBell = EstadoBell;