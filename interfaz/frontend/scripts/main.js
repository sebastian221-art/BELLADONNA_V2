// interfaz/frontend/scripts/main.js
// ================================================
// CORREGIDO: agrega vista Vida + muestra "Conectada"
// ================================================

const BellApp = {
    socket:      null,
    vistaActiva: 'logica',
    motor3d:     null,
    chat:        null,
    iniciado:    false
};

document.addEventListener('DOMContentLoaded', () => {
    iniciarBell();
});

async function iniciarBell() {
    console.log('Bell iniciando...');
    try {
        BellApp.socket = io();
        configurarSocketGlobal(BellApp.socket);

        BellApp.motor3d = new Motor3D('bell-canvas');
        BellApp.motor3d.iniciar();

        window.gestorNodos      = new GestorNodos(BellApp.motor3d);
        window.gestorConexiones = new GestorConexiones(BellApp.motor3d);
        window.gestorImpulsos   = new GestorImpulsos(BellApp.motor3d);

        window.controlCamara = new ControlCamara(
            BellApp.motor3d,
            document.getElementById('bell-canvas')
        );

        // Vistas — VistaVida incluida
        window.vistas = {
            logica:     new VistaLogica(BellApp.motor3d),
            neuronal:   new VistaNeuronal(BellApp.motor3d),
            flujo:      new VistaFlujo(BellApp.motor3d),
            consejeras: new VistaConsejeras(BellApp.motor3d),
            vida:       new VistaVida(BellApp.motor3d),
        };

        activarVista('logica');

        window.estadoBell    = new EstadoBell(BellApp.socket);
        window.sincronizador = new Sincronizador(
            BellApp.socket,
            window.estadoBell,
            window.gestorNodos,
            window.gestorConexiones,
            window.gestorImpulsos
        );
        window.indicador = new Indicador();
        BellApp.chat     = new Chat(BellApp.socket, window.indicador);

        configurarSelectorVistas();

        BellApp.socket.emit('solicitar_estado');
        BellApp.iniciado = true;
        actualizarEstadoGlobal('activo', 'Conectada');
        console.log('Bell iniciada');

    } catch (error) {
        console.error('Error iniciando Bell:', error);
        actualizarEstadoGlobal('error', 'Error al iniciar');
    }
}

function configurarSocketGlobal(socket) {
    socket.on('connect',       () => actualizarEstadoGlobal('activo', 'Conectada'));
    socket.on('disconnect',    () => actualizarEstadoGlobal('error',  'Desconectada'));
    socket.on('connect_error', () => actualizarEstadoGlobal('error',  'Sin conexión'));
}

function configurarSelectorVistas() {
    const botones = document.querySelectorAll('.btn-vista');
    botones.forEach(boton => {
        boton.addEventListener('click', () => {
            if (boton.classList.contains('deshabilitada')) return;
            const vista = boton.dataset.vista;
            activarVista(vista);
            botones.forEach(b => b.classList.remove('activa'));
            boton.classList.add('activa');
        });
    });
}

function activarVista(nombreVista) {
    if (BellApp.vistaActiva && window.vistas[BellApp.vistaActiva]) {
        window.vistas[BellApp.vistaActiva].desactivar();
    }
    if (window.vistas[nombreVista]) {
        window.vistas[nombreVista].activar();
        BellApp.vistaActiva = nombreVista;
    }
}

function actualizarEstadoGlobal(estado, texto) {
    const el = document.getElementById('bell-estado-global');
    if (!el) return;
    el.textContent = `● ${texto}`;
    el.className   = estado;
}

window.BellApp               = BellApp;
window.activarVista          = activarVista;
window.actualizarEstadoGlobal = actualizarEstadoGlobal;