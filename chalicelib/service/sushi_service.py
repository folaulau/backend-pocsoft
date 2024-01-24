
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

    def get_servers_status(self):
        status = {}

        ecs_api_service_status = self.server_service.get_ecs_api_service_status()

        status.update(ecs_api_service_status)

        ecs_graphql_service_status = self.server_service.get_ecs_graphql_service_status()

        status.update(ecs_graphql_service_status)

        database_status = self.server_service.get_database_status()

        status.update(database_status)

        self.logger.info("status={}".format(status))

        return status


