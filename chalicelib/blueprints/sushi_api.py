from chalice import Blueprint, Response, BadRequestError, UnauthorizedError, CORSConfig
import json
import io

from chalicelib.service.sushi_service import SushiService

sushi_api = Blueprint("sushi_api")

sushi_service = SushiService()

@sushi_api.lambda_function(name="inactivity_shutoff")
def inactivity_shutoff(event, context):
    sushi_api.log.info("inactivity_shutoff")

    status = sushi_service.shutoff_services_for_inactivity();

    return status;

