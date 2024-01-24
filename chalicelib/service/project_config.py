import os

class ProjectConfig:
    def __init__(self, name=None, ecs_api_service_name=None, ecs_graphql_service_name=None):
        self.name = name
        self.ecs_cluster_name = os.getenv("ecs_cluster")
        self.ecs_api_service_name = ecs_api_service_name
        self.ecs_graphql_service_name = ecs_graphql_service_name