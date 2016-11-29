from __future__ import print_function

import logging
import json
import urllib2
import base64

import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

API_BASE = {{ scoring.url }}
API_TOKEN = {{ scoring.api_token }}

DYNAMODB = boto3.resource('dynamodb')
STATE_TABLE = DYNAMODB.Table('gameday-messages-state')

def handle(event, context):
    """
    Lambda handler
    """
    logger.info("Event: {}".format(event))

    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data'])
        # parse json
        message = json.loads(payload)
        # parse message
        msg_id = message['Id']
        part_number = message['PartNumber']
        data = message['Data']
        # put the part received into dynamo
        proceed = store_message(msg_id, part_number, data)
        if proceed is False:
            # we have already processed this message so don't proceed
            print("skipping duplicate message")
            continue
        # Try to get the parts of the message from the Dynamo.
        check_messages(msg_id)

    return 'OK'

def store_message(input_id, part_num, data):
    """
    stores the message locally on a file on disk for persistence
    """
    try:
        STATE_TABLE.update_item(
            Key={
                'Id': input_id
            },
            UpdateExpression="set #key=:val",
            ExpressionAttributeValues={
                ":val":data
            },
            ExpressionAttributeNames={
                "#key":str(part_num),
                "#p":"processed"
            },
            ConditionExpression="attribute_not_exists(#p)"
        )
    except Exception:
        # conditional update failed since we have already processed this message
        # at this point we can bail since we don't want to process again
        # and lose cash moneys
        return False

def check_messages(input_id):
    """
    checking to see in dynamo if we have the part already
    """
    # do a get item from dynamo to see if item exists
    response = STATE_TABLE.get_item(
        Key={
            'Id': input_id
        },
        ConsistentRead=True
    )
    item = response['Item']
    # check if both parts exist
    if "0" in item and "1" in item:
        print("we have both!")
        # we have all the parts
        build_final(item, input_id)
        # now we need to update dynamo saying we processed this message
        STATE_TABLE.update_item(
            Key={
                'Id': input_id
            },
            UpdateExpression="set #p=:val",
            ExpressionAttributeValues={
                ":val":"Y"
            },
            ExpressionAttributeNames={
                "#p":"processed"
            }
        )
    else:
        # we have some parts but not all
        return

def build_final(parts, msg_id):
    """
    building the response to return to the server
    """
    # We can build the final message.
    result = parts['0'] + parts['1']
    # sending the response to the score calculator
    # format:
    #   url -> api_base/jFgwN4GvTB1D2QiQsQ8GHwQUbbIJBS6r7ko9RVthXCJqAiobMsLRmsuwZRQTlOEW
    #   headers -> x-gameday-token = API_token
    #   data -> EaXA2G8cVTj1LGuRgv8ZhaGMLpJN2IKBwC5eYzAPNlJwkN4Qu1DIaI3H1zyUdf1H5NITR
    logger.debug("ID: {}".format(msg_id))
    logger.debug("RESULT: {}".format(result))
    # make request
    url = API_BASE + '/' + msg_id
    headers = {
        'x-gameday-token': API_TOKEN
    }
    req = urllib2.Request(url, data=result, headers=headers)
    resp = urllib2.urlopen(req)
    resp.close()

def get_message_stats():
    """
    provides a status that players can check
    """
    msg_count = len(MESSAGES.keys())
    return "There are %d messages in the MESSAGES dictionary" % msg_count
