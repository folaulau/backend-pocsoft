
import json
import os
import logging
import pytz



class SushiService(object):

    def __init__(self):
        self.logger = logging.getLogger("my-trader-lambdas")

        self.env = os.getenv("env")

        self.cache = DictCache()

        self.server_service = ServerService()