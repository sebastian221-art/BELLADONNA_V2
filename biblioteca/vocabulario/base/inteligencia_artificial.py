# biblioteca/vocabulario/base/inteligencia_artificial.py
# ================================================
# IA Y MACHINE LEARNING
# Bell habla de su propia naturaleza y tecnología
# ================================================

IA_ML = {

    # ── CONCEPTOS CORE IA ─────────────────────────
    'inteligencia artificial': {'id': 'IA_CORE',      'tipo': 'concepto_ia',  'grounding_base': 0.95, 'variantes': ['IA', 'ia', 'AI', 'artificial intelligence']},
    'modelo':      {'id': 'IA_MODELO',      'tipo': 'concepto_ia',    'grounding_base': 0.93, 'variantes': ['modelos', 'model', 'LLM', 'llm', 'modelo de lenguaje']},
    'entrenamiento':{'id': 'IA_ENTRENA',    'tipo': 'proceso_ia',     'grounding_base': 0.92, 'variantes': ['entrenar', 'entrenado', 'training', 'fine-tuning', 'finetuning']},
    'dataset':     {'id': 'IA_DATASET',     'tipo': 'datos_ia',       'grounding_base': 0.92, 'variantes': ['datos de entrenamiento', 'data', 'ejemplos']},
    'fine tuning': {'id': 'IA_FINETUNE',    'tipo': 'proceso_ia',     'grounding_base': 0.92, 'variantes': ['fine-tuning', 'finetuning', 'ajuste fino', 'reentrenar']},
    'token':       {'id': 'IA_TOKEN',       'tipo': 'unidad_ia',      'grounding_base': 0.88, 'variantes': ['tokens', 'tokenizar', 'tokenización']},
    'prompt':      {'id': 'IA_PROMPT',      'tipo': 'entrada_ia',     'grounding_base': 0.92, 'variantes': ['prompts', 'instrucción', 'instrucción al modelo']},
    'embedding':   {'id': 'IA_EMBEDDING',   'tipo': 'representacion', 'grounding_base': 0.88, 'variantes': ['embeddings', 'vectores', 'representación vectorial']},
    'inferencia':  {'id': 'IA_INFERENCIA',  'tipo': 'proceso_ia',     'grounding_base': 0.87, 'variantes': ['inference', 'generar respuesta', 'output']},
    'hallucination':{'id': 'IA_HALLUC',     'tipo': 'problema_ia',    'grounding_base': 0.88, 'variantes': ['alucinación', 'alucinaciones', 'inventar', 'inventando']},

    # ── MODELOS Y PLATAFORMAS ────────────────────
    'groq':        {'id': 'IA_GROQ',        'tipo': 'plataforma_ia',  'grounding_base': 0.93, 'variantes': ['Groq', 'groq api', 'groq cloud']},
    'llama':       {'id': 'IA_LLAMA',       'tipo': 'modelo_ia',      'grounding_base': 0.90, 'variantes': ['Llama', 'llama3', 'llama 3', 'meta llama']},
    'ollama':      {'id': 'IA_OLLAMA',      'tipo': 'herramienta_ia', 'grounding_base': 0.88, 'variantes': ['Ollama', 'modelo local']},
    'chatgpt':     {'id': 'IA_CHATGPT',     'tipo': 'modelo_externo', 'grounding_base': 0.90, 'variantes': ['ChatGPT', 'chat gpt', 'gpt', 'GPT']},
    'openai':      {'id': 'IA_OPENAI',      'tipo': 'empresa_ia',     'grounding_base': 0.90, 'variantes': ['OpenAI', 'open ai']},
    'gguf':        {'id': 'IA_GGUF',        'tipo': 'formato_modelo', 'grounding_base': 0.88, 'variantes': ['GGUF', 'formato gguf', 'cuantización']},
    'safetensors': {'id': 'IA_SAFETENSORS', 'tipo': 'formato_modelo', 'grounding_base': 0.85, 'variantes': ['SafeTensors', 'pesos del modelo']},
    'hugging face':{'id': 'IA_HF',          'tipo': 'plataforma_ia',  'grounding_base': 0.88, 'variantes': ['huggingface', 'HuggingFace', 'hf', 'hub']},
    'lora':        {'id': 'IA_LORA',        'tipo': 'tecnica_ia',     'grounding_base': 0.87, 'variantes': ['LoRA', 'low-rank adaptation']},

    # ── BELL Y SU ARQUITECTURA ────────────────────
    'mente pura':  {'id': 'BELL_MENTE_PURA','tipo': 'principio_bell', 'grounding_base': 0.98, 'variantes': ['menté pura', 'principio mente pura']},
    'motor bell':  {'id': 'BELL_MOTOR',     'tipo': 'componente_bell','grounding_base': 0.98, 'variantes': ['bell motor', 'motor de bell', 'mi motor']},
    'bell core':   {'id': 'BELL_CORE',      'tipo': 'componente_bell','grounding_base': 0.98, 'variantes': ['bell_core', 'BELL_CORE', 'neurona de identidad']},
    'capa':        {'id': 'BELL_CAPA',      'tipo': 'componente_bell','grounding_base': 0.95, 'variantes': ['capas', 'layer', 'layers']},
    'habilidad':   {'id': 'BELL_HABILIDAD', 'tipo': 'componente_bell','grounding_base': 0.93, 'variantes': ['habilidades', 'skill', 'skills']},
    'nodo':        {'id': 'BELL_NODO',      'tipo': 'componente_bell','grounding_base': 0.92, 'variantes': ['nodos', 'node', 'nodes', 'neurona']},
    'zona de desconocimiento': {'id': 'BELL_ZD','tipo': 'componente_bell','grounding_base': 0.95, 'variantes': ['zona desconocimiento', 'zona de aprendizaje']},
}
