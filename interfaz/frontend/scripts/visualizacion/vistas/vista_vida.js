// ================================================
// VISTA_VIDA.JS — v2
// Corregido:
//   1. limpiar() elimina objetos directamente de la
//      escena Three.js (no del GestorNodos que no los conoce)
//   2. Raycaster propio para detectar clicks en esta vista
//   3. this.nodos.push() después de cada motor.agregar()
// ================================================

class VistaVida extends BaseVista {
    constructor(motor3d) {
        super(motor3d, 'vida');
        this.datosVida    = null;
        this._listeners   = [];
        this._nodosMalla  = new Map();  // id → mesh para raycasting
        this._objetos3d   = [];         // todos los objetos agregados a la escena
        this._raycaster   = new THREE.Raycaster();
        this._mouse       = new THREE.Vector2();
    }

    activar() {
        super.activar();
        this._configurarRaycaster();
        this._escucharActualizaciones();
        console.log('[VistaVida] activa');
    }

    desactivar() {
        // Quitar listeners
        this._listeners.forEach(({ tipo, fn }) =>
            document.removeEventListener(tipo, fn)
        );
        this._listeners = [];

        // Limpiar objetos directamente de la escena
        // (son THREE.Group creados por esta vista, no por GestorNodos)
        this._objetos3d.forEach(obj => {
            if (this.motor.escena) {
                this.motor.escena.remove(obj);
            }
            // Liberar geometrías y materiales
            obj.traverse(child => {
                if (child.geometry) child.geometry.dispose();
                if (child.material) {
                    if (Array.isArray(child.material))
                        child.material.forEach(m => m.dispose());
                    else
                        child.material.dispose();
                }
            });
        });
        this._objetos3d  = [];
        this._nodosMalla = new Map();
        this.nodos       = [];

        super.desactivar();
        console.log('[VistaVida] limpiada');
    }

    construir() {
        fetch('/api/visualizacion/vida')
            .then(r => r.json())
            .then(datos => {
                if (!datos.disponible || !datos.nodos?.length) {
                    this._construirVacia();
                    return;
                }
                this.datosVida = datos;
                this._construirTejidoVida(datos);
                this._mostrarEstadisticas(datos.estadisticas);
            })
            .catch(err => {
                console.error('[VistaVida] Error cargando datos:', err);
                this._construirVacia();
            });
    }

    _construirTejidoVida(datos) {
        const nodos     = datos.nodos || [];
        const posiciones = this._posicionesVida(nodos);
        nodos.forEach((nodo, i) => this._crearNodoVida(nodo, posiciones[i]));
        this._crearLeyenda();
        console.log(
            `[VistaVida] ${nodos.length} nodos | ` +
            `${datos.total_vivos ?? '?'} vivos | ` +
            `vitalidad prom: ${(datos.estadisticas?.vitalidad_promedio ?? 0).toFixed(3)}`
        );
    }

    _crearNodoVida(nodo, posicion) {
        const vitalidad = nodo.vitalidad  || 0;
        const nivel     = nodo.nivel_vida || 'dormida';
        const brilla    = nodo.brilla     || false;
        const colorHex  = this._hexToInt(nodo.color_vida || '#334455');

        const grupo = new THREE.Group();
        grupo.position.set(posicion.x, posicion.y, posicion.z);

        const radio = 0.4 + vitalidad * 1.2;

        // Núcleo
        const nucleo = new THREE.Mesh(
            new THREE.SphereGeometry(radio * 0.5, 10, 10),
            new THREE.MeshBasicMaterial({ color: colorHex, transparent: true, opacity: 0.9 })
        );
        grupo.add(nucleo);

        // Capa exterior — es la malla que detecta el raycaster
        const capa = new THREE.Mesh(
            new THREE.SphereGeometry(radio, 10, 10),
            new THREE.MeshPhongMaterial({
                color:             colorHex,
                emissive:          colorHex,
                emissiveIntensity: brilla ? vitalidad * 0.8 : 0.1,
                transparent:       true,
                opacity:           0.3 + vitalidad * 0.3,
                side:              THREE.DoubleSide,
            })
        );
        const userData = {
            id:                 nodo.id,
            nombre:             nodo.nombre,
            tipo:               nodo.tipo,
            estado:             'activo',
            vitalidad:          vitalidad,
            nivel_vida:         nivel,
            tipos_grounding:    nodo.tipos_grounding || [],
            grounding_efectivo: nodo.grounding_efectivo || 0,
        };
        capa.userData  = userData;
        grupo.userData = userData;
        grupo.add(capa);

        // Halo para nodos vivos
        if (brilla) {
            const halo = new THREE.Mesh(
                new THREE.SphereGeometry(radio * 2.0, 10, 10),
                new THREE.MeshBasicMaterial({
                    color:       colorHex,
                    transparent: true,
                    opacity:     vitalidad * 0.12,
                    side:        THREE.BackSide,
                })
            );
            grupo.add(halo);
        }

        // Anillo de grounding
        const tiposActivos = (nodo.tipos_grounding || []).length;
        if (tiposActivos > 0) {
            const ancho  = Math.min(1.5, tiposActivos * 0.08);
            const ring   = new THREE.Mesh(
                new THREE.RingGeometry(radio * 1.1, radio * 1.1 + ancho, 16),
                new THREE.MeshBasicMaterial({
                    color:       0x4A9EFF,
                    transparent: true,
                    opacity:     0.3 + (tiposActivos / 23) * 0.4,
                    side:        THREE.DoubleSide,
                })
            );
            ring.rotation.x = Math.PI / 2;
            grupo.add(ring);
        }

        // Registrar en escena directamente
        if (this.motor.escena) {
            this.motor.escena.add(grupo);
        } else {
            this.motor.agregar(grupo, `vida_${nodo.id}`);
        }
        this._objetos3d.push(grupo);
        this.nodos.push(nodo.id);
        this._nodosMalla.set(nodo.id, capa);

        if (brilla) this._animarPulso(grupo, vitalidad);
    }

    _posicionesVida(nodos) {
        const posiciones = new Array(nodos.length);
        const grupos = {
            plena: [], rica: [], funcional: [],
            emergente: [], latente: [], dormida: [],
        };
        nodos.forEach((n, i) => {
            const nivel = n.nivel_vida || 'dormida';
            (grupos[nivel] || grupos.dormida).push(i);
        });

        const capas = [
            { nivel: 'plena',     radio: 8,  offsetY:  20 },
            { nivel: 'rica',      radio: 20, offsetY:  10 },
            { nivel: 'funcional', radio: 35, offsetY:   0 },
            { nivel: 'emergente', radio: 52, offsetY: -10 },
            { nivel: 'latente',   radio: 70, offsetY: -20 },
            { nivel: 'dormida',   radio: 90, offsetY: -30 },
        ];
        const phi = Math.PI * (3 - Math.sqrt(5));

        capas.forEach(({ nivel, radio, offsetY }) => {
            const items = grupos[nivel] || [];
            if (!items.length) return;
            items.forEach((idx, pos) => {
                const total = items.length;
                const y  = total > 1 ? 1 - (pos / (total - 1)) * 2 : 0;
                const r  = Math.sqrt(Math.max(0, 1 - y * y));
                const th = phi * pos;
                const j  = () => (Math.random() - 0.5) * 4;
                posiciones[idx] = {
                    x: Math.cos(th) * r * radio + j(),
                    y: y * radio * 0.4 + offsetY + j() * 0.5,
                    z: Math.sin(th) * r * radio + j(),
                };
            });
        });

        nodos.forEach((_, i) => {
            if (!posiciones[i]) {
                posiciones[i] = {
                    x: (Math.random() - 0.5) * 100,
                    y: (Math.random() - 0.5) * 60,
                    z: (Math.random() - 0.5) * 40,
                };
            }
        });
        return posiciones;
    }

    _animarPulso(grupo, vitalidad) {
        if (!this._nodosPulsando) this._nodosPulsando = [];
        this._nodosPulsando.push({
            grupo,
            vitalidad,
            fase:      Math.random() * Math.PI * 2,
            velocidad: 0.5 + vitalidad * 0.8,
        });
    }

    _mostrarEstadisticas(stats) {
        if (!stats) return;
        const canvas = document.createElement('canvas');
        canvas.width = 512; canvas.height = 200;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = 'rgba(2,5,16,0.8)';
        ctx.fillRect(0, 0, 512, 200);
        ctx.font = 'bold 16px Inter,Arial';
        ctx.fillStyle = '#4A9EFF';
        ctx.fillText('VITALIDAD DE BELL', 20, 30);

        const niveles = [
            { nivel: 'plena',     color: '#00FF88', label: 'Plena'     },
            { nivel: 'rica',      color: '#44FFAA', label: 'Rica'      },
            { nivel: 'funcional', color: '#88FFCC', label: 'Funcional' },
            { nivel: 'emergente', color: '#AAFFDD', label: 'Emergente' },
            { nivel: 'latente',   color: '#FFD700', label: 'Latente'   },
            { nivel: 'dormida',   color: '#556677', label: 'Dormida'   },
        ];
        niveles.forEach(({ nivel, color, label }, i) => {
            const x = 20 + (i % 3) * 165;
            const y = 60 + Math.floor(i / 3) * 50;
            ctx.fillStyle = color;
            ctx.fillRect(x, y, 14, 14);
            ctx.fillStyle = '#AAAACC';
            ctx.font = '13px Inter,Arial';
            ctx.fillText(`${label}: ${stats[nivel] || 0}`, x + 20, y + 11);
        });
        ctx.fillStyle = '#7788AA';
        ctx.font = '12px Inter,Arial';
        ctx.fillText(
            `Vitalidad promedio: ${(stats.vitalidad_promedio || 0).toFixed(3)}`,
            20, 170
        );

        const sprite = new THREE.Sprite(
            new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(canvas), transparent: true, opacity: 0.85 })
        );
        sprite.scale.set(30, 12, 1);
        sprite.position.set(0, -55, 0);
        if (this.motor.escena) this.motor.escena.add(sprite);
        this._objetos3d.push(sprite);
    }

    _crearLeyenda() {
        const canvas = document.createElement('canvas');
        canvas.width = 240; canvas.height = 30;
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, 240, 30);
        ctx.font = '11px Inter,Arial';
        ctx.fillStyle = '#4A9EFF';
        ctx.fillText('● Anillo azul = grounding completo', 5, 20);

        const sprite = new THREE.Sprite(
            new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(canvas), transparent: true, opacity: 0.75 })
        );
        sprite.scale.set(20, 3, 1);
        sprite.position.set(0, -65, 0);
        if (this.motor.escena) this.motor.escena.add(sprite);
        this._objetos3d.push(sprite);
    }

    // ─── RAYCASTER PROPIO ────────────────────────────────────────────
    _configurarRaycaster() {
        const fnClick = (e) => {
            if (!this.activa) return;
            const canvas = document.getElementById('bell-canvas');
            if (!canvas) return;
            const rect = canvas.getBoundingClientRect();
            if (e.clientX < rect.left || e.clientX > rect.right ||
                e.clientY < rect.top  || e.clientY > rect.bottom) return;

            this._mouse.x = ((e.clientX - rect.left) / rect.width)  *  2 - 1;
            this._mouse.y = ((e.clientY - rect.top)  / rect.height) * -2 + 1;

            const camara = this.motor.obtenerCamara?.() || window.BellApp?.motor3d?.obtenerCamara?.();
            if (!camara) return;
            this._raycaster.setFromCamera(this._mouse, camara);

            const mallas = [...this._nodosMalla.values()];
            const hits   = this._raycaster.intersectObjects(mallas, false);
            if (hits.length > 0) {
                this._mostrarInfoNodo(hits[0].object.userData);
            }
        };
        document.addEventListener('click', fnClick);
        this._listeners.push({ tipo: 'click', fn: fnClick });
    }

    _mostrarInfoNodo(datos) {
        const panel = document.getElementById('nodo-info');
        if (!panel) return;
        document.getElementById('nodo-info-nombre').textContent = datos.nombre || datos.id;
        document.getElementById('nodo-info-tipo').textContent   = datos.tipo   || 'nodo';
        const v  = ((datos.vitalidad || 0) * 100).toFixed(0);
        const tg = (datos.tipos_grounding || []).length;
        document.getElementById('nodo-info-estado').textContent =
            `Estado: ${datos.estado || '?'} | Vida: ${datos.nivel_vida || '?'} (${v}%) | Grounding: ${tg}/23`;
        panel.classList.remove('oculto');
        document.getElementById('nodo-info-cerrar').onclick = () =>
            panel.classList.add('oculto');
    }

    _escucharActualizaciones() {
        const fn = (e) => {
            if (!this.activa) return;
            const { nodo_id, vitalidad, nivel_vida } = e.detail || {};
            if (nodo_id && vitalidad !== undefined)
                this._actualizarVitalidadNodo(nodo_id, vitalidad, nivel_vida);
        };
        document.addEventListener('bell:vitalidad_actualizada', fn);
        this._listeners.push({ tipo: 'bell:vitalidad_actualizada', fn });
    }

    _actualizarVitalidadNodo(nodo_id, vitalidad, nivel_vida) {
        const malla = this._nodosMalla.get(nodo_id);
        if (!malla) return;
        const colorHex = this._hexToInt(this._colorParaNivel(nivel_vida || 'dormida'));
        malla.material.color.setHex(colorHex);
        malla.material.emissive.setHex(colorHex);
        malla.material.emissiveIntensity = vitalidad * 0.8;
        malla.material.opacity = 0.3 + vitalidad * 0.3;
    }

    _colorParaNivel(nivel) {
        const c = {
            plena: '#00FF88', rica: '#44FFAA', funcional: '#88FFCC',
            emergente: '#AAFFDD', latente: '#FFD700', dormida: '#334455',
        };
        return c[nivel] || '#334455';
    }

    _hexToInt(hex) {
        return parseInt(hex.replace('#', ''), 16);
    }

    _construirVacia() {
        console.warn('[VistaVida] sin datos disponibles del servidor');
    }
}

window.VistaVida = VistaVida;