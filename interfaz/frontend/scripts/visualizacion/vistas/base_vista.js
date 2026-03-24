// ================================================
// BASE_VISTA.JS — Clase base para todas las vistas
// Todas las vistas heredan de aquí
// Garantiza que todas funcionen igual
// ================================================

class BaseVista {
    constructor(motor3d, nombre) {
        this.motor = motor3d;
        this.nombre = nombre;
        this.activa = false;
        this.nodos = [];
        this.conexiones = [];
    }

    // Activar esta vista
    activar() {
        this.activa = true;
        this.limpiar();
        this.construir();
        console.log(`Vista activada: ${this.nombre}`);
    }

    // Desactivar esta vista
    desactivar() {
        this.activa = false;
        this.limpiar();
        console.log(`Vista desactivada: ${this.nombre}`);
    }

    // Limpiar todos los objetos de esta vista
    limpiar() {
        this.nodos.forEach(id => {
            if (window.gestorNodos) {
                window.gestorNodos.eliminarNodo(id);
            }
        });
        this.conexiones.forEach(id => {
            if (window.gestorConexiones) {
                window.gestorConexiones.eliminarConexion(id);
            }
        });
        this.nodos = [];
        this.conexiones = [];
    }

    // Construir la vista — cada vista lo implementa
    construir() {
        // Implementar en cada vista
        console.warn(`${this.nombre}: construir() no implementado`);
    }

    // Actualizar un nodo en esta vista
    actualizarNodo(id, estado) {
        if (!this.activa) return;
        if (window.gestorNodos) {
            window.gestorNodos.actualizarEstado(id, estado);
        }
    }

    // Agregar un nodo a esta vista
    agregarNodo(datos) {
        if (window.gestorNodos) {
            window.gestorNodos.crearNodo(datos);
            this.nodos.push(datos.id);
        }
    }

    // Agregar una conexión a esta vista
    agregarConexion(id, origenId, destinoId, peso) {
        if (window.gestorConexiones) {
            window.gestorConexiones.crearConexion(
                id, origenId, destinoId, peso
            );
            this.conexiones.push(id);
        }
    }

    // Distribuir nodos en círculo
    posicionesEnCirculo(cantidad, radio = 20) {
        const posiciones = [];
        for (let i = 0; i < cantidad; i++) {
            const angulo = (i / cantidad) * Math.PI * 2;
            posiciones.push({
                x: Math.cos(angulo) * radio,
                y: Math.sin(angulo) * radio,
                z: (Math.random() - 0.5) * 10
            });
        }
        return posiciones;
    }

    // Distribuir nodos en esfera
    posicionesEnEsfera(cantidad, radio = 25) {
        const posiciones = [];
        const phi = Math.PI * (3 - Math.sqrt(5));

        for (let i = 0; i < cantidad; i++) {
            const y = 1 - (i / (cantidad - 1)) * 2;
            const r = Math.sqrt(1 - y * y);
            const theta = phi * i;

            posiciones.push({
                x: Math.cos(theta) * r * radio,
                y: y * radio,
                z: Math.sin(theta) * r * radio
            });
        }
        return posiciones;
    }
}

window.BaseVista = BaseVista;