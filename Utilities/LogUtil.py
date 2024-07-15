import logging
import time
import os


class Logger:
    def __init__(self, logger, file_level=logging.INFO):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        fmt = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
        curr_time = time.strftime("%Y-%m-%d")
        log_dir = os.path.join(os.getenv('CI_PROJECT_DIR', '.'), 'Logs')
        self.FileName = os.path.join(log_dir, f"{curr_time}.txt")

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        fh = logging.FileHandler(self.FileName, mode='a')
        fh.setFormatter(fmt)
        fh.setLevel(file_level)
        self.logger.addHandler(fh)

