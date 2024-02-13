import logging
import time


class Logger:
    def __init__(self,logger,file_level=logging.INFO):
        self.logger=logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        fmt=logging.Formatter('%(asctime)s - %(filename)s -%(levelname)s - %(message)s')
        curr_time=time.strftime("%Y-%m-%d")
        self.FileName='..//Log//log'+ curr_time + ".txt"
        fh=logging.FileHandler(self.FileName,mode='a')
        fh.setFormatter(fmt)
        fh.setLevel(file_level)
        self.logger.addHandler(fh)