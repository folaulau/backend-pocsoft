from chalice import Blueprint, Response, BadRequestError, UnauthorizedError, CORSConfig
import json
import io

sushi_api = Blueprint("sushi_api")

@sushi_api.lambda_function(name="inactivity_shutoff")
def inactivity_shutoff(event, context):
    sushi_api.log.info("inactivity_shutoff")
