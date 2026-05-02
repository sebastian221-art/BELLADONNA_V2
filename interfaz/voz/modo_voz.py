# interfaz/voz/modo_voz.py v4
# ================================================
# BELL — MODO VOZ COMPLETO
#
# Escucha:  micrófono del PC (pyaudio o sounddevice)
# Habla:    Google Nest Mini
#
# Detecta automáticamente cuál librería de audio
# está disponible — pyaudio o sounddevice.
#
# Uso:
#   python interfaz/voz/modo_voz.py
#   python interfaz/voz/modo_voz.py --nest "Sala"
#   python interfaz/voz/modo_voz.py --modo pulsa
# ================================================

import sys, time, threading, random, requests
from pathlib import Path
from datetime import datetime

_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_ROOT))

from interfaz.voz.hablador_nest import HabladorNest

PALABRAS_ACTIVACION = [
    'oye bell','oye bella','hey bell','hey bella',
    'bell','bella','belladonna',
]
URL_BELL = 'http://127.0.0.1:5000/api/chat/mensaje'


# ── ESCUCHADOR — detecta pyaudio o sounddevice ────────────

def _crear_escuchador():
    """
    Intenta crear el mejor escuchador disponible.
    Primero pyaudio, luego sounddevice, luego None.
    """
    # Intentar pyaudio (mejor compatibilidad con SpeechRecognition)
    try:
        import pyaudio
        from interfaz.voz._escuchador_pyaudio import EscuchadorPyAudio
        e = EscuchadorPyAudio()
        if e.ok:
            print('  ✅ Audio: pyaudio')
            return e
    except ImportError:
        pass

    # Intentar sounddevice (para Python 3.14+)
    try:
        import sounddevice
        from interfaz.voz.escuchador_sd import EscuchadorSD
        e = EscuchadorSD()
        if e.ok:
            print('  ✅ Audio: sounddevice')
            return e
    except ImportError:
        pass

    print('  ❌ Sin librería de audio — modo solo texto')
    print('     Instala: pip install sounddevice soundfile numpy')
    return None


class EscuchadorFallback:
    """Escuchador vacío cuando no hay librería de audio."""
    ok = False
    def escuchar_corto(self): return ''
    def escuchar_mensaje(self): return ''
    def escuchar_con_vad(self, timeout=6): return ''


# ── ESCUCHADOR PYAUDIO (encapsulado) ─────────────────────

class _EscuchadorPyAudioInterno:
    """Escuchador usando speech_recognition + pyaudio."""

    def __init__(self):
        self._sr = self._rec = self._mic = None
        self.ok = False
        try:
            import speech_recognition as sr
            self._sr  = sr
            self._rec = sr.Recognizer()
            self._rec.energy_threshold         = 300
            self._rec.dynamic_energy_threshold  = True
            self._rec.pause_threshold           = 0.8
            self._mic = sr.Microphone()
            with self._mic as f:
                self._rec.adjust_for_ambient_noise(f, duration=1)
            self.ok = True
        except Exception:
            pass

    def escuchar_corto(self) -> str:
        if not self.ok: return ''
        try:
            with self._mic as f:
                audio = self._rec.listen(f, timeout=4, phrase_time_limit=5)
            return self._rec.recognize_google(audio, language='es-CO').lower()
        except Exception: return ''

    def escuchar_mensaje(self) -> str:
        if not self.ok: return ''
        try:
            with self._mic as f:
                self._rec.adjust_for_ambient_noise(f, duration=0.2)
                audio = self._rec.listen(f, timeout=8, phrase_time_limit=12)
            return self._rec.recognize_google(audio, language='es-CO').strip()
        except Exception: return ''

    def escuchar_con_vad(self, timeout=6) -> str:
        return self.escuchar_corto()


# ── DETECTOR ──────────────────────────────────────────────

class Detector:
    def detectar(self, texto):
        tl = texto.lower().strip()
        for pa in sorted(PALABRAS_ACTIVACION, key=len, reverse=True):
            if tl == pa: return True, ''
            if tl.startswith(pa + ' '): return True, texto[len(pa):].strip()
            if pa in tl:
                idx = tl.index(pa)
                return True, texto[idx + len(pa):].strip()
        return False, ''


# ── INICIATIVA ────────────────────────────────────────────

class Iniciativa:
    def __init__(self, nest):
        self._nest    = nest
        self._activa  = False
        self._ultimo  = time.time()

    def iniciar(self):
        self._activa = True
        threading.Thread(target=self._loop, daemon=True).start()

    def detener(self): self._activa = False

    def _loop(self):
        time.sleep(120)
        while self._activa:
            try:
                if time.time() - self._ultimo >= 300:
                    msg = self._generar()
                    if msg:
                        print(f'\n  🌿 Bell (iniciativa): "{msg}"')
                        self._nest.hablar(msg, bloquear=False)
                        self._ultimo = time.time()
                time.sleep(30)
            except Exception: time.sleep(60)

    def _generar(self) -> str:
        try:
            from biblioteca.memoria.memoria_persistente import MemoriaPersistente
            mem = MemoriaPersistente.obtener()
            p = mem.obtener_pendientes_relevantes()
            if p:
                return random.choice([
                    f'Oye, ¿pudiste resolver lo de "{p[-1].get("texto","")[:35]}"?',
                    'Me quedé pensando en lo que me contaste. ¿Cómo quedó?',
                ])
            t = mem.obtener_temas_para_iniciativa()
            mapa = {
                'belladonna': '¿Cómo va el proyecto?',
                'trabajo':    '¿Cómo va el trabajo?',
                'estudio':    '¿Cómo van los estudios?',
                'codigo':     '¿Cómo va el código?',
            }
            if t:
                return mapa.get(random.choice(t), '')
        except Exception: pass
        h = datetime.now().hour
        if h in (8,9):   return 'Buenos días. ¿Cómo empezaste?'
        if h in (12,13): return '¿Cómo va el día?'
        if h in (18,19): return '¿Cómo te fue hoy?'
        if h >= 22:      return 'Es tarde. Descansa cuando puedas.'
        return ''

    def forzar(self):
        msg = self._generar()
        if msg:
            print(f'\n  🌿 Bell: "{msg}"')
            self._nest.hablar(msg)
        self._ultimo = time.time()


# ── COMUNICACIÓN CON BELL ─────────────────────────────────

def enviar(mensaje: str) -> str:
    try:
        r = requests.post(URL_BELL, json={'mensaje': mensaje}, timeout=30)
        return r.json().get('respuesta', '') if r.status_code == 200 else ''
    except requests.ConnectionError:
        return 'El servidor no está corriendo. Inicia main.py primero.'
    except Exception: return ''


# ── MODO VOZ ──────────────────────────────────────────────

class ModoVoz:

    def __init__(self, modo='siempre', nombre_nest=None):
        self.modo    = modo
        self._activo = False

        print('\n' + '='*55)
        print('     🌿 BELL — MODO VOZ + NEST MINI 🌿')
        print('='*55 + '\n')

        # Nest Mini — boca de Bell
        print('  Conectando al Nest Mini...')
        self._nest = HabladorNest(nombre_nest)
        print()

        # Micrófono — oído de Bell
        print('  Iniciando sistema de audio...')
        esc_raw = _crear_escuchador()
        self._esc  = esc_raw or EscuchadorFallback()
        self._det  = Detector()
        self._inic = Iniciativa(self._nest)
        print()

    def iniciar(self):
        self._activo = True
        if self._nest.disponible:
            self._inic.iniciar()

        saludo = random.choice([
            'Bell activa. Di "Bell" cuando me necesites.',
            'Aquí estoy. Di "Bell" para hablar.',
            'Lista. Di "Bell" cuando quieras.',
        ])
        print(f'\n  🌿 Bell → Nest: "{saludo}"')
        self._nest.hablar(saludo)

        if self.modo == 'siempre' and self._esc.ok:
            self._loop_siempre()
        else:
            self._loop_pulsa()

    def _loop_siempre(self):
        print('\n  👂 Escuchando... (di "Bell" | escribe aquí | Ctrl+C = salir)\n')
        threading.Thread(target=self._hilo_teclado, daemon=True).start()

        while self._activo:
            try:
                texto = self._esc.escuchar_corto()
                if not texto: continue

                es_act, inline = self._det.detectar(texto)
                if not es_act: continue

                print(f'\n  🔔 "{texto}"')

                if inline and len(inline) > 2:
                    self._procesar(inline)
                else:
                    self._nest.hablar('Dime.', bloquear=False)
                    time.sleep(0.8)
                    msg = self._esc.escuchar_con_vad(timeout=10)
                    if msg:
                        self._procesar(msg)
                    else:
                        self._nest.hablar('No escuché nada.', bloquear=False)

                print('\n  👂 Escuchando...')

            except KeyboardInterrupt: break
            except Exception: continue

        self._fin()

    def _loop_pulsa(self):
        sin_mic = not self._esc.ok
        if sin_mic:
            print('\n  MODO TEXTO — escribe tu mensaje y presiona Enter')
        else:
            print('\n  [Enter]=voz | texto=directo | bell=iniciativa | salir')
        print()

        while self._activo:
            try:
                ent = input('  > ').strip()
                if not ent or ent.lower() == 'salir': break
                if ent.lower() in ('bell','bella'):
                    self._inic.forzar(); continue
                if not sin_mic and ent == '':
                    print('  🎤 Habla...')
                    msg = self._esc.escuchar_con_vad()
                    if msg: self._procesar(msg)
                    else: print('  (no escuché nada)')
                else:
                    self._procesar(ent)
            except (KeyboardInterrupt, EOFError): break
        self._fin()

    def _hilo_teclado(self):
        while self._activo:
            try:
                ent = input()
                if ent.strip().lower() == 'salir':
                    self._activo = False; break
                if ent.strip().lower() in ('bell','bella'):
                    self._inic.forzar()
                elif ent.strip():
                    self._procesar(ent.strip())
            except (KeyboardInterrupt, EOFError):
                self._activo = False; break

    def _procesar(self, mensaje: str):
        print(f'  Sebastian: "{mensaje}"')
        print('  ⚙️  Bell pensando...', end='', flush=True)
        resp = enviar(mensaje)
        if resp:
            print(f'\r  🌿 Bell → Nest: "{resp}"          ')
            self._nest.hablar(resp)
        else:
            print('\r  ❌ Sin respuesta — ¿está main.py corriendo?')
            self._nest.hablar('Algo falló. Intenta de nuevo.')

    def _fin(self):
        self._activo = False
        self._inic.detener()
        desp = random.choice(['Hasta cuando quieras.','Aquí voy a estar.','Cuídate.'])
        print(f'\n  🌿 Bell: "{desp}"')
        self._nest.hablar(desp)


# ── MAIN ──────────────────────────────────────────────────

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--modo','-m', choices=['siempre','pulsa'], default='siempre')
    p.add_argument('--nest','-n', type=str, default=None,
                   help='Nombre del Nest Mini en Google Home')
    args = p.parse_args()
    ModoVoz(modo=args.modo, nombre_nest=args.nest).iniciar()


if __name__ == '__main__':
    main()