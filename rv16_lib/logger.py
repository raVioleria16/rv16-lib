import logging

def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance that uses uvicorn's configuration.

    Args:
        name: Optional name for the logger. If None, uses 'uvicorn'
    """
    if name:
        # Create a child logger under uvicorn to maintain the same formatting
        return logging.getLogger(f"uvicorn.{name}")
    return logging.getLogger("uvicorn")


# For convenience, you can also export a default logger
logger = get_logger()
