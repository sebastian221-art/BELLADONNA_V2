"""
Módulo de operaciones del sistema.
FASE 3 - Sistema de operaciones seguras.
"""

from .shell_executor import ShellExecutor, SecurityError

__all__ = ['ShellExecutor', 'SecurityError']