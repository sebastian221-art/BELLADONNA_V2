// impulsos.js — versión optimizada
// Límite de impulsos activos para no colapsar
class GestorImpulsos {
    constructor(motor3d) {
        this.motor    = motor3d;
        this.impulsos = [];
        this._contadorId = 0;
        this.MAX_IMPULSOS = 20; // Límite duro
    }

    crearImpulso(conexionId, color = 0xFFFFFF, tamanio = 0.2) {
        // Si hay demasiados impulsos activos no crear más
        if (this.impulsos.length >= this.MAX_IMPULSOS) return null;

        const curva = window.gestorConexiones?.obtenerCurva(conexionId);
        if (!curva) return null;

        const geo = new THREE.SphereGeometry(tamanio, 6, 6);
        const mat = new THREE.MeshBasicMaterial({
            color: color, transparent: true, opacity: 0.9
        });
        const particula = new THREE.Mesh(geo, mat);

        const uid = `imp_${this._contadorId++}`;
        this.motor.agregar(particula, uid);

        this.impulsos.push({
            particula, mat, curva,
            progreso:  0,
            velocidad: 0.008 + Math.random() * 0.004,
            activo:    true,
            uid
        });

        return true;
    }

    animar(t) {
        this.impulsos = this.impulsos.filter(imp => {
            if (!imp.activo) return false;

            imp.progreso += imp.velocidad;

            if (imp.progreso >= 1) {
                this.motor.quitar(imp.uid);
                return false;
            }

            const punto = imp.curva.getPoint(
                Math.min(imp.progreso, 0.999)
            );
            imp.particula.position.copy(punto);

            // Desvanecer al final
            if (imp.progreso > 0.7) {
                imp.mat.opacity = (1 - imp.progreso) * 3;
            }

            return true;
        });
    }

    lanzarOlaActivacion(nodoId, color = 0x4A9EFF) {
        if (!window.gestorConexiones) return;

        // Máximo 4 conexiones por ola para no sobrecargar
        let contador = 0;
        window.gestorConexiones.conexiones.forEach((conn, connId) => {
            if (contador >= 4) return;
            if (conn.origenId === nodoId || conn.destinoId === nodoId) {
                setTimeout(() => {
                    this.crearImpulso(connId, color, 0.2);
                    window.gestorConexiones.activarConexion(connId);
                    setTimeout(() => {
                        window.gestorConexiones.desactivarConexion(connId);
                    }, 600);
                }, contador * 50);
                contador++;
            }
        });
    }

    lanzarRuta(ruta, color = 0xFFFFFF, delayMs = 100) {
        // Máximo 5 pasos en una ruta
        const rutaLimitada = ruta.slice(0, 5);
        rutaLimitada.forEach((connId, i) => {
            setTimeout(() => {
                this.crearImpulso(connId, color);
            }, i * delayMs);
        });
    }
}

window.GestorImpulsos = GestorImpulsos;
