# -*- coding:Utf-8 -*-

import os
import sys
import logging


class Logger(object):
    def __init__(self, name, log_name):
        self.name = name
        self.log_name = log_name

    def get_logger(self, debug=False, stdout=True, fdout=True):
        log = logging.getLogger(self.name)
        log.propagate = False
        log.handlers = []

        if debug:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)

        format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        if stdout:
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(format)
            log.addHandler(ch)

        if fdout:
            log_dir_path = os.path.join(os.getcwd(), "logs")
            log_file_path = os.path.join(log_dir_path, self.log_name)

            if not os.path.isdir(log_dir_path):
                os.mkdir(log_dir_path)

            if not os.path.isfile(log_file_path):
                f = open(log_file_path, "w+")
                f.write("# Log start")
                f.close()

            fh = logging.FileHandler(log_file_path)

            fh.setFormatter(format)
            log.addHandler(fh)

        return log


log = Logger("katana", "katana.log").get_logger(debug=True, fdout=True, stdout=True)
