// ================================================
// INDICADOR.JS — Estado de Bell en tiempo real
// Muestra qué está haciendo Bell mientras procesa
// ================================================

class Indicador {
    constructor() {
        this.elemento = document.getElementById('chat-indicador');
        this.textoActual = null;
        this.timeoutOcultar = null;
    }

    mostrar(texto) {
        if (this.timeoutOcultar) {
            clearTimeout(this.timeoutOcultar);
            this.timeoutOcultar = null;
        }

        // Si no hay contenido aún crear los elementos
        if (!this.elemento.querySelector('.indicador-punto')) {
            this.elemento.innerHTML = `
                <div class="indicador-punto"></div>
                <div class="indicador-texto"></div>
            `;
        }

        const textoEl = this.elemento.querySelector('.indicador-texto');
        textoEl.textContent = texto;
        textoEl.classList.add('visible');
        this.textoActual = texto;
    }

    ocultar(delay = 800) {
        this.timeoutOcultar = setTimeout(() => {
            const textoEl = this.elemento.querySelector('.indicador-texto');
            if (textoEl) {
                textoEl.classList.remove('visible');
            }
            this.textoActual = null;
        }, delay);
    }

    actualizar(texto) {
        this.mostrar(texto);
    }
}

window.Indicador = Indicador;