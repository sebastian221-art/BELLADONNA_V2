# biblioteca/fundacional/cargador_fundacional.py
# ================================================
# CARGADOR FUNDACIONAL — versión 4
# Ahora aplica grounding de vida después de cargar
# ================================================

class CargadorFundacional:

    def __init__(self, red_neuronal):
        self.red     = red_neuronal
        self.cargado = False

    def cargar_todo(self):
        if self.cargado:
            print('Fundacional: ya cargado')
            return True

        print('Cargando nodos fundacionales de Belladonna...')

        try:
            self._cargar_identidad()
            self._cargar_valores()
            self._cargar_consejeras()
            self._cargar_sebastian()
            self._cargar_vocabulario()
            self._cargar_capacidades()

            self.cargado = True
            total = len(self.red.obtener_todos_los_nodos())
            print(f'Fundacional cargado: {total} nodos base')
            return True

        except Exception as e:
            import traceback
            print(f'Error cargando fundacional: {e}')
            traceback.print_exc()
            return False

    def _cargar_identidad(self):
        from biblioteca.fundacional.identidad.bell_core import crear_bell_core
        from biblioteca.fundacional.identidad.proposito import crear_proposito
        crear_bell_core(self.red)
        crear_proposito(self.red)
        print('  ✓ Identidad cargada')

    def _cargar_valores(self):
        from biblioteca.fundacional.valores.valores_bell import crear_valores
        crear_valores(self.red)
        print('  ✓ Valores cargados')

    def _cargar_consejeras(self):
        from biblioteca.fundacional.consejeras.neuronas_consejeras import (
            crear_neuronas_consejeras
        )
        crear_neuronas_consejeras(self.red)
        print('  ✓ Consejeras cargadas')

    def _cargar_sebastian(self):
        from biblioteca.fundacional.sebastian.neurona_sebastian import (
            crear_neurona_sebastian
        )
        crear_neurona_sebastian(self.red)
        print('  ✓ Sebastian cargado')

    def _cargar_vocabulario(self):
        from biblioteca.fundacional.vocabulario.neuronas_saludos import crear_neuronas_saludos
        from biblioteca.fundacional.vocabulario.neuronas_preguntas import crear_neuronas_preguntas
        from biblioteca.fundacional.vocabulario.neuronas_emociones import crear_neuronas_emociones
        from biblioteca.fundacional.vocabulario.neuronas_verbos import crear_neuronas_verbos
        from biblioteca.fundacional.vocabulario.neuronas_tiempo import crear_neuronas_tiempo
        from biblioteca.fundacional.vocabulario.neuronas_conectores import crear_neuronas_conectores

        crear_neuronas_saludos(self.red)
        crear_neuronas_preguntas(self.red)
        crear_neuronas_emociones(self.red)
        crear_neuronas_verbos(self.red)
        crear_neuronas_tiempo(self.red)
        crear_neuronas_conectores(self.red)

        total_vocab = sum(
            1 for n in self.red.obtener_todos_los_nodos()
            if self.red.obtener_neurona(n) and
               self.red.obtener_neurona(n).nucleo.tipo == 'concepto'
        )
        print(f'  ✓ Vocabulario cargado: {total_vocab} conceptos en la red')

    def _cargar_capacidades(self):
        print('  Cargando capacidades de Bell...')

        from biblioteca.fundacional.capacidades.neurona_biblioteca import crear_neurona_biblioteca
        from biblioteca.fundacional.capacidades.neuronas_capas import crear_neuronas_capas
        from biblioteca.fundacional.capacidades.neuronas_habilidades import crear_neuronas_habilidades
        from biblioteca.fundacional.capacidades.neuronas_interfaz import crear_neuronas_interfaz

        crear_neurona_biblioteca(self.red)
        crear_neuronas_capas(self.red)
        crear_neuronas_habilidades(self.red)
        crear_neuronas_interfaz(self.red)

        total_caps = sum(
            1 for n in self.red.obtener_todos_los_nodos()
            if self.red.obtener_neurona(n) and
               self.red.obtener_neurona(n).nucleo.tipo in [
                   'capacidad', 'habilidad', 'interfaz'
               ]
        )
        print(f'  ✓ Capacidades cargadas: {total_caps} nodos en la red')
        self._auto_registrar_proyecto()

    def _auto_registrar_proyecto(self):
        try:
            from biblioteca.registrador_automatico import RegistradorAutomatico
            from biblioteca import Biblioteca
            biblioteca = Biblioteca.obtener()
            registrador = RegistradorAutomatico(biblioteca)

            import os
            raiz = os.environ.get('BELLADONNA_ROOT', '')
            if not raiz:
                from pathlib import Path
                raiz = str(Path(__file__).parent.parent.parent.parent)

            total = registrador.registrar_todo_el_proyecto(raiz)
            if total > 0:
                print(f'  ✓ Auto-registro: {total} nuevos nodos integrados')
            else:
                print('  ✓ Auto-registro: todo ya estaba en la red')

        except Exception as e:
            print(f'  ⚠ Auto-registro: {e}')