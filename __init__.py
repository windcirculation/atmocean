"""Top‑level package for the *atmocean* project.

Lazy imports are used to avoid side effects (e.g., reading environment
variables) when the package is imported.
"""

from importlib import import_module as _import_module

def __getattr__(name: str):  # pragma: no cover – dynamic import shim
    mapping = {
        "bot_status": (".job_bot", "bot_status"),
        "postbot": (".job_bot", "postbot"),
        "esjobs": (".es_jobs_net", "esjobs"),
        "metjobs": (".met_jobs", "metjobs"),
        "egujobs": (".egu_jobs", "egujobs"),
    }
    if name in mapping:
        module_name, attr = mapping[name]
        return getattr(_import_module(module_name, __name__), attr)
    raise AttributeError(name)

package_variable = "This is a package-level variable."

__all__ = ["bot_status", "postbot", "esjobs", "metjobs", "egujobs", "package_variable"]
