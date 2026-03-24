// ================================================
// VISTA_FLUJO.JS — El flujo de procesamiento
// Muestra las capas que existen
// Nunca inventa lo que no existe
// ================================================

class VistaFlujo extends BaseVista {
    constructor(motor3d) {
        super(motor3d, 'flujo');

        // Las capas del flujo en orden
        // Estado 'pendiente' = no existe aún
        this.capas = [
            { id: 'capa1', nombre: 'Capa 1\nRecepción', estado: 'pendiente' },
            { id: 'capa2', nombre: 'Capa 2\nActivación', estado: 'pendiente' },
            { id: 'capa3', nombre: 'Capa 3\nComprensión', estado: 'pendiente' },
            { id: 'capa4', nombre: 'Capa 4\nEvaluación', estado: 'pendiente' },
            { id: 'capa5', nombre: 'Capa 5\nDeliberación', estado: 'pendiente' },
            { id: 'capa6', nombre: 'Capa 6\nDecisión', estado: 'pendiente' },
            { id: 'capa7', nombre: 'Capa 7\nEjecución', estado: 'pendiente' },
            { id: 'capa8', nombre: 'Capa 8\nExpresión', estado: 'pendiente' },
            { id: 'capa9', nombre: 'Capa 9\nIntegración', estado: 'pendiente' }
        ];
    }

    construir() {
        // Verificar qué capas existen realmente
        this._verificarCapasExistentes()
            .then(() => this._construirVisualizacion());
    }

    async _verificarCapasExistentes() {
        try {
            const respuesta = await fetch('/api/visualizacion/estado');
            const datos = await respuesta.json();

            // Marcar las capas que existen
            if (datos.capas_existentes) {
                this.capas.forEach(capa => {
                    if (datos.capas_existentes.includes(capa.id)) {
                        capa.estado = 'inactivo';
                    }
                });
            }
        } catch (e) {
            // Si no hay datos dejar todas como pendiente
        }
    }

    _construirVisualizacion() {
        const separacion = 12;
        const inicio = -(this.capas.length - 1) * separacion / 2;

        this.capas.forEach((capa, indice) => {
            const x = inicio + indice * separacion;

            this.agregarNodo({
                id: capa.id,
                nombre: capa.nombre,
                tipo: 'capa',
                estado: capa.estado,
                posicion: { x, y: 0, z: 0 }
            });

            // Conectar con la capa anterior
            if (indice > 0) {
                const capaAnterior = this.capas[indice - 1];
                // Solo conectar si ambas capas existen
                if (capa.estado !== 'pendiente' ||
                    capaAnterior.estado !== 'pendiente') {
                    this.agregarConexion(
                        `flujo_${indice}`,
                        capaAnterior.id,
                        capa.id,
                        0.7
                    );
                }
            }
        });
    }

    activarCapa(id) {
        this.actualizarNodo(id, 'procesando');
    }

    completarCapa(id) {
        this.actualizarNodo(id, 'activo');
    }

    errorEnCapa(id) {
        this.actualizarNodo(id, 'error');
    }
}

window.VistaFlujo = VistaFlujo;