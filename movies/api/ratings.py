import os
import sys
import logging
import boto3
import urllib
import json
from movies.core import web
from boto3.dynamodb.conditions import Key

# Set Logging Level
logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def get_ratings(event, context):
    try:
        year = urllib.unquote(urllib.unquote(event["pathParameters"]["year"]))
    except:
        logger.error('Unable to validate RAiD parameter: {}'.format(sys.exc_info()[0]))
        return web.cors_web_response(
            '400',
            {'message': "Incorrect path parameter type formatting for RAiD handle. Ensure it is a URL encoded string"}
        )

    query_parameters = {
        'KeyConditionExpression': Key('year').eq(str(year))
    }

    try:
        # Initialise DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ["RATINGS_TABLE"])

        # Query table using parameters given and built to return a list of RAiDs the owner is attached too
        query_response = table.query(**query_parameters)

        # Build response body
        return_body = {
            'ratings': query_response["Items"],
            'count': query_response["Count"],
            'scannedCount': query_response["ScannedCount"]
        }

        return web.cors_web_response('200', return_body)

    except Exception as e:
        logger.error('Unable to generate a DynamoDB list response: {}'.format(sys.exc_info()[0]))
        return web.cors_web_response(
            '500', {'message': "Unable to perform request due to error. Please check structure of the parameters."}
        )


def create_rating(event, context):
    try:
        # Parse path parameters
        year = urllib.unquote(urllib.unquote(event["pathParameters"]["year"]))

        # Interpret and validate request body
        body = json.loads(event["body"])

        if "title" not in body or ("rating" not in body):
            return web.cors_web_response('400', {'message': "Incorrect parameters or format."})

        # Define item
        item = {
            'title': body["title"],
            'rating': body["rating"],
            "year": year
        }

        # Initialise DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ["RATINGS_TABLE"])

        # Send Dynamo DB put response
        table.put_item(Item=item)

        return web.cors_web_response('200', item)

    except Exception, e:
        logger.error('Unexpected error string: {}'.format(str(e)))
        return web.cors_web_response(
            '500',
            {'message': "Unknown error has occurred."}
        )


def delete_rating(event, context):
    try:
        # Parse path parameters
        year = urllib.unquote(urllib.unquote(event["pathParameters"]["year"]))
        title = urllib.unquote(urllib.unquote(event["pathParameters"]["title"]))

        # Initialise DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ["RATINGS_TABLE"])

        table.delete_item(
            Key={
                'year': year,
                'title': title
            },
            ReturnValues='ALL_OLD'
        )

        return web.cors_web_response('200', {'message': 'rating "{}" has been removed'.format(title)})

    except Exception, e:
        logger.error('Unexpected error string: {}'.format(str(e)))
        return web.cors_web_response(
            '500',
            {'message': "Unknown error has occurred."}
        )
