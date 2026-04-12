#!/usr/bin/env python3
# ARCHIVO: check_secrets.py
# QUÉ HACE: Hook PreToolUse — analiza comandos Bash y bloquea si detecta secrets
# CÓMO ENCAJA: settings.json lo llama antes de cada Bash y Write
# PARA EDITAR: agregar patrones en PATRONES_PELIGROSOS
# DEPENDENCIAS: solo librería estándar Python

import sys
import json
import re

# ─── Patrones que indican un secret hardcodeado ───────────────────────────────

PATRONES_PELIGROSOS = [
    r'(?i)(password|passwd|pwd)\s*=\s*["\']?.{4,}',
    r'(?i)(api_key|apikey)\s*=\s*["\']?[a-zA-Z0-9]{8,}',
    r'(?i)(secret_key|secret)\s*=\s*["\']?.{8,}',
    r'(?i)(token)\s*=\s*["\']?[a-zA-Z0-9\-_]{16,}',
    r'Bearer\s+[a-zA-Z0-9\-_\.]{20,}',
    r'(?i)Authorization:\s*["\']?.{10,}',
    r'eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+',  # JWT
]

# Comandos siempre permitidos
WHITELIST = [
    'python acciones/avisar.py',
    'python manage.py',
    'git status',
    'git diff',
    'git log',
    'git pull',
]

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    try:
        data    = json.load(sys.stdin)
        comando = data.get('command', '') or data.get('input', '')
    except Exception:
        comando = ' '.join(sys.argv[1:])

    if not comando:
        sys.exit(0)

    for w in WHITELIST:
        if comando.strip().startswith(w):
            sys.exit(0)

    for patron in PATRONES_PELIGROSOS:
        if re.search(patron, comando):
            print(f'[check_secrets] BLOQUEADO — posible secret detectado.')
            print(f'[check_secrets] Patron: {patron}')
            print(f'[check_secrets] Usa .env + .env.example — nunca hardcodes.')
            sys.exit(2)

    sys.exit(0)

if __name__ == '__main__':
    main()
