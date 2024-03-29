from chalice import Blueprint, Response, BadRequestError, UnauthorizedError, CORSConfig
import json
import io

from chalicelib.service.sushi_service import SushiService

sushi_api = Blueprint("sushi_api")

sushi_service = SushiService()

@sushi_api.route("/turnon-servers", methods=["POST"])
def turnon_servers():
    sushi_api.log.info("turnon_servers...")
    status = sushi_service.turnon_servers()
    return status

@sushi_api.route("/turnoff-servers", methods=["POST"])
def turnoff_servers():
    sushi_api.log.info("turnoff_servers...")
    status = sushi_service.turnoff_servers()
    return status

@sushi_api.route("/turnoff-servers-on-inactivity", methods=["POST"])
def turnoff_servers_for_inactivity():
    sushi_api.log.info("turnoff_servers_for_inactivity...")
    status = sushi_service.shutoff_services_for_inactivity()
    return status


@sushi_api.route("/servers-status", methods=["GET"])
def get_all_servers_status():
    sushi_api.log.info("get_all_servers_status...")
    status = sushi_service.get_servers_status()
    return status


