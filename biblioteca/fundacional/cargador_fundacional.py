# biblioteca/fundacional/cargador_fundacional.py
# ================================================
# CARGADOR FUNDACIONAL — v5
# SIN llamada a Biblioteca.obtener() — eso era
# la causa de la recursión infinita.
# El auto-registro se hace DESDE biblioteca/__init__.py
# DESPUÉS de que el cargador termina.
# ================================================

class CargadorFundacional:

    def __init__(self, red_neuronal):
        self.red     = red_neuronal
        self.cargado = False

    def cargar_todo(self) -> bool:
        if self.cargado:
            return True

        print('  Cargando núcleo fundacional...')
        try:
            self._cargar_identidad()
            self._cargar_valores()
            self._cargar_consejeras()
            self._cargar_sebastian()
            self._cargar_vocabulario()
            self._cargar_capacidades()

            self.cargado = True
            total = len(self.red.obtener_todos_los_nodos())
            print(f'  ✓ Fundacional listo: {total} nodos base')
            return True

        except Exception as e:
            import traceback
            print(f'  ✗ Error en fundacional: {e}')
            traceback.print_exc()
            return False

    # ==========================================
    # CARGADORES INDIVIDUALES
    # ==========================================

    def _cargar_identidad(self):
        from biblioteca.fundacional.identidad.bell_core import crear_bell_core
        from biblioteca.fundacional.identidad.proposito import crear_proposito
        crear_bell_core(self.red)
        crear_proposito(self.red)
        print('    ✓ Identidad')

    def _cargar_valores(self):
        from biblioteca.fundacional.valores.valores_bell import crear_valores
        crear_valores(self.red)
        print('    ✓ Valores')

    def _cargar_consejeras(self):
        from biblioteca.fundacional.consejeras.neuronas_consejeras import (
            crear_neuronas_consejeras
        )
        crear_neuronas_consejeras(self.red)
        print('    ✓ Consejeras (neuronas base)')

    def _cargar_sebastian(self):
        from biblioteca.fundacional.sebastian.neurona_sebastian import (
            crear_neurona_sebastian
        )
        crear_neurona_sebastian(self.red)
        print('    ✓ Sebastian')

    def _cargar_vocabulario(self):
        from biblioteca.fundacional.vocabulario.neuronas_saludos    import crear_neuronas_saludos
        from biblioteca.fundacional.vocabulario.neuronas_preguntas  import crear_neuronas_preguntas
        from biblioteca.fundacional.vocabulario.neuronas_emociones  import crear_neuronas_emociones
        from biblioteca.fundacional.vocabulario.neuronas_verbos     import crear_neuronas_verbos
        from biblioteca.fundacional.vocabulario.neuronas_tiempo     import crear_neuronas_tiempo
        from biblioteca.fundacional.vocabulario.neuronas_conectores import crear_neuronas_conectores

        crear_neuronas_saludos(self.red)
        crear_neuronas_preguntas(self.red)
        crear_neuronas_emociones(self.red)
        crear_neuronas_verbos(self.red)
        crear_neuronas_tiempo(self.red)
        crear_neuronas_conectores(self.red)

        total_vocab = sum(
            1 for n in self.red.obtener_todos_los_nodos()
            if (nr := self.red.obtener_neurona(n)) and
               nr.nucleo.tipo == 'concepto'
        )
        print(f'    ✓ Vocabulario: {total_vocab} conceptos')

    def _cargar_capacidades(self):
        from biblioteca.fundacional.capacidades.neurona_biblioteca  import crear_neurona_biblioteca
        from biblioteca.fundacional.capacidades.neuronas_capas      import crear_neuronas_capas
        from biblioteca.fundacional.capacidades.neuronas_habilidades import crear_neuronas_habilidades
        from biblioteca.fundacional.capacidades.neuronas_interfaz   import crear_neuronas_interfaz

        crear_neurona_biblioteca(self.red)
        crear_neuronas_capas(self.red)
        crear_neuronas_habilidades(self.red)
        crear_neuronas_interfaz(self.red)

        total_caps = sum(
            1 for n in self.red.obtener_todos_los_nodos()
            if (nr := self.red.obtener_neurona(n)) and
               nr.nucleo.tipo in ('capacidad', 'habilidad', 'interfaz')
        )
        print(f'    ✓ Capacidades: {total_caps} nodos')

        # ─── NOTA ────────────────────────────────────────────────────
        # El auto-registro del proyecto se hace DESDE biblioteca/__init__.py
        # DESPUÉS de que este método retorna, para evitar la recursión
        # infinita que ocurría al llamar Biblioteca.obtener() desde aquí.
        # ─────────────────────────────────────────────────────────────