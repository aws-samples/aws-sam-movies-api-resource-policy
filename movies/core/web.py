import json


def cors_web_response(status_code, body):
    """
    Generate a valid API Gateway CORS enabled JSON body response
    :param status_code: string of a HTTP status code
    :param body: Dictionary object, converted to JSON
    :param event: API Gateway trigger event
    :return:
    """
    return {
        'statusCode': status_code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps(body)
    }
