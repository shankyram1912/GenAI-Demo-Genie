import functions_framework
import json
import logging
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def get_request_params(param, default=None):
    request_json = request.get_json(silent=True)
    request_args = request.args

    return (request_json or {}).get(param, default) or request_args.get(param, default)

@app.route("/greetings", methods=["GET", "POST"])
def handler_greetings():
    name = get_request_params("name")
    response_json = {"greetings": f"Hello {name}"} # Create a dictionary
    return jsonify(response_json) # Return JSON response using jsonify

@functions_framework.http
def main(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()