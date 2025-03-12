import functions_framework
from flask import Flask, request, jsonify
import logging

from mockresponses import customerprofile_response, balances_response, plans_response, bundles_response
from agent_faqwifi import faqsearch_homewifi

logging.basicConfig(level=logging.INFO)

# Create a Flask app
app = Flask(__name__)

def get_flatrequest_params(param, default=None):
    request_json = request.get_json(silent=True)
    request_args = request.args

    return (request_json or {}).get(param, default) or request_args.get(param, default)

def logrequest(operation: str, request):
    logging.info(f"{operation} API REQUEST - ... {request}; Body - {request.get_json(silent=True)} ... END")

def logresponse(operation: str, response: str):
    logging.info(f"{operation} API RESPONSE - ... {response} ... END") 

# Define a route with Flask
@app.route("/greetings", methods=["GET", "POST"])
def handler_greetings():
    logrequest("Greetings", request)
    name = get_flatrequest_params("name")
    if name:
        greetings_response = {"greetings": f"Hello {name}"}
    else:
        # greetings_response = jsonify({'error': 'Missing name field'}), 400
        greetings_response = {"greetings": "Hello Developer"}
    logresponse("Greetings", greetings_response)    
    return greetings_response

@app.route("/getcustomerprofile", methods=["GET", "POST"])
def handler_getcustomerprofile():
    logrequest("Getcustomerprofile", request)
    logresponse("Getcustomerprofile", customerprofile_response)
    return customerprofile_response

@app.route("/webhook", methods=["GET", "POST"])
def handler_dfcx_webhook():
    logrequest("DFCX Webhook", request)

    request_body = request.get_json()
    webhook_response = ""

    if request:
        user_session_obj = request_body["sessionInfo"]
        dfcx_session = user_session_obj["session"]
        fulfillment_info_obj = request_body["fulfillmentInfo"]
        user_text = request_body["text"]

        webhook_tag = fulfillment_info_obj["tag"]

        if webhook_tag:
            logging.info(f"Webhook request tag - {webhook_tag}")

            if webhook_tag == "getcustomerprofile":
                user_session_obj["parameters"]["customer_fname"] = customerprofile_response["customer_fname"]
                user_session_obj["parameters"]["customer_postpaidmobile"] = customerprofile_response["customer_postpaidmobile"]
                user_session_obj["parameters"]["customer_billingacct"] = customerprofile_response["customer_billingacct"]
                webhook_response = {"sessionInfo": user_session_obj}

            if webhook_tag == "getacctbalances":
                # webhook_response = {
                #     "fulfillmentResponse": {
                #         "messages": [
                #             {
                #                 "payload": balances_response
                #             }
                #         ]
                #     }
                # }
                user_session_obj["parameters"]["webhook_response"] = balances_response
                webhook_response = {"sessionInfo": user_session_obj}

            if webhook_tag == "getacctplans":
                user_session_obj["parameters"]["webhook_response"] = plans_response
                webhook_response = {"sessionInfo": user_session_obj}  

            if webhook_tag == "getacctbundles":
                user_session_obj["parameters"]["webhook_response"] = bundles_response
                webhook_response = {"sessionInfo": user_session_obj} 

            if webhook_tag == "faqhomewifi":
                
                user_turn = 0
                if "faqhomewifi_userturn" in user_session_obj["parameters"]:
                    user_turn = user_session_obj["faqhomewifi_userturn"]
                else:
                    user_turn = user_turn + 1
                user_session_obj["faqhomewifi_userturn"] = user_turn                
                
                user_session_obj["parameters"]["webhook_response"] = faqsearch_homewifi(user_text, dfcx_session)
                webhook_response = {"sessionInfo": user_session_obj}                                                                   

        else:
            logging.error(f"Webhook request tag MISSING")
            webhook_response = jsonify({'error': 'Missing Webhook tag field'}), 400
    else:
        logging.error(f"Webhook request MISSING")
        webhook_response = jsonify({'error': 'Missing Webhook request body'}), 400

    logresponse("DFCX Webhook", webhook_response)
    return webhook_response        


# Cloud Function entry point
@functions_framework.http
def main(request):
    """HTTP Cloud Function that serves a Flask app with
    a greeting endpoint at /greetings.
    """
    # # Handle CORS for preflight requests
    # if request.method == 'OPTIONS':
    #     headers = {
    #         'Access-Control-Allow-Origin': '*',
    #         'Access-Control-Allow-Methods': 'POST',
    #         'Access-Control-Allow-Headers': 'Content-Type',
    #         'Access-Control-Max-Age': '3600'
    #     }
    #     return ('', 204, headers)
    
    # # Set CORS headers for the main request
    # headers = {'Access-Control-Allow-Origin': '*'}
    
    # Create a context for the Flask app with the current request
    with app.request_context(request.environ):
        # Process the request with Flask
        response = app.full_dispatch_request()
    
    # # Add CORS headers to the response
    # for key, value in headers.items():
    #     response.headers[key] = value
    
    return response