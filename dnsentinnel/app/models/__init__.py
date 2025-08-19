import os
import importlib

def auto_import_models():
    models_dir = os.path.dirname(__file__)
    for filename in os.listdir(models_dir):
        if filename.endswith('.py') and not filename.startswith('_') and filename != '__init__.py':
            module_name = f"{__name__}.{filename[:-3]}"
            importlib.import_module(module_name)

auto_import_models()
