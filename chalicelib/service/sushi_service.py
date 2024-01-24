
import json
import os
import logging
import pytz

from chalicelib.service.project_config import ProjectConfig
from chalicelib.service.server_service import ServerService


class SushiService(object):

    def __init__(self):
        self.logger = logging.getLogger("backend-pocsoft")
        self.env = os.getenv("env")

        project_config = ProjectConfig(name="sushi", ecs_api_service_name="sushi-api", ecs_graphql_service_name=None)
        self.server_service = ServerService(project_config=project_config)


    def shutoff_services_for_inactivity(self):
        

        pass

