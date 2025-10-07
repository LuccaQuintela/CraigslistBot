from datetime import datetime
from typing import Optional
import json
import os

class Logger:
    _log_file = "logs/logs.json"
    _initialized = False
    
    @staticmethod
    def initialize():
        """Initialize the logger by clearing the log file for a fresh start"""
        os.makedirs(os.path.dirname(Logger._log_file), exist_ok=True)
        
        with open(Logger._log_file, 'w') as f:
            f.write('')
        
        Logger._initialized = True
        Logger.log("Logger initialized - log file cleared", component="LOGGER")

    @staticmethod
    def format(msg: str, **kwargs):
        return json.dumps({
            "message": msg,
            **{k: v for k, v in kwargs.items() if v is not None},
        })
    
    @staticmethod
    def log(msg: str, severity: str = "INFO", component: Optional[str] = None, context: Optional[dict] = None):
        timestamp = datetime.now().isoformat()
        to_log = Logger.format(
            msg,
            severity=severity,
            component=component,
            context=context,
            timestamp=timestamp,
        )
        
        if not Logger._initialized:
            Logger.initialize()
        
        print(to_log)
        
        with open(Logger._log_file, 'a') as f:
            f.write(to_log + '\n')

    @staticmethod
    def warning(msg: str, component: Optional[str] = None, context: Optional[dict] = None):
        Logger.log(msg, severity="WARNING", component=component, context=context)

    @staticmethod
    def error(msg: str, component: Optional[str] = None, context: Optional[dict] = None):
        Logger.log(msg, severity="ERROR", component=component, context=context)