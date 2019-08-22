from flask import Flask, Response, request, json, jsonify, url_for, g, _request_ctx_stack, abort, has_request_context, session
from ebay import app,db

def seasoned_response( result, status, message=None ):
    if status == "200" and message == None:
        message = "Succeeded"
    elif status == "400" and message == None:
        message = "Bad Request"
    elif status == "401" and message == None:
        message = "Unauthorized"
    elif status == "403" and message == None:
        message = "Forbidden"
    elif status == "404" and message == None:
        message = "Not Found"
    elif status == "405" and message == None:
        message = "Method Not Allowed"
    elif status == "406" and message == None:
        message = "Not Acceptable"
    elif status == "409" and message == None:
        message = "Conflict"

    nice = {
        'status': status,
        'message': message,
        'response': result
        }

    return json.dumps( nice, sort_keys=False, indent=2)