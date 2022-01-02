from functools import wraps
from pycore.core_funcs import stdio
from pycore.models.diagnostics import CommandDiagnostics


def enable_diagnostics(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        diag = CommandDiagnostics()
        diag.start()
        result = func(*args, **kwargs)
        diag.end()
        stdio.report_diagnostics(diag)
        return result
    return wrapper
