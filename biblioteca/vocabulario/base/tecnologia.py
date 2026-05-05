# biblioteca/vocabulario/base/tecnologia.py
# ================================================
# TECNOLOGÍA — Expandida (24 → 80+ entradas)
# ================================================

CONCEPTOS_TECNOLOGIA = {
    # Dispositivos
    'celular':     {'id': 'TEC_CELULAR',    'tipo': 'dispositivo', 'grounding_base': 0.93, 'variantes': ['teléfono', 'telefono', 'móvil', 'movil', 'smartphone', 'cel']},
    'computador':  {'id': 'TEC_PC',         'tipo': 'dispositivo', 'grounding_base': 0.93, 'variantes': ['computadora', 'laptop', 'portátil', 'portatil', 'pc', 'computador portátil']},
    'tablet':      {'id': 'TEC_TABLET',     'tipo': 'dispositivo', 'grounding_base': 0.87, 'variantes': ['tableta', 'iPad', 'ipad']},
    'parlante':    {'id': 'TEC_PARLANTE',   'tipo': 'dispositivo', 'grounding_base': 0.90, 'variantes': ['parlantes', 'altavoz', 'bocina', 'speaker', 'nest mini', 'google home']},
    'teclado':     {'id': 'TEC_TECLADO',    'tipo': 'periferico',  'grounding_base': 0.88, 'variantes': ['teclados', 'keyboard']},
    'pantalla':    {'id': 'TEC_PANTALLA',   'tipo': 'periferico',  'grounding_base': 0.87, 'variantes': ['pantallas', 'monitor', 'display', 'screen']},
    'mouse':       {'id': 'TEC_MOUSE',      'tipo': 'periferico',  'grounding_base': 0.87, 'variantes': ['ratón', 'raton']},
    'auricular':   {'id': 'TEC_AURICULAR',  'tipo': 'periferico',  'grounding_base': 0.87, 'variantes': ['audífonos', 'audifonos', 'auriculares', 'headphones', 'earphones']},

    # Software y sistemas
    'aplicación':  {'id': 'TEC_APP',        'tipo': 'software',    'grounding_base': 0.90, 'variantes': ['aplicacion', 'app', 'apps', 'programa']},
    'sistema':     {'id': 'TEC_SISTEMA',    'tipo': 'software',    'grounding_base': 0.88, 'variantes': ['sistemas', 'sistema operativo', 'OS', 'windows', 'linux']},
    'actualizar':  {'id': 'TEC_ACTUALIZAR', 'tipo': 'accion_tec',  'grounding_base': 0.88, 'variantes': ['actualización', 'update', 'versión nueva']},
    'descargar':   {'id': 'TEC_DESCARGAR',  'tipo': 'accion_tec',  'grounding_base': 0.90, 'variantes': ['descarga', 'download', 'bajar', 'bajar el archivo']},
    'instalar':    {'id': 'TEC_INSTALAR',   'tipo': 'accion_tec',  'grounding_base': 0.90, 'variantes': ['instalación', 'install', 'instalando', 'configurar']},
    'conectar':    {'id': 'TEC_CONECTAR',   'tipo': 'accion_tec',  'grounding_base': 0.88, 'variantes': ['conexión', 'conectado', 'conectarse']},

    # Conceptos técnicos
    'wifi':        {'id': 'TEC_WIFI',       'tipo': 'conectividad','grounding_base': 0.92, 'variantes': ['wi-fi', 'internet inalámbrico', 'sin señal', 'red wifi']},
    'internet':    {'id': 'TEC_INTERNET',   'tipo': 'red',         'grounding_base': 0.93, 'variantes': ['el internet', 'la red', 'en línea', 'online', 'offline']},
    'nube':        {'id': 'TEC_NUBE',       'tipo': 'almacenamiento','grounding_base': 0.87,'variantes': ['cloud', 'en la nube', 'almacenamiento en la nube']},
    'contraseña':  {'id': 'TEC_PASSWORD',   'tipo': 'seguridad',   'grounding_base': 0.88, 'variantes': ['clave', 'password', 'pin', 'clave de acceso']},
    'lento':       {'id': 'TEC_LENTO',      'tipo': 'problema_tec','grounding_base': 0.87, 'variantes': ['está lento', 'lagueando', 'lag', 'se colgó']},
    'reiniciar':   {'id': 'TEC_REINICIAR',  'tipo': 'accion_tec',  'grounding_base': 0.87, 'variantes': ['reinicio', 'restart', 'apagar y encender']},
    'notificación':{'id': 'TEC_NOTIF',      'tipo': 'elemento_tec','grounding_base': 0.87, 'variantes': ['notificaciones', 'alerta', 'notif']},
    'configuración':{'id': 'TEC_CONFIG',    'tipo': 'accion_tec',  'grounding_base': 0.87, 'variantes': ['configurar', 'settings', 'ajustes', 'parametros']},
}


