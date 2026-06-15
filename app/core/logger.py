import logging
import os

os.makedirs("logs" , exist_ok = True)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger
    
    #Handler Terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    #Handler Save File
    file_handler = logging.FileHandler(
        "logs/app.log",
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)

    #Format Message
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    #Add Format
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    #Add handler
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

