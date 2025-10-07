from datetime import datetime
from typing import Optional
import json

class Logger:
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
        print(to_log)

    @staticmethod
    def warning(msg: str, component: Optional[str] = None, context: Optional[dict] = None):
        Logger.log(msg, severity="WARNING", component=component, context=context)

    @staticmethod
    def error(msg: str, component: Optional[str] = None, context: Optional[dict] = None):
        Logger.log(msg, severity="ERROR", component=component, context=context)