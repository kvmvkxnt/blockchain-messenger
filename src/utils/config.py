import os

LOG_LEVEL = os.getenv("LOG_LEVEL") or "INFO"
LOG_DIR = os.getenv("LOG_DIR") or os.getcwd() + "/logs"
