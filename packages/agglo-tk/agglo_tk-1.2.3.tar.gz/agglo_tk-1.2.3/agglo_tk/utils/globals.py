import sys

def set_global(module_name, var_name, value):
    setattr(sys.modules[module_name], var_name, value)