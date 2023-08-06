"""Logger configuration"""
import logging


def configure_logging(name):
    """Configure logging with file path"""
    root = logging.getLogger(name)
    root.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s:bdb:%(module)s: %(message)s')
    default_handler = logging.StreamHandler()
    default_handler.setFormatter(formatter)
    root.addHandler(default_handler)
    root.propagate = False
    return root
