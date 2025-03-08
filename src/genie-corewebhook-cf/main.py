import functions_framework
import json
import logging
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def get_flatrequest_params(param, default=None):
    request_json = request.get_json(silent=True)
    request_args = request.args

    return (request_json or {}).get(param, default) or request_args.get(param, default)

@app.route("/greetings", methods=["GET", "POST"])
def handler_greetings():
    name = get_flatrequest_params("name")
    greetings_response = {"greetings": f"Hello {name}"} 
    return jsonify(greetings_response)

@app.route("/getcustomerprofile", methods=["GET", "POST"])
def getcustomerprofile():
    customerprofile_response = {
        "fname": "Shanky",
        "prepaidmobile": "60000001",
        "postpaidmobile": "60000002"
    } 
    return jsonify(customerprofile_response)

@functions_framework.http
def main(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)    