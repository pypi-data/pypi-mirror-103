"""
Copyright 2020 Beijing Volcano Engine Technology Co., Ltd.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
Apache License, Version 2.0
Home page of The Apache Software Foundation
"""
import os, datetime, logging


class RangersWriter:
    def __init__(self, log_file_path: str, log_file_name: str, max_size=1024 * 1024 * 1, backup_count=36):
        self.prefix = log_file_path
        if not os.path.exists(self.prefix):
            os.mkdir(self.prefix)
        if log_file_name.endswith(".log"):
            log_file_name = log_file_name[0:-4]
        self.file_name = "{}-{}{}".format(log_file_name, datetime.datetime.now().strftime("%Y-%m-%d-%H"), ".log")
        self.write_name = os.path.join(self.prefix, "{}.log".format(log_file_name))
        self.full_name = os.path.join(self.prefix, self.file_name)
        self.name = log_file_name
        self.max_size = max_size
        self.backup_count = backup_count
        self.write_logger = self.init_logger()

    def init_logger(self):
        from logging.handlers import TimedRotatingFileHandler
        write_file = TimedRotatingFileHandler(self.write_name,
                                         backupCount=self.backup_count,
                                         encoding="utf-8")
        write_format = logging.Formatter(fmt="%(message)s")
        write_file.setFormatter(write_format)
        write_logger = logging.Logger("datarangers", level=logging.INFO)
        write_logger.addHandler(write_file)
        return write_logger

    def info(self, message):
        self.write_logger.info(message)

    def debug(self, message):
        self.info(message)
