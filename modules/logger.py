import os
import logging
import json
from typing import Union, Any

def getLogger(name: str, status: bool = False):
    logger = logging.getLogger(name)

    if status:
        logger.disabled = False
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            log_file = os.path.join("logs", f"{name}.log")
            os.makedirs("logs", exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    else:
        logger.disabled = True
        while logger.handlers:
            handler = logger.handlers.pop()
            handler.close()
            logger.removeHandler(handler)

    return logger

def configureModuleLogger(module, package: str, status: bool = False):
    logger = getLogger(package, status)

    def log(message: Union[str, int, list, dict, Any]):
        if isinstance(message, (str, int)):
            formatted_message = str(message)
        elif isinstance(message, (list, dict)):
            formatted_message = json.dumps(message, ensure_ascii=False, indent=2)
        else:
            formatted_message = repr(message)
        
        logger.info(formatted_message)

    setattr(module, "log", log)
    return logger
