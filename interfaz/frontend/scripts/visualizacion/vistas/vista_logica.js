// ================================================
// VISTA_LOGICA.JS v2 — Cerebro lógico
// FIX: usaba /api/visualizacion/estado que NO tiene
// nodos. Ahora usa /api/visualizacion/neuronal.
// ================================================

class VistaLogica extends BaseVista {
    constructor(motor3d) {
        super(motor3d, 'logica');
        this.estructuraActual = null;
    }

    construir() {
        // FIX: el endpoint correcto es /neuronal, no /estado
        // /estado solo retorna { iniciada, consejeras_ok, estadisticas }
        // /neuronal retorna { nodos[], conexiones[] }
        fetch('/api/visualizacion/neuronal')
            .then(r => r.json())
            .then(datos => {
                if (!datos.disponible || !datos.nodos?.length) {
                    this._construirVacia();
                    return;
                }
                this.estructuraActual = datos;
                this._construirEstructura(datos);
            })
            .catch(() => this._construirVacia());
    }

    _construirEstructura(datos) {
        const nodos      = datos.nodos      || [];
        const conexiones = datos.conexiones || [];

        if (!nodos.length) {
            this._construirVacia();
            return;
        }

        // Clasificar por tipo
        const core      = nodos.filter(n => n.tipo === 'core' || n.id === 'BELL_CORE');
        const identidad = nodos.filter(n => n.tipo === 'identidad' && n.id !== 'BELL_CORE');
        const valores   = nodos.filter(n => n.tipo === 'valor');
        const consejeras = nodos.filter(n => n.tipo === 'consejera');
        const capas     = nodos.filter(n => n.tipo === 'capa' || n.tipo === 'capa_flujo');
        const conceptos = nodos.filter(n => n.tipo === 'concepto');
        const cerebro   = nodos.filter(n => n.tipo === 'cerebro');
        const interfaz  = nodos.filter(n => n.tipo === 'interfaz');
        const otros     = nodos.filter(n =>
            !['core','identidad','valor','consejera','capa','capa_flujo',
              'concepto','cerebro','interfaz'].includes(n.tipo) &&
            n.id !== 'BELL_CORE'
        );

        // BELL_CORE — centro absoluto
        const coreNodo = core[0] || { id: 'BELL_CORE', nombre: 'Belladonna', tipo: 'core' };
        this.agregarNodo({
            id: coreNodo.id, nombre: 'Belladonna',
            tipo: 'core', estado: 'activo',
            posicion: { x: 0, y: 0, z: 0 }
        });

        // Identidad — anillo interior muy cercano
        this._colocarEnAnillo(identidad, 12, 0);

        // Valores — anillo 2
        this._colocarEnAnillo(valores, 24, 3);

        // Consejeras — anillo 3
        this._colocarEnAnillo(consejeras, 36, -3);

        // Capas del flujo — línea horizontal abajo
        if (capas.length) {
            const sep   = 14;
            const start = -(capas.length - 1) * sep / 2;
            capas.forEach((n, i) => {
                this.agregarNodo({
                    id: n.id, nombre: n.nombre,
                    tipo: 'capa_flujo', estado: n.estado || 'inactivo',
                    posicion: { x: start + i * sep, y: -48, z: 0 }
                });
            });
        }

        // Conceptos — anillo externo
        this._colocarEnAnillo(conceptos, 55, 8);

        // Cerebro — anillo exterior
        this._colocarEnAnillo(cerebro, 70, -8);

        // Interfaz — anillo más exterior
        this._colocarEnAnillo(interfaz, 85, 5);

        // Otros — periferia
        this._colocarEnAnillo(otros, 95, 0);

        // Conexiones — solo las de peso alto para no saturar
        const consFiltradas = conexiones.filter(c => (c.peso || 0) >= 0.5);
        consFiltradas.forEach((conn, i) => {
            setTimeout(() => {
                this.agregarConexion(conn.id, conn.origen, conn.destino, conn.peso);
            }, i * 3);
        });

        console.log(`[VistaLogica] ${nodos.length} nodos, ${consFiltradas.length} conexiones visibles`);
    }

    _colocarEnAnillo(nodos, radio, offsetZ) {
        if (!nodos.length) return;
        const phi = Math.PI * (3 - Math.sqrt(5));
        nodos.forEach((n, i) => {
            const angulo = (i / nodos.length) * Math.PI * 2;
            const j = () => (Math.random() - 0.5) * 4;
            this.agregarNodo({
                id:     n.id,
                nombre: n.nombre,
                tipo:   n.tipo || 'concepto',
                estado: n.estado || 'inactivo',
                posicion: {
                    x: Math.cos(angulo) * radio + j(),
                    y: Math.sin(angulo) * radio * 0.6 + j(),
                    z: offsetZ + j() * 0.5,
                }
            });
        });
    }

    _construirVacia() {
        this.agregarNodo({
            id: 'BELL_CORE', nombre: 'Belladonna',
            tipo: 'core', estado: 'activo',
            posicion: { x: 0, y: 0, z: 0 }
        });
        console.warn('[VistaLogica] Sin datos del servidor, mostrando solo Bell Core');
    }

    actualizar(nuevosNodos) {
        if (!this.activa) return;
        nuevosNodos.forEach(n => {
            if (this.nodos.includes(n.id)) {
                this.actualizarNodo(n.id, n.estado);
            }
        });
    }
}

window.VistaLogica = VistaLogica;