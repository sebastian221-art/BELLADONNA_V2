// ================================================
// NODOS.JS — versión 3
// Ahora los nodos brillan según su vitalidad
// Si tiene grounding completo = anillo azul
// Si tiene vida genuina = halo verde
// ================================================

const COLORES_TIPO = {
    core:          { base: 0xE8F0FE, emissive: 0x8AB4F8, glow: 0x4A9EFF },
    identidad:     { base: 0xCDD8F5, emissive: 0x6A9EE8, glow: 0x3A7BD5 },
    valor:         { base: 0xB8D4FF, emissive: 0x5A8EE0, glow: 0x2E6BC8 },
    consejera:     { base: 0xCE93D8, emissive: 0x9C27B0, glow: 0x7B00FF },
    relacion:      { base: 0x80DEEA, emissive: 0x00838F, glow: 0x006B7A },
    habilidad:     { base: 0x80CBC4, emissive: 0x00695C, glow: 0x004D40 },
    concepto:      { base: 0x90CAF9, emissive: 0x1565C0, glow: 0x0D47A1 },
    memoria:       { base: 0xFFCC80, emissive: 0xE65100, glow: 0xBF360C },
    archivo:       { base: 0x546E7A, emissive: 0x263238, glow: 0x37474F },
    carpeta:       { base: 0x1E5799, emissive: 0x0D3B6E, glow: 0x0A2D52 },
    capa:          { base: 0x80CBC4, emissive: 0x00695C, glow: 0x004D40 },
    capacidad:     { base: 0xA5D6A7, emissive: 0x2E7D32, glow: 0x1B5E20 },
    capa_flujo:    { base: 0x80CBC4, emissive: 0x00695C, glow: 0x004D40 },
    interfaz:      { base: 0xFFD54F, emissive: 0xF57F17, glow: 0xE65100 },
    cerebro:       { base: 0xEF9A9A, emissive: 0xC62828, glow: 0xB71C1C },
    fundacional:   { base: 0xCE93D8, emissive: 0x6A1B9A, glow: 0x4A148C },
    documentacion: { base: 0xB0BEC5, emissive: 0x546E7A, glow: 0x37474F },
    desconocido:   { base: 0x424242, emissive: 0x212121, glow: 0x111111 },
};

const TAMANIOS_TIPO = {
    core:          4.0,  identidad:     2.5,
    valor:         2.0,  consejera:     2.2,
    relacion:      1.5,  habilidad:     1.8,
    concepto:      1.0,  memoria:       1.2,
    archivo:       0.7,  carpeta:       1.8,
    capa:          2.5,  capacidad:     1.6,
    capa_flujo:    2.0,  interfaz:      1.4,
    cerebro:       1.2,  fundacional:   1.6,
    documentacion: 0.8,  desconocido:   0.6,
};

// Colores de vida para el halo especial
const COLORES_VIDA = {
    plena:     0x00FF88,
    rica:      0x44FFAA,
    funcional: 0x88FFCC,
    emergente: 0xAAFFDD,
    latente:   0xFFD700,
    dormida:   null,  // Sin halo si dormida
};

class GestorNodos {
    constructor(motor3d) {
        this.motor = motor3d;
        this.nodos = new Map();
        this._configurarInteraccion();
    }

    crearNodo(datos) {
        const {
            id, nombre,
            tipo     = 'concepto',
            estado   = 'inactivo',
            posicion = { x: 0, y: 0, z: 0 },
            vitalidad  = 0,
            nivel_vida = 'dormida',
        } = datos;

        const tipoV   = this._tipoVisual(nombre, tipo);
        const colores = COLORES_TIPO[tipoV] || COLORES_TIPO.concepto;
        const radio   = TAMANIOS_TIPO[tipoV] || 1.0;

        const grupo = new THREE.Group();
        grupo.position.set(posicion.x, posicion.y, posicion.z);

        // ---- NÚCLEO ----
        const geoNucleo = new THREE.SphereGeometry(radio * 0.45, 10, 10);
        const matNucleo = new THREE.MeshBasicMaterial({
            color: colores.emissive, transparent: true, opacity: 0.95
        });
        const nucleo = new THREE.Mesh(geoNucleo, matNucleo);
        grupo.add(nucleo);

        // ---- CAPA EXTERIOR ----
        const geoCapa = new THREE.SphereGeometry(radio, 12, 12);
        const matCapa = new THREE.MeshPhongMaterial({
            color:             colores.base,
            emissive:          colores.emissive,
            emissiveIntensity: 0.25,
            transparent:       true,
            opacity:           0.28,
            shininess:         15,
            side:              THREE.DoubleSide
        });
        const capaExterior = new THREE.Mesh(geoCapa, matCapa);
        grupo.add(capaExterior);

        // ---- GLOW BASE ----
        const geoGlow = new THREE.SphereGeometry(radio * 1.7, 10, 10);
        const matGlow = new THREE.MeshBasicMaterial({
            color:       colores.glow,
            transparent: true,
            opacity:     0.04,
            side:        THREE.BackSide
        });
        const glow = new THREE.Mesh(geoGlow, matGlow);
        grupo.add(glow);

        // ---- HALO DE VIDA — visible si nivel > dormida ----
        let haloVida = null;
        const colorVida = COLORES_VIDA[nivel_vida];
        if (colorVida && vitalidad > 0.1) {
            const geoHalo = new THREE.SphereGeometry(radio * 2.2, 10, 10);
            const matHalo = new THREE.MeshBasicMaterial({
                color:       colorVida,
                transparent: true,
                opacity:     vitalidad * 0.15,
                side:        THREE.BackSide
            });
            haloVida = new THREE.Mesh(geoHalo, matHalo);
            grupo.add(haloVida);
        }

        // ---- ANILLO DE GROUNDING — azul si tiene grounding aplicado ----
        let anilloGrounding = null;
        if (vitalidad > 0.2) {
            const geoRing = new THREE.RingGeometry(
                radio * 1.15, radio * 1.25, 16
            );
            const matRing = new THREE.MeshBasicMaterial({
                color:       0x4A9EFF,
                transparent: true,
                opacity:     0.2 + vitalidad * 0.3,
                side:        THREE.DoubleSide
            });
            anilloGrounding = new THREE.Mesh(geoRing, matRing);
            anilloGrounding.rotation.x = Math.PI / 3;
            grupo.add(anilloGrounding);
        }

        // ---- ETIQUETA — solo nodos importantes ----
        const tiposConEtiqueta = [
            'core', 'identidad', 'valor', 'consejera',
            'capacidad', 'capa_flujo', 'habilidad', 'relacion'
        ];
        if (tiposConEtiqueta.includes(tipoV)) {
            const sprite = this._crearEtiqueta(nombre, tipoV, radio);
            if (sprite) grupo.add(sprite);
        }

        grupo.userData        = { id, nombre, tipo: tipoV, estado, vitalidad, nivel_vida };
        capaExterior.userData = { id, nombre, tipo: tipoV, estado, vitalidad, nivel_vida };

        this.motor.agregar(grupo, `nodo_${id}`);

        this.nodos.set(id, {
            grupo, nucleo, capaExterior, glow,
            haloVida, anilloGrounding,
            colorBase:       colores,
            tipoV, radio,
            vitalidad,
            nivel_vida,
            pulsando:        false,
            velocidadPulso:  Math.random() * 0.015 + 0.008,
            fase:            Math.random() * Math.PI * 2,
            tiempoActivacion: 0
        });

        return grupo;
    }

    _tipoVisual(nombre, tipo) {
        if (tipo === 'core' || nombre === 'Bell' || nombre === 'Belladonna') return 'core';
        if (nombre?.endsWith('.py'))  return 'archivo';
        if (nombre?.endsWith('.js'))  return 'archivo';
        if (nombre?.endsWith('.css')) return 'archivo';
        if (nombre?.endsWith('.md'))  return 'archivo';
        const conocidos = [
            'core', 'identidad', 'valor', 'consejera', 'relacion',
            'concepto', 'habilidad', 'memoria', 'carpeta', 'capa',
            'capacidad', 'capa_flujo', 'interfaz', 'cerebro',
            'fundacional', 'documentacion', 'desconocido', 'archivo'
        ];
        return conocidos.includes(tipo) ? tipo : 'concepto';
    }

    _crearEtiqueta(nombre, tipo, radio) {
        const canvas  = document.createElement('canvas');
        canvas.width  = 256;
        canvas.height = 56;
        const ctx     = canvas.getContext('2d');
        const esCore  = tipo === 'core';
        const nombreCorto = this._acortar(nombre);

        ctx.clearRect(0, 0, 256, 56);
        ctx.font         = esCore ? 'bold 18px Inter,Arial' : '12px Inter,Arial';
        ctx.textAlign    = 'center';
        ctx.textBaseline = 'middle';
        ctx.shadowColor  = 'rgba(0,0,0,0.9)';
        ctx.shadowBlur   = 8;

        const colTexto = {
            core: '#E8F0FE', identidad: '#C5D8FF', valor: '#B8D4FF',
            consejera: '#E1BEE7', relacion: '#B2EBF2', habilidad: '#B2DFDB',
            concepto: '#BBDEFB', capacidad: '#C8E6C9', capa_flujo: '#B2DFDB',
            interfaz: '#FFF9C4', cerebro: '#FFCDD2', fundacional: '#E1BEE7',
        };
        ctx.fillStyle = colTexto[tipo] || '#90CAF9';
        ctx.fillText(nombreCorto, 128, 28);

        const tex = new THREE.CanvasTexture(canvas);
        const mat = new THREE.SpriteMaterial({
            map: tex, transparent: true, opacity: 0.85, depthWrite: false
        });
        const sprite = new THREE.Sprite(mat);
        const escala = esCore ? 9 : 6;
        sprite.scale.set(escala, escala * 0.22, 1);
        sprite.position.set(0, radio + 1.3, 0);
        return sprite;
    }

    _acortar(nombre) {
        if (!nombre) return '';
        let n = nombre
            .replace(/\.(py|js|css|html|md|json|txt)$/, '')
            .replace(/^AUTO_/, '');
        if (n.length > 14) n = n.substring(0, 12) + '..';
        return n.charAt(0).toUpperCase() + n.slice(1).toLowerCase();
    }

    actualizarEstado(id, nuevoEstado) {
        const nodo = this.nodos.get(id);
        if (!nodo) return;

        const c = nodo.colorBase;
        const configs = {
            inactivo:   { nucleo: c.emissive, extOpacity: 0.18, glowOp: 0.03, emissiveI: 0.12, pulsar: false },
            activo:     { nucleo: 0x4A9EFF,   extOpacity: 0.52, glowOp: 0.20, emissiveI: 0.70, pulsar: true  },
            procesando: { nucleo: 0xFFFFFF,   extOpacity: 0.72, glowOp: 0.42, emissiveI: 1.00, pulsar: true  },
            error:      { nucleo: 0xFF3B30,   extOpacity: 0.55, glowOp: 0.25, emissiveI: 0.80, pulsar: true  },
            warning:    { nucleo: 0xFFCC00,   extOpacity: 0.45, glowOp: 0.15, emissiveI: 0.50, pulsar: false }
        };

        const cfg = configs[nuevoEstado] || configs.inactivo;
        nodo.nucleo.material.color.setHex(cfg.nucleo);
        nodo.capaExterior.material.opacity           = cfg.extOpacity;
        nodo.capaExterior.material.emissiveIntensity = cfg.emissiveI;
        nodo.glow.material.opacity                   = cfg.glowOp;
        nodo.glow.material.color.setHex(cfg.nucleo);
        nodo.pulsando = cfg.pulsar;

        if (nuevoEstado === 'procesando' || nuevoEstado === 'activo') {
            nodo.tiempoActivacion = Date.now();
        }
        nodo.grupo.userData.estado = nuevoEstado;
    }

    actualizarVitalidad(id, nuevaVitalidad, nuevoNivel) {
        const nodo = this.nodos.get(id);
        if (!nodo) return;

        nodo.vitalidad  = nuevaVitalidad;
        nodo.nivel_vida = nuevoNivel;

        // Actualizar halo de vida
        if (nodo.haloVida) {
            const colorVida = COLORES_VIDA[nuevoNivel];
            if (colorVida) {
                nodo.haloVida.material.color.setHex(colorVida);
                nodo.haloVida.material.opacity = nuevaVitalidad * 0.15;
            }
        }

        // Actualizar anillo de grounding
        if (nodo.anilloGrounding) {
            nodo.anilloGrounding.material.opacity = 0.2 + nuevaVitalidad * 0.3;
        }

        // Emitir evento para vista de vida
        document.dispatchEvent(new CustomEvent('bell:vitalidad_actualizada', {
            detail: { nodo_id: id, vitalidad: nuevaVitalidad, nivel_vida: nuevoNivel }
        }));
    }

    animar(t) {
        this.nodos.forEach((nodo) => {
            nodo.grupo.position.y += Math.sin(t * 0.35 + nodo.fase) * 0.007;
            nodo.nucleo.rotation.y += 0.006;
            nodo.nucleo.rotation.x += 0.002;

            if (nodo.pulsando) {
                const s = 1 + Math.sin(t * nodo.velocidadPulso * 80) * 0.07;
                nodo.grupo.scale.setScalar(s);
                nodo.glow.material.opacity = 0.15 + Math.sin(t * nodo.velocidadPulso * 80) * 0.12;
                // Pulsar también el halo de vida
                if (nodo.haloVida) {
                    nodo.haloVida.material.opacity = (0.08 + Math.sin(t * nodo.velocidadPulso * 80) * 0.06) * nodo.vitalidad;
                }
            }

            if (nodo.tipoV === 'core') {
                nodo.nucleo.rotation.y += 0.008;
                nodo.glow.material.opacity = 0.08 + Math.sin(t * 0.8) * 0.06;
                nodo.capaExterior.rotation.y -= 0.002;
                if (nodo.haloVida) {
                    nodo.haloVida.material.opacity = 0.10 + Math.sin(t * 0.6) * 0.08;
                }
            }

            // Rotar anillo de grounding suavemente
            if (nodo.anilloGrounding) {
                nodo.anilloGrounding.rotation.y += 0.003;
                nodo.anilloGrounding.rotation.z += 0.001;
            }

            if (nodo.tiempoActivacion > 0) {
                const elapsed = (Date.now() - nodo.tiempoActivacion) / 1000;
                if (elapsed > 3 && nodo.pulsando) {
                    nodo.pulsando         = false;
                    nodo.tiempoActivacion = 0;
                    this.actualizarEstado(nodo.grupo.userData.id, 'activo');
                }
            }
        });
    }

    eliminarNodo(id) {
        const nodo = this.nodos.get(id);
        if (nodo) { this.motor.quitar(`nodo_${id}`); this.nodos.delete(id); }
    }

    obtenerNodo(id)         { return this.nodos.get(id); }
    obtenerMalla(id)        { const n = this.nodos.get(id); return n?.capaExterior || null; }
    obtenerGrupo(id)        { const n = this.nodos.get(id); return n?.grupo || null; }
    obtenerTodasLasMallas() {
        const m = [];
        this.nodos.forEach(n => m.push(n.capaExterior));
        return m;
    }

    _configurarInteraccion() {
        const raycaster = new THREE.Raycaster();
        const mouse     = new THREE.Vector2();

        document.addEventListener('click', (e) => {
            const canvas = document.getElementById('bell-canvas');
            if (!canvas) return;
            const rect = canvas.getBoundingClientRect();
            if (e.clientX < rect.left || e.clientX > rect.right ||
                e.clientY < rect.top  || e.clientY > rect.bottom) return;

            mouse.x = ((e.clientX - rect.left) / rect.width)  *  2 - 1;
            mouse.y = ((e.clientY - rect.top)  / rect.height) * -2 + 1;

            if (!window.BellApp?.motor3d) return;
            raycaster.setFromCamera(mouse, window.BellApp.motor3d.obtenerCamara());
            const hits = raycaster.intersectObjects(this.obtenerTodasLasMallas(), false);
            if (hits.length > 0) this._mostrarInfo(hits[0].object.userData);
        });
    }

    _mostrarInfo(datos) {
        const panel = document.getElementById('nodo-info');
        if (!panel) return;
        document.getElementById('nodo-info-nombre').textContent = datos.nombre || datos.id;
        document.getElementById('nodo-info-tipo').textContent   = datos.tipo || 'nodo';
        document.getElementById('nodo-info-estado').textContent =
            `Estado: ${datos.estado || '?'} | Vida: ${datos.nivel_vida || '?'} (${((datos.vitalidad || 0) * 100).toFixed(0)}%)`;
        panel.classList.remove('oculto');
        document.getElementById('nodo-info-cerrar').onclick = () => panel.classList.add('oculto');
    }
}

window.GestorNodos  = GestorNodos;
window.COLORES_TIPO = COLORES_TIPO;