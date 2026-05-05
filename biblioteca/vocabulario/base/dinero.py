# biblioteca/vocabulario/base/dinero.py
DINERO = {
    'dinero':      {'id': 'DIN_DINERO',    'tipo': 'concepto_dinero', 'grounding_base': 0.93, 'variantes': ['plata', 'guita', 'billete', 'efectivo', 'cash']},
    'pagar':       {'id': 'DIN_PAGAR',     'tipo': 'accion_economica','grounding_base': 0.92, 'variantes': ['pago', 'pagué', 'pagando', 'cancelar']},
    'cobrar':      {'id': 'DIN_COBRAR',    'tipo': 'accion_economica','grounding_base': 0.88, 'variantes': ['cobro', 'cobré', 'cobran']},
    'comprar':     {'id': 'DIN_COMPRAR',   'tipo': 'accion_economica','grounding_base': 0.92, 'variantes': ['compra', 'compré', 'comprado', 'comprando']},
    'vender':      {'id': 'DIN_VENDER',    'tipo': 'accion_economica','grounding_base': 0.88, 'variantes': ['venta', 'vendí', 'vendiendo']},
    'caro':        {'id': 'DIN_CARO',      'tipo': 'valoracion_precio','grounding_base': 0.90,'variantes': ['cara', 'caros', 'costoso', 'costosa']},
    'barato':      {'id': 'DIN_BARATO',    'tipo': 'valoracion_precio','grounding_base': 0.90,'variantes': ['barata', 'baratos', 'económico', 'economico']},
    'precio':      {'id': 'DIN_PRECIO',    'tipo': 'concepto_dinero', 'grounding_base': 0.88, 'variantes': ['precios', 'cuánto cuesta', 'cuanto vale']},
    'cuenta':      {'id': 'DIN_CUENTA',    'tipo': 'concepto_dinero', 'grounding_base': 0.87, 'variantes': ['cuentas', 'factura', 'boleta', 'recibo']},
    'deuda':       {'id': 'DIN_DEUDA',     'tipo': 'concepto_dinero', 'grounding_base': 0.87, 'variantes': ['deudas', 'debiendo', 'debo']},
    'ahorro':      {'id': 'DIN_AHORRO',    'tipo': 'concepto_dinero', 'grounding_base': 0.87, 'variantes': ['ahorros', 'ahorrar', 'guardar plata']},
    'banco':       {'id': 'DIN_BANCO',     'tipo': 'entidad_economica','grounding_base': 0.87,'variantes': ['bancos', 'cuenta bancaria']},
    'gratis':      {'id': 'DIN_GRATIS',    'tipo': 'valoracion_precio','grounding_base': 0.90,'variantes': ['gratuito', 'gratuita', 'sin costo', 'free']},
    'invertir':    {'id': 'DIN_INVERTIR',  'tipo': 'accion_economica', 'grounding_base': 0.85,'variantes': ['inversión', 'inversion', 'invertí']},
    'presupuesto': {'id': 'DIN_PRESUPUESTO','tipo': 'planificacion',  'grounding_base': 0.85,'variantes': ['budget', 'presupuestos']},
}
