// ================================================
// VISTA_FLUJO.JS v2
// FIX: buscaba datos.capas_existentes pero el API
// retorna datos.capas. Ahora usa el campo correcto
// y conecta las capas entre sí siempre.
// ================================================

class VistaFlujo extends BaseVista {
    constructor(motor3d) {
        super(motor3d, 'flujo');
    }

    construir() {
        fetch('/api/visualizacion/flujo')
            .then(r => r.json())
            .then(datos => {
                if (!datos.disponible) {
                    this._construirFallback();
                    return;
                }
                // FIX: el API retorna datos.capas, no datos.capas_existentes
                this._construirVisualizacion(datos.capas || []);
            })
            .catch(() => this._construirFallback());
    }

    _construirVisualizacion(capas) {
        if (!capas.length) {
            this._construirFallback();
            return;
        }

        const separacion = 14;
        const inicio     = -(capas.length - 1) * separacion / 2;

        // Colores por estado de capa
        const TIPO_POR_ESTADO = {
            activo:    'capa_flujo',
            inactivo:  'capa_flujo',
            pendiente: 'capa_flujo',
        };

        capas.forEach((capa, i) => {
            const x = inicio + i * separacion;
            this.agregarNodo({
                id:     capa.id,
                nombre: capa.nombre,
                tipo:   TIPO_POR_ESTADO[capa.estado] || 'capa_flujo',
                estado: capa.estado || 'pendiente',
                posicion: { x, y: 0, z: 0 },
            });

            // Conectar SIEMPRE con la capa anterior
            // (no solo cuando alguna existe — todas deben mostrarse conectadas)
            if (i > 0) {
                const anterior = capas[i - 1];
                this.agregarConexion(
                    `flujo_${i}`,
                    anterior.id,
                    capa.id,
                    capa.estado !== 'pendiente' ? 0.9 : 0.3
                );
            }
        });

        console.log(`[VistaFlujo] ${capas.length} capas renderizadas`);
    }

    _construirFallback() {
        // Fallback local si el API falla — muestra las 9 capas
        const capas = [
            { id: 'capa1', nombre: 'Capa 1 Recepcion',    estado: 'inactivo'  },
            { id: 'capa2', nombre: 'Capa 2 Activacion',   estado: 'inactivo'  },
            { id: 'capa3', nombre: 'Capa 3 Comprension',  estado: 'inactivo'  },
            { id: 'capa4', nombre: 'Capa 4 Evaluacion',   estado: 'pendiente' },
            { id: 'capa5', nombre: 'Capa 5 Deliberacion', estado: 'pendiente' },
            { id: 'capa6', nombre: 'Capa 6 Decision',     estado: 'pendiente' },
            { id: 'capa7', nombre: 'Capa 7 Ejecucion',    estado: 'pendiente' },
            { id: 'capa8', nombre: 'Capa 8 Expresion',    estado: 'pendiente' },
            { id: 'capa9', nombre: 'Capa 9 Integracion',  estado: 'pendiente' },
        ];
        this._construirVisualizacion(capas);
    }

    activarCapa(id)   { this.actualizarNodo(id, 'procesando'); }
    completarCapa(id) { this.actualizarNodo(id, 'activo');     }
    errorEnCapa(id)   { this.actualizarNodo(id, 'error');      }
}

window.VistaFlujo = VistaFlujo;