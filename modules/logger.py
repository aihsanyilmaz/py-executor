import os
import logging

def getLogger(name: str, status: bool = False):
    logger = logging.getLogger(name)

    if status:
        logger.disabled = False
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            log_file = os.path.join("logs", f"{name}.log")
            os.makedirs("logs", exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(message)s")
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

    def log(message: str):
        logger.info(message)

    setattr(module, "log", log)
    return logger
