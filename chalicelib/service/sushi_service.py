
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

        self.project_config = ProjectConfig(name="sushi", ecs_api_service_name="sushi-api", ecs_graphql_service_name="sushi-graphql-service")
        self.server_service = ServerService(project_config=self.project_config)

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

    def turnon_servers(self):
        status = {}

        statuses = self.get_servers_status()

        status['prev_status'] = statuses

        server_status = self.server_service.turn_on_database_server()

        status.update(server_status)

        server_status = self.server_service.turn_on_ecs_api_service()

        status.update(server_status)

        server_status = self.server_service.turn_on_ecs_graphql_service()

        status.update(server_status)

        self.logger.info("status={}".format(status))

        return status

    def turnoff_servers(self):
        status = {}

        statuses = self.get_servers_status()

        status['prev_status'] = statuses

        any_project_user_activity = self.server_service.any_project_user_activity()
        self.logger.info("name={}, any_project_user_activity={}".format(self.project_config.name, any_project_user_activity))

        any_user_activity = self.server_service.any_user_activity()
        self.logger.info("any_user_activity={}".format(any_user_activity))

        db_status = statuses["db_status"]
        ecs_api_desired_count = statuses["ecs_api_desired_count"]
        ecs_graphql_desired_count = statuses["ecs_graphql_desired_count"]

        if db_status.lower() in ["available"] and any_user_activity is False:
            server_status = self.server_service.turn_off_database_server()
            status.update(server_status)

        if ecs_api_desired_count > 0:
            server_status = self.server_service.turn_off_ecs_api_service()
            status.update(server_status)

        if ecs_graphql_desired_count > 0:
            server_status = self.server_service.turn_off_ecs_graphl_service()
            status.update(server_status)

        return status

    def shutoff_services_for_inactivity(self):
        status = {}

        statuses = self.get_servers_status()

        status['prev_status'] = statuses

        any_project_user_activity = self.server_service.any_project_user_activity()
        self.logger.info("name={}, any_project_user_activity={}".format(self.project_config.name, any_project_user_activity))

        any_user_activity = self.server_service.any_user_activity()
        self.logger.info("any_user_activity={}".format(any_user_activity))

        db_status = statuses["db_status"]
        ecs_api_desired_count = statuses["ecs_api_desired_count"]
        ecs_graphql_desired_count = statuses["ecs_graphql_desired_count"]

        if any_user_activity is False:
            if db_status.lower() in ["available"]:
                server_status = self.server_service.turn_off_database_server()
                status.update(server_status)

            if ecs_api_desired_count > 0:
                server_status = self.server_service.turn_off_ecs_api_service()
                status.update(server_status)

            if ecs_graphql_desired_count > 0:
                server_status = self.server_service.turn_off_ecs_graphl_service()
                status.update(server_status)

        elif any_user_activity is True and any_project_user_activity is False:

            if ecs_api_desired_count > 0:
                server_status = self.server_service.turn_off_ecs_api_service()
                status.update(server_status)

            if ecs_graphql_desired_count > 0:
                server_status = self.server_service.turn_off_ecs_graphl_service()
                status.update(server_status)

        return status


