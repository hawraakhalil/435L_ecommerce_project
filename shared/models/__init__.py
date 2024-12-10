import os
import importlib

def import_models():
    models_path = os.path.dirname(__file__)
    for file in os.listdir(models_path):
        if file.endswith('.py') and file != '__init__.py':
            module_name = f"shared.models.{file[:-3]}"
            importlib.import_module(module_name)

import_models()
