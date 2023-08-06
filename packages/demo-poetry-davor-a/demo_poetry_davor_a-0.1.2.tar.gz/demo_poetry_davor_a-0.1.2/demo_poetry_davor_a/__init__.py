import psutil
from datetime import datetime
from loguru import logger

__version__ = '0.1.0'

def main():
    logger.info(system_boot_time())


def system_boot_time():
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    return f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"