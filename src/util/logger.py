import logging
from datetime import datetime
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    f'logs/{datetime.now().strftime("%d.%m.%Y_%H-%M-%S")}.log',
    mode='a',
    encoding='utf-8'
)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
