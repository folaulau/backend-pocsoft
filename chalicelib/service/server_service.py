import boto3
import json
import os
import logging
from datetime import timedelta, datetime
from pytz import timezone
import pytz

from chalicelib.service.project_config import ProjectConfig


class ServerService(object):

    def __init__(self, project_config: ProjectConfig):
        self.logger = logging.getLogger("backend-pocsoft")

        self.env = os.getenv("env")

        if self.env == "local":
            session = boto3.Session(region_name="us-west-2", profile_name='folau')
        else:
            session = boto3.Session(region_name="us-west-2")

        self.rds_client = session.client('rds')
        self.ecs_client = session.client('ecs')
        self.s3_client = session.client('s3')
        self.project_config = project_config

    def get_ecs_api_service_status(self) -> dict:

        result = {}

        ecs_cluster = self.project_config.ecs_cluster_name

        self.logger.info("ecs_cluster: "+ecs_cluster)

        ecs_api_service = self.project_config.ecs_api_service_name

        self.logger.info("ecs_api_service: "+ecs_api_service)

        try:
            response = self.ecs_client.describe_services(
                cluster=ecs_cluster,
                services=[ecs_api_service]
            )

            if len(response['services']) > 0:

                service = response['services'][0]
                status = service['status']
                desired_count = service['desiredCount']
                running_count = service['runningCount']
                pending_count = service['pendingCount']

                result['ecs_api_status'] = status
                result['ecs_api_desired_count'] = desired_count
                result['ecs_api_running_count'] = running_count
                result['ecs_api_pending_count'] = pending_count

        except Exception as ex:
            self.logger.warning("Exception, msg=%s", str(ex))
            result["ecs_api_status"] = str(ex)
            result['ecs_api_desired_count'] = 0

        return result

    def get_ecs_graphql_service_status(self) -> dict:

        result = {}

        ecs_cluster = self.project_config.ecs_cluster_name

        self.logger.info("ecs_cluster: "+ecs_cluster)

        ecs_graphql_service = self.project_config.ecs_graphql_service_name

        self.logger.info("ecs_graphql_service: "+ecs_graphql_service)

        if ecs_graphql_service is None:
            result["ecs_graphql_status"] = "no graphql service"
            return result

        try:
            response = self.ecs_client.describe_services(
                cluster=ecs_cluster,
                services=[ecs_graphql_service]
            )

            if len(response['services']) > 0:

                service = response['services'][0]
                status = service['status']
                desired_count = service['desiredCount']
                running_count = service['runningCount']
                pending_count = service['pendingCount']

                result['ecs_graphql_status'] = status
                result['ecs_graphql_desired_count'] = desired_count
                result['ecs_graphql_running_count'] = running_count
                result['ecs_graphql_pending_count'] = pending_count

        except Exception as ex:
            self.logger.warning("Exception, msg=%s", str(ex))
            result["ecs_graphql_status"] = str(ex)
            result['ecs_graphql_desired_count'] = 0

        return result

    def get_database_status(self) -> dict:

        result = {}

        db_identifier = os.getenv("db_identifier")

        self.logger.info("db_identifier: "+db_identifier)

        try:
            response = self.rds_client.describe_db_instances(DBInstanceIdentifier=db_identifier)

            db_instance = response['DBInstances'][0]

            # https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/accessing-monitoring.html#Overview.DBInstance.Status
            db_status = db_instance['DBInstanceStatus']

            result['db_status'] = db_status

        except Exception as ex:
            self.logger.warning("Exception, msg=%s", str(ex))
            result['db_status'] = str(ex)

        return result

    def turn_on_database_server(self):

        result = {}

        db_identifier = os.getenv("db_identifier")

        # Turn on RDS
        status = ""

        try:
            response = self.rds_client.start_db_instance(
                DBInstanceIdentifier=db_identifier
            )
            status = response['DBInstance']['DBInstanceStatus']
        except Exception as ex:
            self.logger.warning("Exception, msg=%s", str(ex))
            status = str(ex)

        result['db_status'] = status

        return result

    def turn_off_database_server(self):
        # Turn off RDS
        result = {}

        db_identifier = os.getenv("db_identifier")

        # Turn on RDS
        status = ""

        try:
            response = self.rds_client.stop_db_instance(
                DBInstanceIdentifier=db_identifier
            )
            print(response)
            status = response['DBInstance']['DBInstanceStatus']
        except Exception as ex:
            self.logger.warning("Exception, msg=%s", str(ex))
            status = str(ex)

        result['db_status'] = status

        return result

    def turn_on_ecs_api_service(self):

        result = {}

        ecs_cluster = self.project_config.ecs_cluster_name

        self.logger.info("ecs_cluster: "+ecs_cluster)

        ecs_api_service = self.project_config.ecs_api_service_name

        self.logger.info("ecs_api_service: "+ecs_api_service)

        # Turn on ECS

        try:
            response = self.ecs_client.update_service(
                cluster=ecs_cluster,
                service=ecs_api_service,
                desiredCount=1
            )

            if response is not None and "services" in response and len(response['services']) > 0:
                service = response['services'][0]
                status = service['status']
                desired_count = service['desiredCount']
                running_count = service['runningCount']
                pending_count = service['pendingCount']

                result['ecs_status'] = status
                result['ecs_desired_count'] = desired_count
                result['ecs_running_count'] = running_count
                result['ecs_pending_count'] = pending_count

            elif response is not None and "service" in response:
                service = response['service']
                status = service['status']
                desired_count = service['desiredCount']
                running_count = service['runningCount']
                pending_count = service['pendingCount']

                result['ecs_api_status'] = status
                result['ecs_api_desired_count'] = desired_count
                result['ecs_api_running_count'] = running_count
                result['ecs_api_pending_count'] = pending_count

        except Exception as ex:
            self.logger.warning("Exception, msg=%s", str(ex))
            result["ecs_api_status"] = str(ex)
            result['ecs_api_desired_count'] = 0

        return result

    def turn_off_ecs_api_service(self):

        result = {}

        ecs_cluster = self.project_config.ecs_cluster_name

        self.logger.info("ecs_cluster: "+ecs_cluster)

        ecs_api_service = self.project_config.ecs_api_service_name

        self.logger.info("ecs_service: "+ecs_api_service)

        # Turn on ECS

        try:
            response = self.ecs_client.update_service(
                cluster=ecs_cluster,
                service=ecs_api_service,
                desiredCount=0
            )

            if response is not None and "services" in response and len(response['services']) > 0:
                service = response['services'][0]
                status = service['status']
                desired_count = service['desiredCount']
                running_count = service['runningCount']
                pending_count = service['pendingCount']

                result['ecs_status'] = status
                result['ecs_desired_count'] = desired_count
                result['ecs_running_count'] = running_count
                result['ecs_pending_count'] = pending_count

            elif response is not None and "service" in response:
                service = response['service']
                status = service['status']
                desired_count = service['desiredCount']
                running_count = service['runningCount']
                pending_count = service['pendingCount']

                result['ecs_api_status'] = status
                result['ecs_api_desired_count'] = desired_count
                result['ecs_api_running_count'] = running_count
                result['ecs_api_pending_count'] = pending_count

        except Exception as ex:
            self.logger.warning("Exception, msg=%s", str(ex))
            result["ecs_api_status"] = str(ex)
            result['ecs_api_desired_count'] = 0

        return result

    def turn_on_ecs_graphql_service(self):

        result = {}

        ecs_cluster = self.project_config.ecs_cluster_name

        self.logger.info("ecs_cluster: "+ecs_cluster)

        ecs_graphql_service = self.project_config.ecs_graphql_service_name

        self.logger.info("ecs_graphql_service: "+ecs_graphql_service)

        if ecs_graphql_service is None:
            result["ecs_graphq_status"] = "no graphql service"
            return result

        # Turn on ECS

        try:
            response = self.ecs_client.update_service(
                cluster=ecs_cluster,
                service=ecs_graphql_service,
                desiredCount=1
            )

            if response is not None and "services" in response and len(response['services']) > 0:
                service = response['services'][0]
                status = service['status']
                desired_count = service['desiredCount']
                running_count = service['runningCount']
                pending_count = service['pendingCount']

                result['ecs_status'] = status
                result['ecs_desired_count'] = desired_count
                result['ecs_running_count'] = running_count
                result['ecs_pending_count'] = pending_count

            elif response is not None and "service" in response:
                service = response['service']
                status = service['status']
                desired_count = service['desiredCount']
                running_count = service['runningCount']
                pending_count = service['pendingCount']

                result['ecs_graphql_status'] = status
                result['ecs_graphql_desired_count'] = desired_count
                result['ecs_graphql_running_count'] = running_count
                result['ecs_graphql_pending_count'] = pending_count

        except Exception as ex:
            self.logger.warning("Exception, msg=%s", str(ex))
            result["ecs_graphql_status"] = str(ex)
            result['ecs_graphql_desired_count'] = 0

        return result

    def turn_off_ecs_graphl_service(self):

        result = {}

        ecs_cluster = self.project_config.ecs_cluster_name

        self.logger.info("ecs_cluster: "+ecs_cluster)

        ecs_graphql_service = self.project_config.ecs_graphql_service_name

        self.logger.info("ecs_graphql_service: "+ecs_graphql_service)

        # Turn on ECS

        try:
            response = self.ecs_client.update_service(
                cluster=ecs_cluster,
                service=ecs_graphql_service,
                desiredCount=0
            )

            if response is not None and "services" in response and len(response['services']) > 0:
                service = response['services'][0]
                status = service['status']
                desired_count = service['desiredCount']
                running_count = service['runningCount']
                pending_count = service['pendingCount']

                result['ecs_status'] = status
                result['ecs_desired_count'] = desired_count
                result['ecs_running_count'] = running_count
                result['ecs_pending_count'] = pending_count

            elif response is not None and "service" in response:
                service = response['service']
                status = service['status']
                desired_count = service['desiredCount']
                running_count = service['runningCount']
                pending_count = service['pendingCount']

                result['ecs_graphql_status'] = status
                result['ecs_graphql_desired_count'] = desired_count
                result['ecs_graphql_running_count'] = running_count
                result['ecs_graphql_pending_count'] = pending_count

        except Exception as ex:
            self.logger.warning("Exception, msg=%s", str(ex))
            result["ecs_graphql_status"] = str(ex)
            result['ecs_graphql_desired_count'] = 0

        return result
    def any_user_activity(self) -> bool:

        last_created_at = self.get_db_latest_timestamp()

        if last_created_at is None:
            return False

        utah_tz = pytz.timezone('America/Denver')

        utah_time_now = datetime.now(utah_tz)

        _mins_ago = utah_time_now - timedelta(minutes=60)

        self.logger.info("created_at:{}, _mins_ago={}".format(last_created_at, _mins_ago))

        if last_created_at < _mins_ago:
            return True

        return False
    def get_db_latest_timestamp(self) -> datetime:

        last_created_at = None

        s3_bucket = os.getenv('s3_bucket')

        s3_key = 'db_last_activity_' + self.env + '.json'

        self.logger.info("s3_bucket={}, s3_key={}".format(s3_bucket, s3_key))

        try:

            s3_response = self.s3_client.get_object(Bucket=s3_bucket, Key=s3_key)

            # self.logger.info("s3_response={}".format(s3_response))

            last_activity = s3_response['Body'].read().decode('utf-8')

            last_activity = json.loads(last_activity)

            # self.logger.info("file_content={} type={}, createdAt={}, type={}".format(last_activity, type(last_activity), last_activity.get('createdAt'), type(last_activity.get('createdAt'))))

            created_at_str = last_activity.get('createdAt')

            last_created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%S.%f")

            utah_tz = pytz.timezone('America/Denver')

            last_created_at = utah_tz.localize(last_created_at)

        except (Exception) as error:
            self.logger.warning("Exception, msg={}".format(error))

        return last_created_at

    def get_project_db_latest_timestamp(self) -> datetime:

        last_created_at = None

        s3_bucket = os.getenv('s3_bucket')

        s3_key = 'db_last_activity_'+self.env+'.json'

        self.logger.info("s3_bucket={}, s3_key={}".format(s3_bucket, s3_key))

        try:

            s3_response = self.s3_client.get_object(Bucket=s3_bucket, Key=s3_key)

            last_activity = s3_response['Body'].read().decode('utf-8')

            last_activity = json.loads(last_activity)

            project_last_activity = json.loads(last_activity.get(self.project_config.name))

            created_at_str = project_last_activity.get('createdAt')

            last_created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%S.%f")

            utah_tz = pytz.timezone('America/Denver')

            last_created_at = utah_tz.localize(last_created_at)

        except (Exception) as error:
            self.logger.warning("Exception, msg={}".format(error))

        return last_created_at
