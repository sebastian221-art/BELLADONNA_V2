// ================================================
// CAMARA.JS — Control libre de cámara
// Zoom hacia cualquier punto
// Pan para moverse por el espacio
// Rotación orbital alrededor del objetivo
// ================================================

class ControlCamara {
    constructor(motor3d, canvas) {
        this.motor = motor3d;
        this.canvas = canvas;
        this.camara = motor3d.obtenerCamara();

        // Objetivo — punto al que mira la cámara
        // Cambia con el pan para moverse libremente
        this.objetivo = new THREE.Vector3(0, 0, 0);

        // Posición esférica relativa al objetivo
        this.esferica = {
            radio: 80,
            theta: 0,       // Rotación horizontal
            phi: Math.PI / 2  // Rotación vertical
        };

        // Estado del mouse
        this.estado = {
            rotando: false,
            panneando: false,
            ultimaPos: { x: 0, y: 0 },
            botonPresionado: -1
        };

        // Auto-rotación
        this.autoRotacion = true;
        this.velocidadAutoRotacion = 0.0003;
        this._timeoutAutoRotacion = null;

        // Vectores de pan
        this._vectorPanX = new THREE.Vector3();
        this._vectorPanY = new THREE.Vector3();

        this._configurarEventos();
    }

    _configurarEventos() {
        // ---- MOUSE DOWN ----
        this.canvas.addEventListener('mousedown', (e) => {
            e.preventDefault();
            this.estado.botonPresionado = e.button;
            this.estado.ultimaPos = { x: e.clientX, y: e.clientY };

            if (e.button === 0) {
                // Click izquierdo — rotar
                this.estado.rotando = true;
                this.estado.panneando = false;
            } else if (e.button === 2) {
                // Click derecho — pan
                this.estado.panneando = true;
                this.estado.rotando = false;
            } else if (e.button === 1) {
                // Click medio — pan también
                this.estado.panneando = true;
                this.estado.rotando = false;
            }

            this._pausarAutoRotacion();
        });

        // ---- MOUSE MOVE ----
        this.canvas.addEventListener('mousemove', (e) => {
            if (!this.estado.rotando && !this.estado.panneando) return;

            const deltaX = e.clientX - this.estado.ultimaPos.x;
            const deltaY = e.clientY - this.estado.ultimaPos.y;

            if (this.estado.rotando) {
                this._rotar(deltaX, deltaY);
            } else if (this.estado.panneando) {
                this._pan(deltaX, deltaY);
            }

            this.estado.ultimaPos = { x: e.clientX, y: e.clientY };
        });

        // ---- MOUSE UP ----
        this.canvas.addEventListener('mouseup', () => {
            this.estado.rotando = false;
            this.estado.panneando = false;
            this.estado.botonPresionado = -1;
            this._reanudarAutoRotacion();
        });

        // ---- MOUSE LEAVE ----
        this.canvas.addEventListener('mouseleave', () => {
            this.estado.rotando = false;
            this.estado.panneando = false;
        });

        // ---- WHEEL — zoom hacia el cursor ----
        this.canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            this._zoom(e.deltaY, e.clientX, e.clientY);
        }, { passive: false });

        // ---- TOUCH — soporte móvil ----
        this._configurarTouch();

        // ---- CLICK DERECHO — deshabilitar menú contextual ----
        this.canvas.addEventListener('contextmenu', (e) => {
            e.preventDefault();
        });

        // ---- DOBLE CLICK — centrar en nodo ----
        this.canvas.addEventListener('dblclick', (e) => {
            this._centrarEnNodoCercano(e);
        });
    }

    _rotar(deltaX, deltaY) {
        this.esferica.theta -= deltaX * 0.006;
        this.esferica.phi  -= deltaY * 0.006;

        // Límites verticales
        this.esferica.phi = Math.max(
            0.05,
            Math.min(Math.PI - 0.05, this.esferica.phi)
        );
    }

    _pan(deltaX, deltaY) {
        // Calcular vectores de pan según orientación de la cámara
        const distancia = this.esferica.radio;
        const factorPan = distancia * 0.001;

        // Vector derecha de la cámara
        this._vectorPanX.setFromMatrixColumn(
            this.camara.matrix, 0
        );
        this._vectorPanX.multiplyScalar(-deltaX * factorPan);

        // Vector arriba de la cámara
        this._vectorPanY.setFromMatrixColumn(
            this.camara.matrix, 1
        );
        this._vectorPanY.multiplyScalar(deltaY * factorPan);

        // Mover el objetivo
        this.objetivo.add(this._vectorPanX);
        this.objetivo.add(this._vectorPanY);
    }

    _zoom(deltaRueda, mouseX, mouseY) {
        // Zoom hacia el punto donde está el cursor
        const factorZoom = deltaRueda > 0 ? 1.12 : 0.88;

        // Si el cursor está sobre un nodo hacer zoom hacia él
        const puntoObjetivo = this._obtenerPuntoEnEspacio(
            mouseX, mouseY
        );

        if (puntoObjetivo) {
            // Mover el objetivo ligeramente hacia el punto del cursor
            const direccion = new THREE.Vector3()
                .subVectors(puntoObjetivo, this.objetivo)
                .multiplyScalar(0.1);

            if (deltaRueda < 0) {
                // Acercando — mover objetivo hacia el cursor
                this.objetivo.add(direccion);
            }
        }

        // Ajustar radio
        this.esferica.radio *= factorZoom;
        this.esferica.radio = Math.max(
            5,
            Math.min(500, this.esferica.radio)
        );
    }

    _obtenerPuntoEnEspacio(clientX, clientY) {
        // Obtener el punto 3D donde está el cursor
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        const rect = this.canvas.getBoundingClientRect();

        mouse.x = ((clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((clientY - rect.top) / rect.height) * 2 + 1;

        raycaster.setFromCamera(mouse, this.camara);

        if (window.gestorNodos) {
            const mallas = window.gestorNodos.obtenerTodasLasMallas();
            const intersecciones = raycaster.intersectObjects(
                mallas, false
            );
            if (intersecciones.length > 0) {
                return intersecciones[0].point;
            }
        }

        return null;
    }

    _centrarEnNodoCercano(evento) {
        const rect = this.canvas.getBoundingClientRect();
        const mouse = new THREE.Vector2(
            ((evento.clientX - rect.left) / rect.width) * 2 - 1,
            -((evento.clientY - rect.top) / rect.height) * 2 + 1
        );

        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, this.camara);

        if (!window.gestorNodos) return;

        const mallas = window.gestorNodos.obtenerTodasLasMallas();
        const intersecciones = raycaster.intersectObjects(mallas, false);

        if (intersecciones.length > 0) {
            const posicion = intersecciones[0].object.position;

            // Animar suavemente hacia el nodo clickeado
            this._animarHacia(posicion.clone(), 25);
        }
    }

    _animarHacia(nuevoPunto, nuevoRadio) {
        // Guardar estado inicial
        const objetivoInicial = this.objetivo.clone();
        const radioInicial = this.esferica.radio;
        const inicio = Date.now();
        const duracion = 600;

        const animar = () => {
            const progreso = Math.min(
                (Date.now() - inicio) / duracion, 1
            );

            // Easing suave
            const t = 1 - Math.pow(1 - progreso, 3);

            this.objetivo.lerpVectors(objetivoInicial, nuevoPunto, t);
            this.esferica.radio = radioInicial +
                (nuevoRadio - radioInicial) * t;

            if (progreso < 1) {
                requestAnimationFrame(animar);
            }
        };

        requestAnimationFrame(animar);
    }

    _pausarAutoRotacion() {
        this.autoRotacion = false;
        if (this._timeoutAutoRotacion) {
            clearTimeout(this._timeoutAutoRotacion);
        }
    }

    _reanudarAutoRotacion() {
        // Reanudar auto-rotación después de 4 segundos sin interacción
        this._timeoutAutoRotacion = setTimeout(() => {
            this.autoRotacion = true;
        }, 4000);
    }

    _configurarTouch() {
        let tocandoCon2Dedos = false;
        let distanciaInicial = 0;
        let ultimosTocques = [];

        this.canvas.addEventListener('touchstart', (e) => {
            e.preventDefault();
            if (e.touches.length === 1) {
                this.estado.rotando = true;
                this.estado.ultimaPos = {
                    x: e.touches[0].clientX,
                    y: e.touches[0].clientY
                };
                this._pausarAutoRotacion();
            } else if (e.touches.length === 2) {
                tocandoCon2Dedos = true;
                this.estado.rotando = false;
                distanciaInicial = this._distanciaEntreTocques(e.touches);
                ultimosTocques = [
                    { x: e.touches[0].clientX, y: e.touches[0].clientY },
                    { x: e.touches[1].clientX, y: e.touches[1].clientY }
                ];
            }
        }, { passive: false });

        this.canvas.addEventListener('touchmove', (e) => {
            e.preventDefault();
            if (e.touches.length === 1 && this.estado.rotando) {
                const deltaX = e.touches[0].clientX -
                               this.estado.ultimaPos.x;
                const deltaY = e.touches[0].clientY -
                               this.estado.ultimaPos.y;
                this._rotar(deltaX, deltaY);
                this.estado.ultimaPos = {
                    x: e.touches[0].clientX,
                    y: e.touches[0].clientY
                };
            } else if (e.touches.length === 2 && tocandoCon2Dedos) {
                // Pinch zoom
                const distanciaActual = this._distanciaEntreTocques(
                    e.touches
                );
                const delta = distanciaInicial - distanciaActual;
                this._zoom(delta * 2, 0, 0);
                distanciaInicial = distanciaActual;

                // Pan con dos dedos
                const centroActual = {
                    x: (e.touches[0].clientX + e.touches[1].clientX) / 2,
                    y: (e.touches[0].clientY + e.touches[1].clientY) / 2
                };
                const centroAnterior = {
                    x: (ultimosTocques[0].x + ultimosTocques[1].x) / 2,
                    y: (ultimosTocques[0].y + ultimosTocques[1].y) / 2
                };
                this._pan(
                    centroActual.x - centroAnterior.x,
                    centroActual.y - centroAnterior.y
                );
                ultimosTocques = [
                    { x: e.touches[0].clientX, y: e.touches[0].clientY },
                    { x: e.touches[1].clientX, y: e.touches[1].clientY }
                ];
            }
        }, { passive: false });

        this.canvas.addEventListener('touchend', () => {
            this.estado.rotando = false;
            tocandoCon2Dedos = false;
            this._reanudarAutoRotacion();
        });
    }

    _distanciaEntreTocques(touches) {
        const dx = touches[0].clientX - touches[1].clientX;
        const dy = touches[0].clientY - touches[1].clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }

    animar() {
        // Auto-rotación suave
        if (this.autoRotacion) {
            this.esferica.theta += this.velocidadAutoRotacion;
        }

        // Calcular posición de la cámara en coordenadas esféricas
        // relativas al objetivo actual
        const sinPhi = Math.sin(this.esferica.phi);
        const cosPhi = Math.cos(this.esferica.phi);
        const sinTheta = Math.sin(this.esferica.theta);
        const cosTheta = Math.cos(this.esferica.theta);

        this.camara.position.x = this.objetivo.x +
            this.esferica.radio * sinPhi * cosTheta;
        this.camara.position.y = this.objetivo.y +
            this.esferica.radio * cosPhi;
        this.camara.position.z = this.objetivo.z +
            this.esferica.radio * sinPhi * sinTheta;

        // Siempre mirar al objetivo — que ahora puede moverse
        this.camara.lookAt(this.objetivo);
    }

    // API pública
    irA(posicion, radio = 25) {
        this._animarHacia(
            new THREE.Vector3(posicion.x, posicion.y, posicion.z),
            radio
        );
    }

    resetear() {
        this._animarHacia(new THREE.Vector3(0, 0, 0), 80);
    }
}

window.ControlCamara = ControlCamara;