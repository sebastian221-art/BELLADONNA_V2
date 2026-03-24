// conexiones.js — fibras nerviosas orgánicas mejoradas
class GestorConexiones {
    constructor(motor3d) {
        this.motor      = motor3d;
        this.conexiones = new Map();
    }

    crearConexion(id, origenId, destinoId, peso = 0.5) {
        const grupoOrigen  = window.gestorNodos?.obtenerGrupo(origenId);
        const grupoDestino = window.gestorNodos?.obtenerGrupo(destinoId);
        if (!grupoOrigen || !grupoDestino) return null;

        const pO = grupoOrigen.position.clone();
        const pD = grupoDestino.position.clone();

        // Curva orgánica proporcional a la distancia
        const distancia   = pO.distanceTo(pD);
        const desvFactor  = Math.min(distancia * 0.30, 14);
        const ctrl = new THREE.Vector3(
            (pO.x + pD.x) / 2 + (Math.random() - 0.5) * desvFactor,
            (pO.y + pD.y) / 2 + (Math.random() - 0.5) * desvFactor,
            (pO.z + pD.z) / 2 + (Math.random() - 0.5) * desvFactor * 0.5
        );

        const curva  = new THREE.QuadraticBezierCurve3(pO, ctrl, pD);
        const puntos = curva.getPoints(50);

        // Opacidad proporcional al peso — más visible
        const opBase = 0.06 + peso * 0.28;

        // Color por peso — más brillante cuanto más fuerte
        const colorConn = peso >= 0.85 ? 0x3A6BC8
                        : peso >= 0.65 ? 0x2A5298
                        : peso >= 0.45 ? 0x1A3A6B
                        :                0x0F2040;

        const geo = new THREE.BufferGeometry().setFromPoints(puntos);
        const mat = new THREE.LineBasicMaterial({
            color:       colorConn,
            transparent: true,
            opacity:     opBase,
            linewidth:   1
        });

        const linea = new THREE.Line(geo, mat);
        linea.userData = { id, origenId, destinoId, peso };

        this.motor.agregar(linea, `conn_${id}`);

        this.conexiones.set(id, {
            linea, mat, curva, puntos,
            origenId, destinoId, peso,
            opBase,
            activa: false,
            fase:   Math.random() * Math.PI * 2
        });

        return linea;
    }

    activarConexion(id) {
        const conn = this.conexiones.get(id);
        if (!conn) return;
        conn.mat.color.setHex(0xB8D4FF);
        conn.mat.opacity = Math.min(conn.opBase * 3.5, 0.92);
        conn.activa = true;
    }

    desactivarConexion(id) {
        const conn = this.conexiones.get(id);
        if (!conn) return;
        conn.mat.color.setHex(0x1A3A6B);
        conn.mat.opacity = conn.opBase;
        conn.activa = false;
    }

    animar(t) {
        this.conexiones.forEach((conn) => {
            if (!conn.activa) {
                // Pulso muy suave — da vida al tejido
                const pulso = Math.sin(t * 0.5 + conn.fase) * 0.015;
                conn.mat.opacity = Math.max(0.012, conn.opBase + pulso);
            }
        });
    }

    obtenerCurva(id)     { return this.conexiones.get(id)?.curva || null; }

    eliminarConexion(id) {
        this.motor.quitar(`conn_${id}`);
        this.conexiones.delete(id);
    }
}

window.GestorConexiones = GestorConexiones;
