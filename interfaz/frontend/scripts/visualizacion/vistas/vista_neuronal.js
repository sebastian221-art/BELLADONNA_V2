// vista_neuronal.js — versión final con distribución completa
class VistaNeuronal extends BaseVista {
    constructor(motor3d) {
        super(motor3d, 'neuronal');
        this.datosRed  = null;
        this._listeners = [];
    }

    activar() {
        super.activar();
        this._escucharActivaciones();
    }

    desactivar() {
        this._listeners.forEach(({ tipo, fn }) => {
            document.removeEventListener(tipo, fn);
        });
        this._listeners = [];
        super.desactivar();
    }

    construir() {
        fetch('/api/visualizacion/neuronal')
            .then(r => r.json())
            .then(datos => {
                if (!datos.disponible || !datos.nodos?.length) {
                    this._construirVacia();
                    return;
                }
                this.datosRed = datos;
                this._construirTejido(datos);
                this._habilitarBoton();
            })
            .catch(() => this._construirVacia());
    }

    _construirTejido(datos) {
        const nodos      = datos.nodos      || [];
        const conexiones = datos.conexiones || [];
        const posiciones = this._posicionesOrganicas(nodos);

        // Crear nodos
        nodos.forEach((nodo, i) => {
            this.agregarNodo({
                id:       nodo.id,
                nombre:   nodo.nombre,
                tipo:     nodo.tipo,
                estado:   'inactivo',
                posicion: posiciones[i]
            });
        });

        // Crear solo conexiones relevantes — filtrar las de muy bajo peso
        // para reducir el ruido visual
        const conexionesFiltradas = conexiones.filter(
            c => (c.peso || 0) >= 0.4
        );

        conexionesFiltradas.forEach((conn, i) => {
            setTimeout(() => {
                this.agregarConexion(
                    conn.id, conn.origen,
                    conn.destino, conn.peso
                );
            }, i * 2);
        });

        setTimeout(() => this._animarEncendidoInicial(nodos), 800);

        console.log(
            `Tejido: ${nodos.length} neuronas, ` +
            `${conexionesFiltradas.length} sinapsis visibles`
        );
    }

    _posicionesOrganicas(nodos) {
        const posiciones = new Array(nodos.length);

        // Bell Core en el centro absoluto
        const iCore = nodos.findIndex(n => n.id === 'BELL_CORE');
        if (iCore >= 0) posiciones[iCore] = { x: 0, y: 0, z: 0 };

        // Clasificar todos los nodos por tipo
        const grupos = {};
        const tiposOrden = [
            'identidad', 'valor', 'consejera', 'relacion',
            'concepto', 'capacidad', 'habilidad',
            'capa_flujo', 'interfaz', 'cerebro',
            'fundacional', 'documentacion', 'desconocido', 'otros'
        ];

        tiposOrden.forEach(t => { grupos[t] = []; });

        nodos.forEach((nodo, i) => {
            if (i === iCore) return;
            const tipo = nodo.tipo || 'otros';
            if (grupos[tipo] !== undefined) {
                grupos[tipo].push(i);
            } else {
                grupos.otros.push(i);
            }
        });

        // Distribución en capas esféricas concéntricas
        // Cada grupo en su propio radio con su dispersión
        const capas = [
            { grupo: 'identidad',     radio: 14,  dispersion: 3,  offsetZ: 0   },
            { grupo: 'valor',         radio: 24,  dispersion: 5,  offsetZ: 5   },
            { grupo: 'consejera',     radio: 33,  dispersion: 5,  offsetZ: -5  },
            { grupo: 'relacion',      radio: 42,  dispersion: 6,  offsetZ: 0   },
            { grupo: 'concepto',      radio: 52,  dispersion: 8,  offsetZ: 7   },
            { grupo: 'capacidad',     radio: 60,  dispersion: 7,  offsetZ: -7  },
            { grupo: 'habilidad',     radio: 68,  dispersion: 8,  offsetZ: 0   },
            { grupo: 'capa_flujo',    radio: 76,  dispersion: 9,  offsetZ: 8   },
            { grupo: 'interfaz',      radio: 85,  dispersion: 10, offsetZ: -8  },
            { grupo: 'cerebro',       radio: 94,  dispersion: 10, offsetZ: 10  },
            { grupo: 'fundacional',   radio: 102, dispersion: 10, offsetZ: -10 },
            { grupo: 'documentacion', radio: 108, dispersion: 8,  offsetZ: 0   },
            { grupo: 'desconocido',   radio: 113, dispersion: 8,  offsetZ: 5   },
            { grupo: 'otros',         radio: 118, dispersion: 12, offsetZ: 0   },
        ];

        capas.forEach(({ grupo, radio, dispersion, offsetZ }) => {
            this._capaSferica(
                grupos[grupo] || [],
                posiciones, radio, dispersion, offsetZ
            );
        });

        // Rellenar sin posición
        nodos.forEach((_, i) => {
            if (!posiciones[i]) {
                posiciones[i] = {
                    x: (Math.random() - 0.5) * 130,
                    y: (Math.random() - 0.5) * 130,
                    z: (Math.random() - 0.5) * 50
                };
            }
        });

        return posiciones;
    }

    _capaSferica(items, posiciones, radio, dispersion, offsetZ = 0) {
        if (!items.length) return;
        // Distribución de Fibonacci — máxima uniformidad
        const phi = Math.PI * (3 - Math.sqrt(5));
        items.forEach((idx, pos) => {
            const y  = 1 - (pos / Math.max(items.length - 1, 1)) * 2;
            const r  = Math.sqrt(Math.max(0, 1 - y * y));
            const th = phi * pos;
            const j  = () => (Math.random() - 0.5) * dispersion;
            posiciones[idx] = {
                x: Math.cos(th) * r * radio + j(),
                y: y * radio + j(),
                z: Math.sin(th) * r * radio + offsetZ + j()
            };
        });
    }

    _animarEncendidoInicial(nodos) {
        // 1. Bell Core se enciende
        window.gestorNodos?.actualizarEstado('BELL_CORE', 'activo');
        window.gestorImpulsos?.lanzarOlaActivacion('BELL_CORE', 0x4A9EFF);

        // 2. Ola que se propaga capa por capa
        const orden = [
            'identidad', 'valor', 'consejera', 'relacion',
            'concepto', 'capacidad', 'habilidad',
            'capa_flujo', 'interfaz'
        ];

        let tiempoAcumulado = 400;

        orden.forEach((tipo) => {
            const grupo = nodos.filter(n => n.tipo === tipo);
            grupo.forEach((nodo, i) => {
                const t = tiempoAcumulado + i * 35;
                setTimeout(() => {
                    window.gestorNodos?.actualizarEstado(
                        nodo.id, 'activo'
                    );
                    // Impulsos solo cada 4 nodos para no saturar
                    if (i % 4 === 0 && window.gestorImpulsos) {
                        window.gestorImpulsos.lanzarOlaActivacion(
                            nodo.id, 0x3A7BD5
                        );
                    }
                }, t);
            });
            tiempoAcumulado += Math.max(grupo.length * 35, 250);
        });

        // 3. Volver a inactivo después de todo el encendido
        setTimeout(() => {
            nodos.forEach(nodo => {
                if (nodo.id !== 'BELL_CORE') {
                    window.gestorNodos?.actualizarEstado(
                        nodo.id, 'inactivo'
                    );
                }
            });
        }, tiempoAcumulado + 1500);
    }

    _escucharActivaciones() {
        // Nodo individual activado
        const fnNodo = (e) => {
            if (!this.activa) return;
            const { nodo_id, estado } = e.detail;
            window.gestorNodos?.actualizarEstado(nodo_id, estado);
            if ((estado === 'activo' || estado === 'procesando')
                && window.gestorImpulsos) {
                const color = estado === 'procesando'
                    ? 0xFFFFFF : 0x4A9EFF;
                window.gestorImpulsos.lanzarOlaActivacion(nodo_id, color);
            }
        };
        document.addEventListener('bell:nodo_actualizado', fnNodo);
        this._listeners.push({ tipo: 'bell:nodo_actualizado', fn: fnNodo });

        // Respuesta completa con red activa
        const fnRespuesta = (e) => {
            if (!this.activa) return;
            const redActiva = e.detail?.paquete_capa2?.red_activa;
            if (redActiva) this._activarCascada(redActiva);
        };
        document.addEventListener('bell:respuesta_completa', fnRespuesta);
        this._listeners.push({
            tipo: 'bell:respuesta_completa', fn: fnRespuesta
        });
    }

    _activarCascada(redActiva) {
        const primarios   = redActiva.nodos_primarios   || [];
        const secundarios = redActiva.nodos_secundarios || [];
        const terciarios  = redActiva.nodos_terciarios  || [];

        // Primarios — blanco puro, inmediato
        primarios.forEach((nodo, i) => {
            setTimeout(() => {
                window.gestorNodos?.actualizarEstado(
                    nodo.nodo_id, 'procesando'
                );
                window.gestorImpulsos?.lanzarOlaActivacion(
                    nodo.nodo_id, 0xFFFFFF
                );
            }, i * 100);
        });

        // Secundarios — azul brillante
        secundarios.forEach((nodo, i) => {
            setTimeout(() => {
                window.gestorNodos?.actualizarEstado(
                    nodo.nodo_id, 'activo'
                );
                window.gestorImpulsos?.lanzarOlaActivacion(
                    nodo.nodo_id, 0x4A9EFF
                );
            }, 400 + i * 70);
        });

        // Terciarios — solo color, sin ola
        terciarios.forEach((nodo, i) => {
            setTimeout(() => {
                window.gestorNodos?.actualizarEstado(
                    nodo.nodo_id, 'activo'
                );
            }, 900 + i * 50);
        });

        // Todo vuelve a inactivo
        const todos = [...primarios, ...secundarios, ...terciarios];
        setTimeout(() => {
            todos.forEach(nodo => {
                window.gestorNodos?.actualizarEstado(
                    nodo.nodo_id, 'inactivo'
                );
            });
        }, 4500);
    }

    _construirVacia() {
        this.agregarNodo({
            id: 'bell_core_vis', nombre: 'Belladonna',
            tipo: 'core', estado: 'warning',
            posicion: { x: 0, y: 0, z: 0 }
        });
    }

    _habilitarBoton() {
        const btn = document.querySelector('[data-vista="neuronal"]');
        if (btn) btn.classList.remove('deshabilitada');
    }
}

window.VistaNeuronal = VistaNeuronal;
