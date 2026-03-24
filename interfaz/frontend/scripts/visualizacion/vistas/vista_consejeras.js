// ================================================
// VISTA_CONSEJERAS.JS — Las 8 consejeras
// Deshabilitada hasta que las consejeras existan
// La estructura ya está lista para cuando lleguen
// ================================================

class VistaConsejeras extends BaseVista {
    constructor(motor3d) {
        super(motor3d, 'consejeras');

        // Colores de cada consejera
        this.coloresConsejeras = {
            vega:  0x8B0000,
            echo:  0x00695C,
            nova:  0x1565C0,
            lyra:  0xF57F17,
            luna:  0x37474F,
            iris:  0x00838F,
            soma:  0x2E7D32,
            sage:  0x7B00FF
        };
    }

    construir() {
        // Deshabilitada — mostrar placeholder
        this.agregarNodo({
            id: 'consejeras_pendiente',
            nombre: 'Consejeras',
            tipo: 'core',
            estado: 'warning',
            posicion: { x: 0, y: 0, z: 0 }
        });

        console.log('Vista consejeras: pendiente hasta que existan');
    }

    // Cuando las consejeras existan se implementará aquí
    // sin tocar nada de lo existente
}

window.VistaConsejeras = VistaConsejeras;