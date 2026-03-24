// ================================================
// VISTA_LOGICA.JS — Cerebro lógico tecnológico
// Estructura de archivos clara y limpia
// Conexiones por imports visibles
// ================================================

class VistaLogica extends BaseVista {
    constructor(motor3d) {
        super(motor3d, 'logica');
        this.estructuraActual = null;
    }

    construir() {
        fetch('/api/visualizacion/estado')
            .then(r => r.json())
            .then(datos => {
                this.estructuraActual = datos;
                this._construirEstructura(datos);
            })
            .catch(() => this._construirVacia());
    }

    _construirEstructura(datos) {
        if (!datos.nodos?.length) {
            this._construirVacia();
            return;
        }

        // Separar por tipo para layout limpio
        const core      = datos.nodos.filter(n => n.tipo === 'core');
        const capas     = datos.nodos.filter(n => n.tipo === 'capa');
        const carpetas  = datos.nodos.filter(n =>
            n.tipo === 'carpeta' && n.tipo !== 'capa'
        );
        const archivos  = datos.nodos.filter(n =>
            n.tipo === 'archivo'
        );
        const otros     = datos.nodos.filter(n =>
            !['core','capa','carpeta','archivo'].includes(n.tipo)
        );

        // CORE — centro
        core.forEach(n => {
            this.agregarNodo({
                id: n.id,
                nombre: n.nombre === 'Bell' ? 'Belladonna' : n.nombre,
                tipo: 'core', estado: n.estado || 'activo',
                posicion: { x: 0, y: 0, z: 0 }
            });
        });

        // CAPAS — línea horizontal
        const separacionCapa = 14;
        const inicioCapa = -(capas.length - 1) * separacionCapa / 2;
        capas.forEach((n, i) => {
            this.agregarNodo({
                id: n.id, nombre: n.nombre, tipo: 'capa',
                estado: n.estado || 'inactivo',
                posicion: {
                    x: inicioCapa + i * separacionCapa,
                    y: -30,
                    z: 0
                }
            });
        });

        // CARPETAS — anillo medio
        const posCarpetas = this._anilloLimpio(carpetas.length, 28, 0);
        carpetas.forEach((n, i) => {
            this.agregarNodo({
                id: n.id, nombre: n.nombre, tipo: 'carpeta',
                estado: n.estado || 'inactivo',
                posicion: posCarpetas[i]
            });
        });

        // ARCHIVOS — agrupados cerca de su carpeta
        const posArchivos = this._anilloLimpio(archivos.length, 50, 0);
        archivos.forEach((n, i) => {
            this.agregarNodo({
                id: n.id, nombre: n.nombre,
                tipo: this._tipoArchivo(n.nombre),
                estado: n.estado || 'inactivo',
                posicion: posArchivos[i]
            });
        });

        // OTROS
        const posOtros = this._anilloLimpio(otros.length, 38, 15);
        otros.forEach((n, i) => {
            this.agregarNodo({
                id: n.id, nombre: n.nombre,
                tipo: n.tipo || 'concepto',
                estado: n.estado || 'inactivo',
                posicion: posOtros[i]
            });
        });

        // Conexiones
        if (datos.conexiones) {
            datos.conexiones.forEach(conn => {
                this.agregarConexion(
                    conn.id, conn.origen, conn.destino, conn.peso
                );
            });
        }
    }

    _anilloLimpio(cantidad, radio, offsetZ) {
        const pos = [];
        for (let i = 0; i < cantidad; i++) {
            const angulo = (i / cantidad) * Math.PI * 2;
            const jitterZ = (Math.random() - 0.5) * 10;
            pos.push({
                x: Math.cos(angulo) * radio,
                y: Math.sin(angulo) * radio,
                z: offsetZ + jitterZ
            });
        }
        return pos;
    }

    _tipoArchivo(nombre) {
        if (!nombre) return 'archivo';
        if (nombre.endsWith('.py'))  return 'archivo';
        if (nombre.endsWith('.js'))  return 'archivo';
        if (nombre.endsWith('.css')) return 'archivo';
        if (nombre.endsWith('.md'))  return 'archivo';
        if (nombre.endsWith('.html'))return 'archivo';
        return 'archivo';
    }

    _construirVacia() {
        this.agregarNodo({
            id: 'bell_core', nombre: 'Belladonna',
            tipo: 'core', estado: 'activo',
            posicion: { x: 0, y: 0, z: 0 }
        });
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
