// ================================================
// VISTA_VIDA.JS — La vista de vida de Bell
// Muestra qué tan vivo está cada elemento
// Verde brillante = vida plena
// Dorado = vida latente
// Gris = dormido
// Cada neurona brilla según su vitalidad
// ================================================

class VistaVida extends BaseVista {
    constructor(motor3d) {
        super(motor3d, 'vida');
        this.datosVida = null;
        this._listeners = [];
        this._nodosMalla = new Map(); // id → mesh para raycasting
    }

    activar() {
        super.activar();
        this._escucharActualizaciones();
        console.log('Vista de vida activa');
    }

    desactivar() {
        this._listeners.forEach(({ tipo, fn }) => {
            document.removeEventListener(tipo, fn);
        });
        this._listeners = [];
        this._nodosMalla.clear();
        super.desactivar();
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
            .catch(() => this._construirVacia());
    }

    _construirTejidoVida(datos) {
        const nodos = datos.nodos || [];
        const posiciones = this._posicionesVida(nodos);

        nodos.forEach((nodo, i) => {
            this._crearNodoVida(nodo, posiciones[i]);
        });

        // Leyenda de vida
        this._crearLeyenda();

        console.log(
            `Vista vida: ${nodos.length} nodos, ` +
            `${datos.total_vivos} vivos, ` +
            `vitalidad promedio: ${datos.estadisticas?.vitalidad_promedio?.toFixed(3)}`
        );
    }

    _crearNodoVida(nodo, posicion) {
        const vitalidad  = nodo.vitalidad || 0;
        const nivel      = nodo.nivel_vida || 'dormida';
        const brilla     = nodo.brilla || false;
        const colorHex   = this._hexToInt(nodo.color_vida || '#334455');

        const grupo = new THREE.Group();
        grupo.position.set(posicion.x, posicion.y, posicion.z);

        // Radio según vitalidad — más vivo = más grande
        const radio = 0.4 + vitalidad * 1.2;

        // ---- NÚCLEO ----
        const geoNucleo = new THREE.SphereGeometry(radio * 0.5, 10, 10);
        const matNucleo = new THREE.MeshBasicMaterial({
            color: colorHex, transparent: true, opacity: 0.9
        });
        const nucleo = new THREE.Mesh(geoNucleo, matNucleo);
        grupo.add(nucleo);

        // ---- CAPA EXTERIOR ----
        const geoCapa = new THREE.SphereGeometry(radio, 10, 10);
        const matCapa = new THREE.MeshPhongMaterial({
            color:             colorHex,
            emissive:          colorHex,
            emissiveIntensity: brilla ? vitalidad * 0.8 : 0.1,
            transparent:       true,
            opacity:           0.3 + vitalidad * 0.3,
            side:              THREE.DoubleSide
        });
        const capa = new THREE.Mesh(geoCapa, matCapa);
        grupo.add(capa);

        // ---- HALO — solo si está vivo ----
        if (brilla) {
            const geoHalo = new THREE.SphereGeometry(radio * 2.0, 10, 10);
            const matHalo = new THREE.MeshBasicMaterial({
                color:       colorHex,
                transparent: true,
                opacity:     vitalidad * 0.12,
                side:        THREE.BackSide
            });
            const halo = new THREE.Mesh(geoHalo, matHalo);
            grupo.add(halo);
        }

        // ---- ANILLO DE GROUNDING ----
        // Cuántos tipos de grounding tiene activos
        const tiposActivos = (nodo.tipos_grounding || []).length;
        if (tiposActivos > 0) {
            const ancho  = Math.min(1.5, tiposActivos * 0.08);
            const geoRing = new THREE.RingGeometry(
                radio * 1.1, radio * 1.1 + ancho, 16
            );
            const matRing = new THREE.MeshBasicMaterial({
                color:       0x4A9EFF,
                transparent: true,
                opacity:     0.3 + (tiposActivos / 23) * 0.4,
                side:        THREE.DoubleSide
            });
            const ring = new THREE.Mesh(geoRing, matRing);
            ring.rotation.x = Math.PI / 2;
            grupo.add(ring);
        }

        // Datos para interacción
        const userData = {
            id:         nodo.id,
            nombre:     nodo.nombre,
            tipo:       nodo.tipo,
            vitalidad:  vitalidad,
            nivel_vida: nivel,
            tipos_grounding: nodo.tipos_grounding || [],
            grounding_efectivo: nodo.grounding_efectivo || 0,
        };
        grupo.userData = userData;
        capa.userData  = userData;

        this.motor.agregar(grupo, `vida_${nodo.id}`);
        this.nodos.push(nodo.id);
        this._nodosMalla.set(nodo.id, capa);

        // Animación de pulso para nodos vivos
        if (brilla) {
            this._animarPulso(grupo, vitalidad);
        }
    }

    _posicionesVida(nodos) {
        const posiciones = new Array(nodos.length);

        // Agrupar por nivel de vida
        const grupos = {
            plena:     [], rica:      [], funcional: [],
            emergente: [], latente:   [], dormida:   [],
        };
        nodos.forEach((n, i) => {
            const nivel = n.nivel_vida || 'dormida';
            if (grupos[nivel]) grupos[nivel].push(i);
            else grupos.dormida.push(i);
        });

        // Capas concéntricas — los más vivos al centro
        const capas = [
            { nivel: 'plena',     radio: 8,   offsetY:  20 },
            { nivel: 'rica',      radio: 20,  offsetY:  10 },
            { nivel: 'funcional', radio: 35,  offsetY:   0 },
            { nivel: 'emergente', radio: 52,  offsetY: -10 },
            { nivel: 'latente',   radio: 70,  offsetY: -20 },
            { nivel: 'dormida',   radio: 90,  offsetY: -30 },
        ];

        const phi = Math.PI * (3 - Math.sqrt(5));

        capas.forEach(({ nivel, radio, offsetY }) => {
            const items = grupos[nivel] || [];
            items.forEach((idx, pos) => {
                const y  = 1 - (pos / Math.max(items.length - 1, 1)) * 2;
                const r  = Math.sqrt(Math.max(0, 1 - y * y));
                const th = phi * pos;
                const j  = () => (Math.random() - 0.5) * 4;
                posiciones[idx] = {
                    x: Math.cos(th) * r * radio + j(),
                    y: y * radio * 0.4 + offsetY + j() * 0.5,
                    z: Math.sin(th) * r * radio + j()
                };
            });
        });

        // Rellenar sin posición
        nodos.forEach((_, i) => {
            if (!posiciones[i]) {
                posiciones[i] = {
                    x: (Math.random() - 0.5) * 100,
                    y: (Math.random() - 0.5) * 60,
                    z: (Math.random() - 0.5) * 40
                };
            }
        });

        return posiciones;
    }

    _animarPulso(grupo, vitalidad) {
        // Registrar para animación continua
        const datos = {
            grupo,
            vitalidad,
            fase:    Math.random() * Math.PI * 2,
            velocidad: 0.5 + vitalidad * 0.8,
        };
        if (!this._nodosPulsando) this._nodosPulsando = [];
        this._nodosPulsando.push(datos);
    }

    _mostrarEstadisticas(stats) {
        if (!stats) return;

        // Crear panel de estadísticas en 3D
        const canvas  = document.createElement('canvas');
        canvas.width  = 512;
        canvas.height = 200;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = 'rgba(2, 5, 16, 0.8)';
        ctx.fillRect(0, 0, 512, 200);

        ctx.font      = 'bold 16px Inter, Arial';
        ctx.fillStyle = '#4A9EFF';
        ctx.fillText('VITALIDAD DE BELL', 20, 30);

        const niveles = [
            { nivel: 'plena',     color: '#00FF88', label: 'Plena' },
            { nivel: 'rica',      color: '#44FFAA', label: 'Rica' },
            { nivel: 'funcional', color: '#88FFCC', label: 'Funcional' },
            { nivel: 'emergente', color: '#AAFFDD', label: 'Emergente' },
            { nivel: 'latente',   color: '#FFD700', label: 'Latente' },
            { nivel: 'dormida',   color: '#556677', label: 'Dormida' },
        ];

        niveles.forEach(({ nivel, color, label }, i) => {
            const x = 20 + (i % 3) * 165;
            const y = 60 + Math.floor(i / 3) * 50;
            const count = stats[nivel] || 0;

            ctx.fillStyle = color;
            ctx.fillRect(x, y, 14, 14);
            ctx.fillStyle = '#AAAACC';
            ctx.font = '13px Inter, Arial';
            ctx.fillText(`${label}: ${count}`, x + 20, y + 11);
        });

        ctx.fillStyle = '#7788AA';
        ctx.font = '12px Inter, Arial';
        ctx.fillText(
            `Vitalidad promedio: ${(stats.vitalidad_promedio || 0).toFixed(3)}`,
            20, 170
        );

        const tex    = new THREE.CanvasTexture(canvas);
        const mat    = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.85 });
        const sprite = new THREE.Sprite(mat);
        sprite.scale.set(30, 12, 1);
        sprite.position.set(0, -55, 0);
        this.motor.agregar(sprite, 'vida_estadisticas');
        this.nodos.push('vida_estadisticas_sprite');
    }

    _crearLeyenda() {
        // Mini leyenda flotante
        const canvas  = document.createElement('canvas');
        canvas.width  = 200;
        canvas.height = 30;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = 'rgba(0,0,0,0)';
        ctx.clearRect(0, 0, 200, 30);
        ctx.font      = '11px Inter, Arial';
        ctx.fillStyle = '#4A9EFF';
        ctx.fillText('● Anillo azul = grounding completo', 5, 20);

        const tex    = new THREE.CanvasTexture(canvas);
        const mat    = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 0.75 });
        const sprite = new THREE.Sprite(mat);
        sprite.scale.set(20, 3, 1);
        sprite.position.set(0, -65, 0);
        this.motor.agregar(sprite, 'vida_leyenda');
    }

    _escucharActualizaciones() {
        const fn = (e) => {
            if (!this.activa) return;
            // Actualizar vitalidad de un nodo en tiempo real
            const { nodo_id, vitalidad, nivel_vida } = e.detail || {};
            if (nodo_id && vitalidad !== undefined) {
                this._actualizarVitalidadNodo(nodo_id, vitalidad, nivel_vida);
            }
        };
        document.addEventListener('bell:vitalidad_actualizada', fn);
        this._listeners.push({ tipo: 'bell:vitalidad_actualizada', fn });
    }

    _actualizarVitalidadNodo(nodo_id, vitalidad, nivel_vida) {
        const malla = this._nodosMalla.get(nodo_id);
        if (!malla) return;

        const colorHex = this._hexToInt(
            this._colorParaNivel(nivel_vida || 'dormida')
        );

        malla.material.color.setHex(colorHex);
        malla.material.emissive.setHex(colorHex);
        malla.material.emissiveIntensity = vitalidad * 0.8;
        malla.material.opacity = 0.3 + vitalidad * 0.3;
    }

    _colorParaNivel(nivel) {
        const colores = {
            'plena':     '#00FF88',
            'rica':      '#44FFAA',
            'funcional': '#88FFCC',
            'emergente': '#AAFFDD',
            'latente':   '#FFD700',
            'dormida':   '#334455',
        };
        return colores[nivel] || '#334455';
    }

    _hexToInt(hex) {
        return parseInt(hex.replace('#', ''), 16);
    }

    _construirVacia() {
        // Mostrar mensaje si no hay datos
        console.warn('Vista vida: sin datos disponibles');
    }
}

window.VistaVida = VistaVida;