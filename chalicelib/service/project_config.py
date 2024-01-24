

class ProjectConfig:
    def __init__(self, name=None, ecs_cluster_name=None, ecs_service_name=None):
        self.name = name
        self.ecs_cluster_name = ecs_cluster_name
        self.ecs_service_name = ecs_service_name