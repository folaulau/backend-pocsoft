from chalice import Chalice
import os
import logging

# from chalicelib.blueprints.sushi_api import sushi_api

from chalicelib.service.sushi_service import SushiService

app = Chalice(app_name='backend-pocsoft')
app.api_gateway_stage = ''
app.api.cors = True
app.debug = True

os.environ['TZ'] = 'America/Denver'

# Set logging format
formatter = logging.Formatter(os.getenv('log_format', '%(asctime)s %(filename)s %(funcName)s %(lineno)d %(levelname)-8s %(message)s'), datefmt='%Y-%m-%d %I:%M:%S %p')
app.log.handlers[0].setFormatter(formatter)
app.log.setLevel(os.getenv('log_level', 'INFO'))

sushi_service = SushiService()

# app.register_blueprint(url_prefix="/sushi", blueprint=sushi_api, name_prefix="sushi")

@app.middleware('all')
def middleware(event, get_response):
    # app.log.info("before event path={}".format(event.path))
    response = get_response(event)
    # app.log.info("after event")
    return response

@app.route('/')
def index():
    return {'app': 'pocsoft'}


# ================== sushi endpoints =================

@app.route("/sushi/turnon-servers", methods=["POST"])
def sushi_turnon_servers():
    app.log.info("turnon_servers...")
    status = sushi_service.turnon_servers()
    return status

@app.route("/sushi/turnoff-servers", methods=["POST"])
def sushi_turnoff_servers():
    app.log.info("turnoff_servers...")
    status = sushi_service.turnoff_servers()
    return status

@app.route("/sushi/turnoff-servers-on-inactivity", methods=["POST"])
def sushi_turnoff_servers_for_inactivity():
    app.log.info("turnoff_servers_for_inactivity...")
    status = sushi_service.shutoff_services_for_inactivity()
    return status


@app.route("/sushi/servers-status", methods=["GET"])
def sushi_get_all_servers_status():
    app.log.info("get_all_servers_status...")
    status = sushi_service.get_servers_status()
    return status

@app.lambda_function(name="sushi_inactivity_shutoff")
def sushi_inactivity_shutoff(event, context):
    app.log.info("sushi_inactivity_shutoff")

    status = sushi_service.shutoff_services_for_inactivity()

    return status


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
