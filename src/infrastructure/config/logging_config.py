# src/infrastructure/config/logging_config.py
import logging
import sys
import os
from logging.config import dictConfig


def get_logging_config():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir, exist_ok=True)
        except:
            pass 
    
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - "
                          "%(module)s:%(lineno)d - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": log_level,
            },
            "src": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
            "celery": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }
    
    try:
        test_file = os.path.join(log_dir, "test_write.log")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        
        log_config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": os.path.join(log_dir, "app.log"),
            "maxBytes": 10485760, 
            "backupCount": 5,
        }
        
        for logger in log_config["loggers"].values():
            logger["handlers"].append("file")
            
    except (PermissionError, OSError):
        print("Warning: Cannot write to logs directory. Logging to console only.")
    
    return log_config


def setup_logging():
    log_config = get_logging_config()
    dictConfig(log_config)