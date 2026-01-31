import logging
import sys
from logtail import LogtailHandler
from src.config import configs


logger=logging.getLogger("__name__")

formatter=logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

stream_handler=logging.StreamHandler(sys.stdout)
file_handler=logging.FileHandler("app.log")
# betterstackhandler=LogtailHandler(source_token=configs.BetterStack)

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.handlers=([file_handler,stream_handler]) #add betterstackhandler if using
logger.setLevel(logging.INFO)