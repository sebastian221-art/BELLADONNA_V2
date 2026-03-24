// ================================================
// MOTOR3D.JS — Núcleo Three.js mejorado
// Atmósfera cerebral profunda y orgánica
// ================================================

class Motor3D {
    constructor(idCanvas) {
        this.canvas = document.getElementById(idCanvas);
        this.escena = null;
        this.camara = null;
        this.renderer = null;
        this.animando = false;
        this.objetos = new Map();
        this.reloj = new THREE.Clock();
    }

    iniciar() {
        this._crearEscena();
        this._crearCamara();
        this._crearRenderer();
        this._crearLuces();
        this._crearAtmosfera();
        this._iniciarLoop();
        this._configurarResize();
        console.log('Motor 3D iniciado');
    }

    _crearEscena() {
        this.escena = new THREE.Scene();
        this.escena.fog = new THREE.FogExp2(0x020510, 0.006);
        this.escena.background = new THREE.Color(0x020510);
    }

    _crearCamara() {
        const ancho = this.canvas.clientWidth || window.innerWidth;
        const alto  = this.canvas.clientHeight || window.innerHeight;
        this.camara = new THREE.PerspectiveCamera(55, ancho / alto, 0.1, 2000);
        this.camara.position.set(0, 0, 90);
        this.camara.lookAt(0, 0, 0);
    }

    _crearRenderer() {
        this.renderer = new THREE.WebGLRenderer({
            canvas:    this.canvas,
            antialias: true,
            alpha:     false
        });
        const ancho = this.canvas.clientWidth || window.innerWidth;
        const alto  = this.canvas.clientHeight || window.innerHeight;
        this.renderer.setSize(ancho, alto);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.setClearColor(0x020510, 1);
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.8;
    }

    _crearLuces() {
        // Luz ambiental muy suave — casi oscuro
        const ambiental = new THREE.AmbientLight(0x050820, 1.5);
        this.escena.add(ambiental);

        // Luz central azul — simula el núcleo del cerebro
        const central = new THREE.PointLight(0x3A7BD5, 4.0, 200);
        central.position.set(0, 0, 20);
        this.escena.add(central);
        this._luzCentral = central;

        // Luces secundarias de colores biológicos
        const luz1 = new THREE.PointLight(0x0D3B6E, 2.0, 150);
        luz1.position.set(40, 30, -10);
        this.escena.add(luz1);

        const luz2 = new THREE.PointLight(0x1A0A3E, 1.5, 120);
        luz2.position.set(-40, -30, -10);
        this.escena.add(luz2);

        const luz3 = new THREE.PointLight(0x0A2040, 1.0, 100);
        luz3.position.set(0, -50, 30);
        this.escena.add(luz3);
    }

    _crearAtmosfera() {
        // Partículas de fondo — polvo neuronal
        const geo = new THREE.BufferGeometry();
        const count = 2000;
        const pos = new Float32Array(count * 3);
        const colores = new Float32Array(count * 3);

        for (let i = 0; i < count; i++) {
            const r = 150 + Math.random() * 200;
            const theta = Math.random() * Math.PI * 2;
            const phi   = Math.acos(2 * Math.random() - 1);
            pos[i*3]   = r * Math.sin(phi) * Math.cos(theta);
            pos[i*3+1] = r * Math.sin(phi) * Math.sin(theta);
            pos[i*3+2] = r * Math.cos(phi);

            // Colores azulados variados
            colores[i*3]   = 0.05 + Math.random() * 0.15;
            colores[i*3+1] = 0.10 + Math.random() * 0.20;
            colores[i*3+2] = 0.30 + Math.random() * 0.40;
        }

        geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
        geo.setAttribute('color',    new THREE.BufferAttribute(colores, 3));

        const mat = new THREE.PointsMaterial({
            size:         0.5,
            vertexColors: true,
            transparent:  true,
            opacity:      0.6,
            sizeAttenuation: true
        });

        const particulas = new THREE.Points(geo, mat);
        this.escena.add(particulas);
        this._particulas = particulas;

        // Partículas más cercanas — "neurotransmisores"
        const geo2 = new THREE.BufferGeometry();
        const count2 = 300;
        const pos2 = new Float32Array(count2 * 3);

        for (let i = 0; i < count2; i++) {
            pos2[i*3]   = (Math.random() - 0.5) * 120;
            pos2[i*3+1] = (Math.random() - 0.5) * 120;
            pos2[i*3+2] = (Math.random() - 0.5) * 60;
        }
        geo2.setAttribute('position', new THREE.BufferAttribute(pos2, 3));

        const mat2 = new THREE.PointsMaterial({
            size:        0.3,
            color:       0x4A9EFF,
            transparent: true,
            opacity:     0.3
        });

        const neuro = new THREE.Points(geo2, mat2);
        this.escena.add(neuro);
        this._neurotransmisores = neuro;
    }

    _iniciarLoop() {
        this.animando = true;
        this._loop();
    }

    _loop() {
        if (!this.animando) return;
        requestAnimationFrame(() => this._loop());

        const t = this.reloj.getElapsedTime();

        // Pulso de la luz central — como latido
        if (this._luzCentral) {
            this._luzCentral.intensity = 3.0 + Math.sin(t * 1.2) * 1.0;
        }

        // Rotación muy lenta del fondo
        if (this._particulas) {
            this._particulas.rotation.y += 0.00006;
            this._particulas.rotation.x += 0.00003;
        }

        // Movimiento flotante de neurotransmisores
        if (this._neurotransmisores) {
            this._neurotransmisores.rotation.y -= 0.00008;
            const posAttr = this._neurotransmisores.geometry.attributes.position;
            for (let i = 0; i < posAttr.count; i++) {
                posAttr.setY(i, posAttr.getY(i) + Math.sin(t * 0.3 + i) * 0.002);
            }
            posAttr.needsUpdate = true;
        }

        if (window.gestorNodos)    window.gestorNodos.animar(t);
        if (window.gestorConexiones) window.gestorConexiones.animar(t);
        if (window.gestorImpulsos) window.gestorImpulsos.animar(t);
        if (window.controlCamara)  window.controlCamara.animar();

        this.renderer.render(this.escena, this.camara);
    }

    _configurarResize() {
        window.addEventListener('resize', () => {
            const ancho = this.canvas.clientWidth;
            const alto  = this.canvas.clientHeight;
            this.camara.aspect = ancho / alto;
            this.camara.updateProjectionMatrix();
            this.renderer.setSize(ancho, alto);
        });
    }

    agregar(objeto, id) {
        this.escena.add(objeto);
        if (id) this.objetos.set(id, objeto);
    }

    quitar(id) {
        const obj = this.objetos.get(id);
        if (obj) {
            this.escena.remove(obj);
            this.objetos.delete(id);
        }
    }

    obtener(id)         { return this.objetos.get(id); }
    obtenerCamara()     { return this.camara; }
    obtenerRenderer()   { return this.renderer; }
    obtenerEscena()     { return this.escena; }
}

window.Motor3D = Motor3D;